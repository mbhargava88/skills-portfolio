package com.order_processing_workflow.workflow.infrastructure;

import com.order_processing_workflow.workflow.domain.WorkflowInstance;
import com.order_processing_workflow.workflow.domain.WorkflowInstanceRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface JpaWorkflowInstanceRepository extends WorkflowInstanceRepository, JpaRepository<WorkflowInstance, Long> {
    List<WorkflowInstance> findByEntityTypeAndEntityId(String entityType, Long entityId);
}
