# Skills Portfolio

This monorepo contains a collection of projects demonstrating my expertise in **AI Engineering**, **Golang**, **Java/Spring**, and **Python**. I focus on building production-ready applications with Clean Architecture, Domain-Driven Design (DDD), and modern infrastructure.

## 🤖 AI & Python Projects

| Project | Description | Stack |
|---------|-------------|-------|
| **[SmartCart AI](ai/smartcart-ai)** | LLM-powered product recommendation engine. Uses accumulated user history and cart context to reason and explain recommendations. | Python, Clean Arch, DDD, Groq, Vector Store (RAG) |
| **[RAG MCP Server](python/mcp/mcp-rag)** | A Model Context Protocol (MCP) server for RAG. Enables AI agents to perform semantic search and retrieval on custom data. | Python, fastmcp, Groq, HuggingFace, FAISS |
| **[Agentic Chatbot](python/agentic-chatbot)** | An end-to-end agentic AI chatbot. | Python, AI Agents |

## 🐹 Golang Projects

| Project | Description | Stack |
|---------|-------------|-------|
| **[Catalog Service](golang/catalog-service-grpc-http)** | Robust CRUD application for managing products. Supports dual interfaces (HTTP & gRPC) with a focus on Clean Architecture. | Go, gRPC, REST, DDD, PostgreSQL, Docker, K8s |
| **[Expense Tracker](golang/expense-tracker)** | Full-stack expense tracking application with authentication and reporting. | React, Go, PostgreSQL, JWT Auth, Docker |

## 🍃 Java & Spring Projects

| Project | Description | Stack |
|---------|-------------|-------|
| **[Order Processing Workflow](java-spring/order-processing-workflow)** | Microservice to manage complex order processing workflows using a Directed Acyclic Graph (DAG) approach. | Spring Boot, PostgreSQL, Docker, Flyway |
| **[Spring REST](java/spring-rest)** | Standard REST API implementation demonstrating Spring Boot fundamentals. | Spring Boot, REST |

## ⚓ Kubernetes

| Project | Description | Stack |
|---------|-------------|-------|
| **[EphemeralEnv Operator](kubernetes/ephemeral-env-operator)** | Kubebuilder operator managing TTL-bound `EphemeralEnv` custom resources — provisions a Deployment + ClusterIP Service per CR and auto-tears them down once the TTL expires. | Go, Kubebuilder, controller-runtime, Minikube, CRDs |

More Kubernetes projects are in progress — see the [kubernetes](kubernetes) folder.

