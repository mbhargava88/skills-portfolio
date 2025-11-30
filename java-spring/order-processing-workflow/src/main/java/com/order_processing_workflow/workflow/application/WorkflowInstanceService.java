package com.order_processing_workflow.workflow.application;

import java.util.*;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.order_processing_workflow.workflow.domain.*;
import com.order_processing_workflow.workflow.infrastructure.*;

@Service
public class WorkflowInstanceService {

    private final WorkflowDefinitionRepository workflowDefinitionRepository;
    private final WorkflowInstanceRepository workflowInstanceRepository;
    private final WorkflowStepInstanceRepository stepInstanceRepository;

    public WorkflowInstanceService(
            WorkflowDefinitionRepository workflowDefinitionRepository,
            WorkflowInstanceRepository workflowInstanceRepository,
            WorkflowStepInstanceRepository stepInstanceRepository) {
        this.workflowDefinitionRepository = workflowDefinitionRepository;
        this.workflowInstanceRepository = workflowInstanceRepository;
        this.stepInstanceRepository = stepInstanceRepository;
    }

    /**
     * Start a workflow for a given entity (like an Order).
     */
    @Transactional
    public WorkflowInstance startWorkflow(Long workflowDefinitionId, String entityType, Long entityId) {
        WorkflowDefinition definition = workflowDefinitionRepository.findById(workflowDefinitionId)
                .orElseThrow(() -> new RuntimeException("Workflow definition not found"));

        WorkflowInstance instance = new WorkflowInstance(definition, entityType, entityId, WorkflowStatus.RUNNING);
        workflowInstanceRepository.save(instance);

        // Find all steps eligible to start (no dependency)
        List<WorkflowStepDefinition> startableSteps = definition.getStepMappings().stream()
                .map(WorkflowStepDefinitionMapping::getStepDefinition)
                .filter(step -> step.getDependsOn() == null)
                .collect(Collectors.toList());

        startableSteps.forEach(stepDef -> createAndRunStep(instance, stepDef));

        return instance;
    }

    /**
     * Mark a step as completed and trigger next eligible steps.
     */
    @Transactional
    public void markStepCompleted(Long stepInstanceId) {
        WorkflowStepInstance stepInstance = stepInstanceRepository.findById(stepInstanceId)
                .orElseThrow(() -> new RuntimeException("Step instance not found"));

        stepInstance.setStatus(WorkflowStepStatus.COMPLETED);
        stepInstanceRepository.save(stepInstance);

        WorkflowInstance instance = stepInstance.getWorkflowInstance();

        // Find dependent steps
        List<WorkflowStepDefinition> nextSteps = instance.getWorkflowDefinition()
                .getStepMappings().stream()
                .map(WorkflowStepDefinitionMapping::getStepDefinition)
                .filter(step -> step.getDependsOn() != null
                        && step.getDependsOn().getId().equals(stepInstance.getStepDefinition().getId()))
                .collect(Collectors.toList());

        // Check if their dependencies are all satisfied
        for (WorkflowStepDefinition nextStep : nextSteps) {
            boolean allDepsDone = areDependenciesComplete(instance, nextStep);
            if (allDepsDone) {
                // Parallel group check — group steps started together
                List<WorkflowStepDefinition> parallelGroup = findParallelGroup(nextStep, instance);
                parallelGroup.forEach(stepDef -> createAndRunStep(instance, stepDef));
            }
        }

        // If all steps complete → mark workflow as complete
        if (isWorkflowComplete(instance)) {
            instance.setStatus(WorkflowStatus.COMPLETED);
            workflowInstanceRepository.save(instance);
        }
    }

    private void createAndRunStep(WorkflowInstance instance, WorkflowStepDefinition stepDef) {
        WorkflowStepInstance stepInstance = new WorkflowStepInstance(instance, stepDef, WorkflowStepStatus.RUNNING);
        stepInstanceRepository.save(stepInstance);
        // Future: dynamically invoke handler from stepDef.getCodeHandler()
    }

    private boolean areDependenciesComplete(WorkflowInstance instance, WorkflowStepDefinition stepDef) {
        WorkflowStepDefinition dependency = stepDef.getDependsOn();
        if (dependency == null) return true;

        return stepInstanceRepository.existsByWorkflowInstanceAndStepDefinitionAndStatus(
                instance, dependency, WorkflowStepStatus.COMPLETED);
    }

    private List<WorkflowStepDefinition> findParallelGroup(WorkflowStepDefinition stepDef, WorkflowInstance instance) {
        String group = stepDef.getParallelGroup();
        if (group == null) return Collections.singletonList(stepDef);

        return instance.getWorkflowDefinition()
                .getStepMappings().stream()
                .map(WorkflowStepDefinitionMapping::getStepDefinition)
                .filter(s -> Objects.equals(s.getParallelGroup(), group))
                .collect(Collectors.toList());
    }

    private boolean isWorkflowComplete(WorkflowInstance instance) {
        List<WorkflowStepInstance> steps = stepInstanceRepository.findByWorkflowInstance(instance);
        return steps.stream().allMatch(s -> s.getStatus() == WorkflowStepStatus.COMPLETED);
    }
}
