package com.order_processing_workflow.workflow.domain;

import jakarta.persistence.*;
import java.util.Objects;

@Entity
@Table(name = "workflow_step_definitions")
public class WorkflowStepDefinition {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;             // e.g., "Validate Order"
    private String codeHandler;      // e.g., "com.app.workflow.steps.ValidateOrderHandler"
    private String description;

    @Column(name = "parallel_group")
    private String parallelGroup;    // Steps in same group can execute in parallel

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "depends_on_step_id")
    private WorkflowStepDefinition dependsOn; // Step this one depends on

    // Constructors
    public WorkflowStepDefinition() {}

    public WorkflowStepDefinition(String name, String codeHandler, String description) {
        this.name = name;
        this.codeHandler = codeHandler;
        this.description = description;
    }

    // Getters & Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getCodeHandler() { return codeHandler; }
    public void setCodeHandler(String codeHandler) { this.codeHandler = codeHandler; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getParallelGroup() { return parallelGroup; }
    public void setParallelGroup(String parallelGroup) { this.parallelGroup = parallelGroup; }

    public WorkflowStepDefinition getDependsOn() { return dependsOn; }
    public void setDependsOn(WorkflowStepDefinition dependsOn) { this.dependsOn = dependsOn; }

    // Equals & HashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof WorkflowStepDefinition)) return false;
        WorkflowStepDefinition that = (WorkflowStepDefinition) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
