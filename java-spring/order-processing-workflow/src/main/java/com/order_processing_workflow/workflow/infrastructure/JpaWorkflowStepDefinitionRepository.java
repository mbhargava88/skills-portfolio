package com.order_processing_workflow.workflow.infrastructure;

import com.order_processing_workflow.workflow.domain.WorkflowStepDefinition;
import com.order_processing_workflow.workflow.domain.WorkflowStepDefinitionRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface JpaWorkflowStepDefinitionRepository extends WorkflowStepDefinitionRepository, JpaRepository<WorkflowStepDefinition, Long> {
    List<WorkflowStepDefinition> findByWorkflowDefinitionIdOrderByStepOrder(Long workflowDefinitionId);
}
