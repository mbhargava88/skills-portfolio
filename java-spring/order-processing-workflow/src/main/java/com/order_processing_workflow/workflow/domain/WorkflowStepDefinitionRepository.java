// src/main/java/com/order_processing_workflow/workflow/domain/WorkflowStepDefinitionRepository.java
package com.order_processing_workflow.workflow.domain;

import org.springframework.data.jpa.repository.JpaRepository;

public interface WorkflowStepDefinitionRepository extends JpaRepository<WorkflowStepDefinition, Long> {
}
