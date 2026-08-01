# EphemeralEnv Operator

A Kubernetes Operator, built with [Kubebuilder](https://book.kubebuilder.io/) and
[controller-runtime](https://github.com/kubernetes-sigs/controller-runtime), that manages the
full lifecycle of short-lived development/test environments through a custom resource:
`EphemeralEnv`.

Apply an `EphemeralEnv` with a container image, a port, and a TTL — the operator provisions a
`Deployment` and a `ClusterIP` `Service` for it, tracks the expiry, and tears everything down
automatically once the TTL elapses. No cron jobs, no manual cleanup.

## Architecture

```
                       ┌─────────────────────┐
   kubectl apply  ───► │  EphemeralEnv (CR)   │
                       └──────────┬───────────┘
                                  │ watched by
                                  ▼
                       ┌─────────────────────┐
                       │ EphemeralEnvReconciler│
                       │ (internal/controller) │
                       └──────────┬───────────┘
              ┌───────────────────┼───────────────────┐
              │ owns              │ owns              │ requeues at
              ▼                   ▼                   │ status.expiresAt
   ┌─────────────────┐  ┌──────────────────┐           │
   │ Deployment       │  │ Service          │◄──────────┘
   │ <name>-deploy    │  │ <name>-svc       │
   └─────────────────┘  └──────────────────┘
```

The Deployment and Service are owned by the `EphemeralEnv` CR via `OwnerReferences`
(`controllerutil.SetControllerReference`), so deleting the CR is enough to garbage-collect both
children — the operator itself never has to delete them directly.

### Reconcile loop

Each call to `Reconcile` runs through four phases:

1. **Initialization** — on first sight of a CR, compute `status.expiresAt = creationTimestamp +
   spec.durationMinutes` and set `status.phase = Initializing`.
2. **Expiration check** — if `time.Now() >= status.expiresAt`, delete the CR and return. Owner
   references handle cleanup of the Deployment/Service.
3. **Child reconciliation** — otherwise, `controllerutil.CreateOrUpdate` a Deployment (running
   `spec.image` on `spec.port`, sized to `spec.replicas`) and a ClusterIP Service in front of it.
4. **Status + scheduled requeue** — copy the Deployment's `readyReplicas` and the Service's
   internal DNS name into `status`, set `phase = Active`, and requeue with
   `RequeueAfter: status.expiresAt - time.Now()` so the controller wakes up exactly at the TTL
   boundary instead of polling.

### CRD reference

**`apps.myrepo.dev/v1alpha1`, Kind: `EphemeralEnv`** (namespaced)

`spec`:

| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `image` | `string` | required, non-empty | Container image to run (e.g. `nginx:alpine`) |
| `port` | `int32` | required, 1–65535 | Container port the workload listens on |
| `durationMinutes` | `int32` | required, 1–1440 | Lifetime in minutes before automatic deletion |
| `replicas` | `*int32` | optional, default `1`, min `1` | Desired replica count |

`status`:

| Field | Type | Description |
| :--- | :--- | :--- |
| `expiresAt` | `metav1.Time` | Computed at creation: `creationTimestamp + durationMinutes` |
| `phase` | `string` | `Initializing`, `Active`, or `Expired` |
| `readyReplicas` | `int32` | Ready pods reported by the managed Deployment |
| `serviceURL` | `string` | `http://<name>-svc.<namespace>.svc.cluster.local:<port>` |

## Prerequisites

Everything below is installed and configured automatically by `make setup` on macOS. Manual
prerequisites, if you'd rather not use Homebrew:

- [Go](https://go.dev/) 1.22+
- [Docker](https://www.docker.com/)
- [Minikube](https://minikube.sigs.k8s.io/docs/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Quickstart

```bash
# 1. Install prerequisites (via brew, if missing) and start Minikube.
make setup

# 2. Register the CRD and RBAC, then run the controller locally
#    (talks to Minikube via your kubeconfig, no in-cluster image needed).
make install
make run
```

In a second terminal, apply a sample environment:

```bash
kubectl apply -f config/samples/apps_v1alpha1_ephemeralenv.yaml

kubectl get ephemeralenv
# NAME                  PHASE    IMAGE          EXPIRES AT             READY
# ephemeralenv-sample   Active   nginx:alpine   2026-08-01T09:22:47Z   1

kubectl get deployment,service
```

To see the full TTL-driven lifecycle in a couple of minutes rather than an hour, use the
short-lived sample (`durationMinutes: 2`) via the bundled demo target:

```bash
make demo
```

This applies `config/samples/apps_v1alpha1_ephemeralenv_shortlived.yaml` and watches the CR,
Deployment, and Service — all three disappear on their own once the 2-minute TTL elapses.

### Running the test suite

```bash
make test
```

This runs the [envtest](https://book.kubebuilder.io/reference/envtest)-based Ginkgo suite in
`internal/controller`, which spins up a real (binary-only, no Docker) API server + etcd and
exercises the reconciler's three phases: initialization, child-resource creation, and
TTL-driven deletion.

### Cleaning up

```bash
kubectl delete -f config/samples/ --ignore-not-found
make uninstall        # remove the CRD
minikube stop          # optional: stop the cluster entirely
```

## Project layout

Standard Kubebuilder v4 layout:

```
.
├── api/v1alpha1/                      # EphemeralEnv CRD Go types + generated deepcopy
├── cmd/main.go                        # Controller manager entrypoint
├── config/                            # Kustomize manifests: CRD, RBAC, manager, samples
├── internal/controller/                # Reconciler + envtest-based test suite
├── Makefile                           # setup/build/test/deploy targets (see `make help`)
└── PROJECT                            # Kubebuilder project metadata
```

## Notes on tool versions

This project bumps a couple of Kubebuilder v4's default scaffolded tool versions in the
`Makefile` beyond what `kubebuilder init` pins, to work with current Go toolchains:

- `CONTROLLER_TOOLS_VERSION` → `v0.16.5` (the default `v0.15.0` pulls in a `golang.org/x/tools`
  version that fails to compile under Go 1.23+).
- `ENVTEST_VERSION` → `v0.24.1` (the default `release-0.18` fetches envtest binaries from a GCS
  bucket that now returns 403/401; newer `setup-envtest` releases pull from the maintained
  `kubebuilder-envtest-binaries` source instead).

## License

Copyright 2026.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
