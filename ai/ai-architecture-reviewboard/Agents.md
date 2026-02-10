# AI Architecture Review Board – Agents Specification

This document defines the agent roles, responsibilities, prompts, and StateGraph orchestration for the **AI Architecture Review Board** project.

Tech Stack:

* Python
* LangChain
* LangGraph (StateGraph)
* Groq LLMs
* Clean Architecture

---

## 1. System Overview

The system simulates a real-world architecture design review meeting using two autonomous LLM agents:

1. **Principal Architect Agent** – Proposes and iteratively refines system architecture.
2. **Chief Reviewer Agent** – Critically evaluates the design for scalability, security, cost, reliability, and observability.

They engage in a structured feedback loop until convergence or a quality threshold is met.

---

## 2. Agent Roles

### 2.1 Principal Architect Agent

**Responsibility**:

* Generate an initial high-level and low-level architecture.
* Refine the design based on review feedback.
* Justify design trade-offs.

**Persona**:
Senior Staff+ Engineer with expertise in:

* Distributed Systems
* Kubernetes
* Observability (OpenTelemetry, Prometheus, Grafana)
* CI/CD and Load Testing

**Prompt Template (Simplified)**:

```
You are a Principal Software Architect.
Design a production-grade system for the following problem:

{problem_statement}

Constraints:
- Cloud native
- Secure by design
- Cost efficient
- Observable (metrics, logs, traces)

Output:
- Architecture overview
- Component diagram (text)
- Data flow
- Technology choices
- Key trade-offs
```

---

### 2.2 Chief Reviewer Agent

**Responsibility**:

* Perform adversarial review of the architecture.
* Identify gaps in:

  * Scalability
  * Fault tolerance
  * Security
  * Cost
  * SLOs
  * Operational readiness
* Assign a readiness score.

**Persona**:
Ex-Principal SRE / Cloud Security Architect.

**Prompt Template (Simplified)**:

```
You are a Chief Architecture Reviewer.
Review the following architecture critically:

{architecture_proposal}

Evaluate on:
1. Scalability
2. Resilience
3. Security
4. Cost efficiency
5. Observability
6. Maintainability

Provide:
- Top risks
- Missing components
- Concrete improvement suggestions
- Readiness score (0-100)
```

---

## 3. Feedback Loop Strategy

The system uses LangGraph StateGraph to model iterative debate.

### State

```python
class ReviewState(TypedDict):
    problem: str
    proposal: str
    critique: str
    score: int
    iteration: int
    final_architecture: str
```

### Flow

```
User Input
   ↓
Architect Agent (propose)
   ↓
Reviewer Agent (critique + score)
   ↓
Decision Node
   ├─ if score < threshold → Architect Refines
   └─ if score >= threshold → Final Verdict
```

Stopping conditions:

* Score >= 85
* Or max_iterations = 3

---

## 4. StateGraph Nodes

### 4.1 propose_architecture

Calls Architect Agent.

### 4.2 review_architecture

Calls Reviewer Agent.

### 4.3 decide_next_step

```python
def should_continue(state: ReviewState) -> str:
    if state["score"] >= 85 or state["iteration"] >= 3:
        return "finalize"
    return "refine"
```

### 4.4 finalize

Produces:

* Final architecture
* Risk register
* Readiness score

---

## 5. Clean Architecture Mapping

```
/ai-architecture-review
  /domain
    entities.py        # ReviewState, Score, Risk
    interfaces.py     # LLMPort, AgentPort

  /application
    usecases/
      run_review.py   # Orchestrates StateGraph
    agents/
      architect.py
      reviewer.py

  /infrastructure
    llm/
      groq_client.py
    graph/
      state_graph.py

  /interfaces
    api.py            # FastAPI / Streamlit
    cli.py
```

---

## 6. Groq LLM Configuration

* Model: `llama-3.1-70b` or `mixtral-8x7b`
* Temperature:

  * Architect: 0.6 (creative)
  * Reviewer: 0.2 (strict)

---

## 7. Future Extension (Optional)

* Add a **CTO Judge Agent** for arbitration.
* Add **Cost Estimator Tool Agent** using pricing APIs.
* Add **Diagram Generator Agent** (Mermaid / PlantUML).

---

## 8. Hackathon Pitch Line

> "An autonomous multi-agent architecture review board that debates, critiques, and converges on production-ready system designs using StateGraph and Groq-powered LLMs."

