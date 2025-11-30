package com.order_processing_workflow.workflow.infrastructure;

import com.order_processing_workflow.workflow.domain.WorkflowStepInstance;
import com.order_processing_workflow.workflow.domain.WorkflowStepInstanceRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface JpaWorkflowStepInstanceRepository extends WorkflowStepInstanceRepository, JpaRepository<WorkflowStepInstance, Long> {
    List<WorkflowStepInstance> findByWorkflowInstanceId(Long workflowInstanceId);
}
