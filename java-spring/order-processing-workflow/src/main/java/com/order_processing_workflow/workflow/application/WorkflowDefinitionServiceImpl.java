package com.order_processing_workflow.workflow.application;

import com.order_processing_workflow.workflow.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class WorkflowDefinitionServiceImpl implements WorkflowDefinitionService{

    private final WorkflowDefinitionRepository workflowRepository;
    private final WorkflowStepDefinitionRepository stepRepository;
    private final WorkflowStepDefinitionMappingRepository mappingRepository;

    public WorkflowDefinitionServiceImpl(WorkflowDefinitionRepository workflowRepository,
                                         WorkflowStepDefinitionRepository stepRepository,
                                         WorkflowStepDefinitionMappingRepository mappingRepository) {
        this.workflowRepository = workflowRepository;
        this.stepRepository = stepRepository;
        this.mappingRepository = mappingRepository;
    }

    @Transactional
    public WorkflowDefinition createWorkflow(String name, String entityType, List<Long> stepIdsInSequence) {
        WorkflowDefinition workflow = new WorkflowDefinition(name, entityType);
        workflow = workflowRepository.save(workflow);

        int order = 1;
        for (Long stepId : stepIdsInSequence) {
            WorkflowStepDefinition step = stepRepository.findById(stepId)
                    .orElseThrow(() -> new RuntimeException("Step not found: " + stepId));

            WorkflowStepDefinitionMapping mapping = new WorkflowStepDefinitionMapping();
            mapping.setWorkflowDefinition(workflow);
            mapping.setStepDefinition(step);
            mapping.setSequenceOrder(order++);
            mappingRepository.save(mapping);
            workflow.addStepMapping(mapping);
        }
        return workflow;
    }

    public List<WorkflowDefinition> getAllWorkflows() {
        return workflowRepository.findAll();
    }

    public WorkflowDefinition getWorkflowById(Long id) {
        return workflowRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Workflow not found: " + id));
    }

    public List<WorkflowStepDefinitionMapping> getWorkflowSteps(Long workflowId) {
        return mappingRepository.findByWorkflowDefinitionIdOrderBySequenceOrder(workflowId);
    }
}
