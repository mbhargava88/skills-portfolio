package com.order_processing_workflow.workflow.api;

import com.order_processing_workflow.workflow.application.WorkflowStepDefinitionServiceImpl;
import com.order_processing_workflow.workflow.domain.WorkflowStepDefinition;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/workflow/steps")
public class WorkflowStepDefinitionController {

    private final WorkflowStepDefinitionServiceImpl service;

    public WorkflowStepDefinitionController(WorkflowStepDefinitionServiceImpl service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<WorkflowStepDefinition> createStep(@RequestBody WorkflowStepRequest request) {
        WorkflowStepDefinition step = service.createStep(request.getName(), request.getCodeHandler(), request.getDescription());
        return ResponseEntity.ok(step);
    }

    @GetMapping
    public ResponseEntity<List<WorkflowStepDefinition>> getAllSteps() {
        return ResponseEntity.ok(service.getAllSteps());
    }

    public static class WorkflowStepRequest {
        private String name;
        private String codeHandler;
        private String description;

        // getters & setters
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getCodeHandler() { return codeHandler; }
        public void setCodeHandler(String codeHandler) { this.codeHandler = codeHandler; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
    }
}
