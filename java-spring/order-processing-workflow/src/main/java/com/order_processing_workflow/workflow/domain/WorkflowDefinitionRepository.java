// src/main/java/com/order_processing_workflow/workflow/domain/WorkflowDefinitionRepository.java
package com.order_processing_workflow.workflow.domain;

import org.springframework.data.jpa.repository.JpaRepository;

public interface WorkflowDefinitionRepository extends JpaRepository<WorkflowDefinition, Long> {
}
