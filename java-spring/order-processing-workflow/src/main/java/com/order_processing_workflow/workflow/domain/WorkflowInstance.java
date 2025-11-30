package com.order_processing_workflow.workflow.domain;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@Entity
@Table(name = "workflow_instances")
public class WorkflowInstance {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String entityType;   // e.g., ORDER, DELIVERY
    private Long entityId;       // The actual entity id (order id, delivery id)
    private String status;       // e.g., PENDING, IN_PROGRESS, COMPLETED, FAILED

    private LocalDateTime startedAt;
    private LocalDateTime completedAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "workflow_definition_id")
    private WorkflowDefinition workflowDefinition;

    @OneToMany(mappedBy = "workflowInstance", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<WorkflowStepInstance> stepInstances = new ArrayList<>();

    public WorkflowInstance() {}

    public WorkflowInstance(WorkflowDefinition workflowDefinition, String entityType, Long entityId) {
        this.workflowDefinition = workflowDefinition;
        this.entityType = entityType;
        this.entityId = entityId;
        this.status = "PENDING";
        this.startedAt = LocalDateTime.now();
    }

    public void addStepInstance(WorkflowStepInstance stepInstance) {
        stepInstances.add(stepInstance);
        stepInstance.setWorkflowInstance(this);
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEntityType() {
        return entityType;
    }

    public void setEntityType(String entityType) {
        this.entityType = entityType;
    }

    public Long getEntityId() {
        return entityId;
    }

    public void setEntityId(Long entityId) {
        this.entityId = entityId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public LocalDateTime getStartedAt() {
        return startedAt;
    }

    public void setStartedAt(LocalDateTime startedAt) {
        this.startedAt = startedAt;
    }

    public LocalDateTime getCompletedAt() {
        return completedAt;
    }

    public void setCompletedAt(LocalDateTime completedAt) {
        this.completedAt = completedAt;
    }

    public WorkflowDefinition getWorkflowDefinition() {
        return workflowDefinition;
    }

    public void setWorkflowDefinition(WorkflowDefinition workflowDefinition) {
        this.workflowDefinition = workflowDefinition;
    }

    public List<WorkflowStepInstance> getStepInstances() {
        return stepInstances;
    }

    public void setStepInstances(List<WorkflowStepInstance> stepInstances) {
        this.stepInstances = stepInstances;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof WorkflowInstance)) return false;
        return Objects.equals(id, ((WorkflowInstance)o).id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
