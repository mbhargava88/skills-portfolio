package com.order_processing_workflow.workflow.domain;

import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@Entity
@Table(name = "workflow_definitions")
public class WorkflowDefinition {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;        // e.g., "OrderProcessing"
    private String entityType;  // e.g., "ORDER" or "DELIVERY"

    @OneToMany(mappedBy = "workflowDefinition", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<WorkflowStepDefinitionMapping> steps = new ArrayList<>();

    // Constructors
    public WorkflowDefinition() {}
    public WorkflowDefinition(String name, String entityType) {
        this.name = name;
        this.entityType = entityType;
    }

    // Getters & Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEntityType() { return entityType; }
    public void setEntityType(String entityType) { this.entityType = entityType; }

    public List<WorkflowStepDefinitionMapping> getSteps() { return steps; }
    public void setSteps(List<WorkflowStepDefinitionMapping> steps) { this.steps = steps; }

    public void addStepMapping(WorkflowStepDefinitionMapping mapping) {
        steps.add(mapping);
        mapping.setWorkflowDefinition(this);
    }

    public void removeStepMapping(WorkflowStepDefinitionMapping mapping) {
        steps.remove(mapping);
        mapping.setWorkflowDefinition(null);
    }

    // Equals & HashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof WorkflowDefinition)) return false;
        WorkflowDefinition that = (WorkflowDefinition) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
