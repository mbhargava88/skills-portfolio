package com.order_processing_workflow.workflow.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface WorkflowInstanceRepository extends JpaRepository<WorkflowInstance, Long> {
    List<WorkflowInstance> findByEntityTypeAndEntityId(String entityType, Long entityId);
}
