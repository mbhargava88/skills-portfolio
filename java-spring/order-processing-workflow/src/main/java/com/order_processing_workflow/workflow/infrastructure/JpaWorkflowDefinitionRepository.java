package com.order_processing_workflow.workflow.infrastructure;

import com.order_processing_workflow.workflow.domain.WorkflowDefinition;
import com.order_processing_workflow.workflow.domain.WorkflowDefinitionRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JpaWorkflowDefinitionRepository extends WorkflowDefinitionRepository, JpaRepository<WorkflowDefinition, Long> {
}
