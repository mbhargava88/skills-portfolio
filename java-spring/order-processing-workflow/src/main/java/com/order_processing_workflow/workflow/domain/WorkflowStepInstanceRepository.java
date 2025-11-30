package com.order_processing_workflow.workflow.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface WorkflowStepInstanceRepository extends JpaRepository<WorkflowStepInstance, Long> {
    List<WorkflowStepInstance> findByWorkflowInstanceIdOrderBySequenceOrder(Long workflowInstanceId);
}
