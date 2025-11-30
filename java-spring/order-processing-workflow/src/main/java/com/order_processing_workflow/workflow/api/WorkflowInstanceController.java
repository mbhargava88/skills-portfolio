package com.order_processing_workflow.workflow.api;

import com.order_processing_workflow.workflow.application.WorkflowInstanceService;
import com.order_processing_workflow.workflow.domain.WorkflowInstance;
import com.order_processing_workflow.workflow.domain.WorkflowStepInstance;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/workflow/instances")
public class WorkflowInstanceController {

    private final WorkflowInstanceService workflowInstanceService;

    public WorkflowInstanceController(WorkflowInstanceService workflowInstanceService) {
        this.workflowInstanceService = workflowInstanceService;
    }

    /**
     * Start a new workflow instance for a specific entity
     */
    @PostMapping("/start")
    public ResponseEntity<WorkflowInstance> startWorkflow(
            @RequestParam Long workflowDefinitionId,
            @RequestParam String entityType,
            @RequestParam Long entityId) {

        WorkflowInstance instance = workflowInstanceService.startWorkflow(workflowDefinitionId, entityType, entityId);
        return ResponseEntity.ok(instance);
    }

    /**
     * Get all workflow instances for a specific entity
     */
    @GetMapping
    public ResponseEntity<List<WorkflowInstance>> getInstances(
            @RequestParam String entityType,
            @RequestParam Long entityId) {

        return null;
       // return ResponseEntity.ok(workflowInstanceService.getWorkflowInstances(entityType, entityId));
    }

    /**
     * Get all step instances for a workflow instance
     */
    @GetMapping("/{workflowInstanceId}/steps")
    public ResponseEntity<List<WorkflowStepInstance>> getStepInstances(@PathVariable Long workflowInstanceId) {
        return null;
        // return ResponseEntity.ok(workflowInstanceService.getWorkflowStepInstances(workflowInstanceId));
    }

    /**
     * Mark a workflow step as completed
     */
    @PostMapping("/{workflowInstanceId}/steps/{stepInstanceId}/complete")
    public ResponseEntity<String> completeStep(
            @PathVariable Long workflowInstanceId,
            @PathVariable Long stepInstanceId) {
        return null;
        // workflowInstanceService.completeStep(workflowInstanceId, stepInstanceId);
        // return ResponseEntity.ok("Step marked as completed.");
    }
}
