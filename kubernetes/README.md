# Kubernetes Projects

Each subfolder here is a self-contained Kubernetes use case with its own `Makefile` (runnable
end-to-end on a Mac via Minikube) and `README.md`. More projects will be added over time.

| Project | Description | Stack |
|---------|-------------|-------|
| **[EphemeralEnv Operator](ephemeral-env-operator)** | Kubebuilder operator managing TTL-bound `EphemeralEnv` custom resources — provisions a Deployment + ClusterIP Service per CR and auto-tears them down once the TTL expires. | Go, Kubebuilder, controller-runtime, Minikube, CRDs |
