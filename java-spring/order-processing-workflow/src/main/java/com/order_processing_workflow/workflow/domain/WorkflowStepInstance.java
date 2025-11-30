package com.order_processing_workflow.workflow.domain;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.Objects;

@Entity
@Table(name = "workflow_step_instances")
public class WorkflowStepInstance {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String status;          // PENDING, IN_PROGRESS, COMPLETED, FAILED
    private LocalDateTime startedAt;
    private LocalDateTime completedAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "workflow_instance_id")
    private WorkflowInstance workflowInstance;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "step_definition_id")
    private WorkflowStepDefinition stepDefinition;

    private int sequenceOrder;

    public WorkflowStepInstance() {}

    public WorkflowStepInstance(WorkflowStepDefinition stepDefinition, int sequenceOrder) {
        this.stepDefinition = stepDefinition;
        this.sequenceOrder = sequenceOrder;
        this.status = "PENDING";
    }

    // Getters and Setters
    public void setWorkflowInstance(WorkflowInstance workflowInstance) {
        this.workflowInstance = workflowInstance;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof WorkflowStepInstance)) return false;
        return Objects.equals(id, ((WorkflowStepInstance)o).id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
