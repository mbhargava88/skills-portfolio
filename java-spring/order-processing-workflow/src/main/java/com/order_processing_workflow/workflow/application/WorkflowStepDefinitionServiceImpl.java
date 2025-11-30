package com.order_processing_workflow.workflow.application;

import com.order_processing_workflow.workflow.domain.WorkflowStepDefinition;
import com.order_processing_workflow.workflow.domain.WorkflowStepDefinitionRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class WorkflowStepDefinitionServiceImpl implements WorkflowStepDefinitionService {

    private final WorkflowStepDefinitionRepository stepDefinitionRepository;

    public WorkflowStepDefinitionServiceImpl(WorkflowStepDefinitionRepository stepDefinitionRepository) {
        this.stepDefinitionRepository = stepDefinitionRepository;
    }

    public WorkflowStepDefinition createStep(String name, String codeHandler, String description) {
        WorkflowStepDefinition step = new WorkflowStepDefinition(name, codeHandler, description);
        return stepDefinitionRepository.save(step);
    }

    public List<WorkflowStepDefinition> getAllSteps() {
        return stepDefinitionRepository.findAll();
    }

    public WorkflowStepDefinition getStepById(Long id) {
        return stepDefinitionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Step definition not found: " + id));
    }
}
