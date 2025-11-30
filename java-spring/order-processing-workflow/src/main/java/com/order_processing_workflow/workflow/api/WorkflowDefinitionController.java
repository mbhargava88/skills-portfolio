package com.order_processing_workflow.workflow.api;

import com.order_processing_workflow.workflow.application.WorkflowDefinitionServiceImpl;
import com.order_processing_workflow.workflow.domain.WorkflowDefinition;
import com.order_processing_workflow.workflow.domain.WorkflowStepDefinitionMapping;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/workflow/definitions")
public class WorkflowDefinitionController {

    private final WorkflowDefinitionServiceImpl service;

    public WorkflowDefinitionController(WorkflowDefinitionServiceImpl service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<WorkflowDefinition> createWorkflow(@RequestBody WorkflowDefinitionRequest request) {
        WorkflowDefinition workflow = service.createWorkflow(request.getName(), request.getEntityType(), request.getStepIdsInSequence());
        return ResponseEntity.ok(workflow);
    }

    @GetMapping
    public ResponseEntity<List<WorkflowDefinition>> getAllWorkflows() {
        return ResponseEntity.ok(service.getAllWorkflows());
    }

    @GetMapping("/{id}/steps")
    public ResponseEntity<List<WorkflowStepDefinitionMapping>> getWorkflowSteps(@PathVariable Long id) {
        return ResponseEntity.ok(service.getWorkflowSteps(id));
    }

    public static class WorkflowDefinitionRequest {
        private String name;
        private String entityType;
        private List<Long> stepIdsInSequence;

        // getters & setters
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getEntityType() { return entityType; }
        public void setEntityType(String entityType) { this.entityType = entityType; }
        public List<Long> getStepIdsInSequence() { return stepIdsInSequence; }
        public void setStepIdsInSequence(List<Long> stepIdsInSequence) { this.stepIdsInSequence = stepIdsInSequence; }
    }
}
