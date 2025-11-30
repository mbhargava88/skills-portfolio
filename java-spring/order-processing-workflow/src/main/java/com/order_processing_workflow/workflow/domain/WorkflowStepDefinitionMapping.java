package com.order_processing_workflow.workflow.domain;

import jakarta.persistence.*;
import java.util.Objects;

@Entity
@Table(name = "workflow_step_definition_mapping")
public class WorkflowStepDefinitionMapping {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "workflow_definition_id")
    private WorkflowDefinition workflowDefinition;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "step_definition_id")
    private WorkflowStepDefinition stepDefinition;

    private int sequenceOrder; // Step order within workflow

    // Constructors
    public WorkflowStepDefinitionMapping() {}
    public WorkflowStepDefinitionMapping(WorkflowDefinition workflowDefinition,
                                         WorkflowStepDefinition stepDefinition,
                                         int sequenceOrder) {
        this.workflowDefinition = workflowDefinition;
        this.stepDefinition = stepDefinition;
        this.sequenceOrder = sequenceOrder;
    }

    // Getters & Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public WorkflowDefinition getWorkflowDefinition() { return workflowDefinition; }
    public void setWorkflowDefinition(WorkflowDefinition workflowDefinition) {
        this.workflowDefinition = workflowDefinition;
    }

    public WorkflowStepDefinition getStepDefinition() { return stepDefinition; }
    public void setStepDefinition(WorkflowStepDefinition stepDefinition) {
        this.stepDefinition = stepDefinition;
    }

    public int getSequenceOrder() { return sequenceOrder; }
    public void setSequenceOrder(int sequenceOrder) { this.sequenceOrder = sequenceOrder; }

    // Equals & HashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof WorkflowStepDefinitionMapping)) return false;
        WorkflowStepDefinitionMapping that = (WorkflowStepDefinitionMapping) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
