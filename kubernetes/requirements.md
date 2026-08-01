# Requirements Specification: Ephemeral Environment Operator (`EphemeralEnv`)

## 1. Project Overview & Objective
Build a Kubernetes Operator written in Go using **Kubebuilder** / **controller-runtime** that manages the lifecycle of dynamic, short-lived development/testing environments (`EphemeralEnv` Custom Resources). 

The operator must run locally on a **Minikube** cluster and execute an automated Reconciliation Loop that handles provisioning, TTL (Time-To-Live) tracking, scheduled cleanup, and garbage collection of child resources.

---

## 2. Technical Stack & Dependencies

* **Language:** Go `1.22+`
* **Operator Framework:** `Kubebuilder` (v3+ / v4+) or `Operator-SDK` with `controller-runtime`
* **Target Cluster:** Minikube (Kubernetes `1.28+`)
* **API Extension Mechanism:** Custom Resource Definition (CRD) v1

---

## 3. Custom Resource Definition (CRD) Specification

* **Group:** `apps.myrepo.dev`
* **Version:** `v1alpha1`
* **Kind:** `EphemeralEnv`
* **Scope:** Namespaced

### 3.1 `Spec` Schema Fields
The operator must accept the following fields in `spec`:

| Field Name | Type | Validation / Constraints | Description |
| :--- | :--- | :--- | :--- |
| `image` | `string` | Required, Non-empty | The container image to run (e.g., `nginx:alpine`). |
| `port` | `int32` | Required, Min: `1`, Max: `65535` | Container port on which the workload listens. |
| `durationMinutes` | `int32` | Required, Min: `1`, Max: `1440` | Lifetime of the environment in minutes before deletion. |
| `replicas` | `*int32` | Optional, Default: `1`, Min: `1` | Desired replica count for the underlying workload deployment. |

### 3.2 `Status` Subresource Fields
The operator must update and maintain the following fields in `status`:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `expiresAt` | `metav1.Time` | Timestamp calculated at creation time indicating when the environment expires (`Creation/Initialization Time + durationMinutes`). |
| `phase` | `string` | Current lifecycle phase: `Initializing`, `Active`, or `Expired`. |
| `readyReplicas` | `int32` | Number of ready pods reported by the underlying Deployment. |
| `serviceURL` | `string` | Cluster-internal endpoint string (e.g., `http://<service-name>.<namespace>.svc.cluster.local:<port>`). |

---

## 4. Reconciliation Logic & Controller Requirements

The controller's `Reconcile(ctx context.Context, req ctrl.Request)` function must implement the following state transitions and operations idempotently:

### 4.1 Phase 1: Initialization & Expiration Calculation
1. Fetch the `EphemeralEnv` instance using the client. If not found, return `ctrl.Result{}, nil` (ignore not found).
2. Check if `status.expiresAt` is zero/empty:
   * Calculate `expiresAt = time.Now() + spec.durationMinutes`.
   * Set `status.phase = "Initializing"`.
   * Update the status subresource using `r.Status().Update()`.

### 4.2 Phase 2: Expiration Check & Cleanup Execution
1. Compare `time.Now()` against `status.expiresAt.Time`.
2. **If expired (`time.Now() >= status.expiresAt`):**
   * Log an informational message indicating TTL expiration.
   * Delete the `EphemeralEnv` CR instance via `r.Delete()`.
   * Rely on Kubernetes garbage collection (`OwnerReferences`) to remove child Deployments and Services automatically.
   * Return `ctrl.Result{}, nil`.

### 4.3 Phase 3: Child Resource Management (Deployments & Services)
If not expired:
1. **Deployment Management:**
   * Ensure a Deployment named `<cr-name>-deploy` exists in the CR's namespace.
   * Configure pod specs using `spec.image`, `spec.port`, and `spec.replicas`.
   * Use `controllerutil.SetControllerReference` to attach the `EphemeralEnv` CR as the owner.
   * Use `controllerutil.CreateOrUpdate` to keep the deployment synchronized.
2. **Service Management:**
   * Ensure a ClusterIP Service named `<cr-name>-svc` exists in the CR's namespace matching pod labels (`app: <cr-name>`).
   * Map service port and target port to `spec.port`.
   * Attach `OwnerReference` to the Service object.

### 4.4 Phase 4: Status Updates & Scheduled Requeue
1. Read the readiness state of the managed Deployment and set `status.readyReplicas`.
2. Update `status.serviceURL` with the internal DNS string.
3. Set `status.phase = "Active"`.
4. Update `r.Status().Update()`.
5. Compute remaining duration: `remaining = status.expiresAt.Time - time.Now()`.
6. Return `ctrl.Result{RequeueAfter: remaining}` to force the controller to wake up precisely when the TTL expires.

---

## 5. RBAC Annotations & Controller Event Watches

* **RBAC Markers:** Define standard Kubebuilder markers for:
  * `apps.myrepo.dev` (EphemeralEnv, EphemeralEnv/status)
  * `apps` (Deployments)
  * `core` (Services, Events)
* **Manager Setup (`SetupWithManager`):** Configure the builder to watch `EphemeralEnv` primary resources and **Own** secondary resources (`appsv1.Deployment`, `corev1.Service`).

---

## 6. Project Structure & Deliverables

The generated project repository must follow standard Kubebuilder layout:

```text
.
├── Makefile                     # Standard targets: build, install, run, test, manifests
├── PROJECT                      # Kubebuilder metadata project file
├── README.md                    # Architecture documentation & quickstart guide
├── api/
│   └── v1alpha1/
│       ├── ephemeralenv_types.go # Go struct definitions with validation markers
│       └── groupversion_info.go
├── config/                      # Kustomize manifests for CRDs, RBAC, and Manager
│   └── crd/
├── internal/
│   └── controller/
│       ├── ephemeralenv_controller.go     # Core reconcile loop
│       └── ephemeralenv_controller_test.go# Unit / Envtest suite
├── main.go                      # Controller Manager bootstrap script
└── go.mod
```

---

## 7. Verification & Acceptance Criteria

When executed against Minikube, the code generated by Claude CLI must satisfy:

1. **`make install`** successfully registers the `EphemeralEnv` CRD in the cluster.
2. **`make run`** runs the controller locally connected to Minikube without panics or missing RBAC errors.
3. Applying a sample CR (`kubectl apply -f sample.yaml`) creates:
   * 1 `EphemeralEnv` instance with `status.expiresAt` set.
   * 1 corresponding Deployment running the specified container image.
   * 1 corresponding ClusterIP Service.
4. Setting `durationMinutes: 2` causes all three resources (`EphemeralEnv`, Deployment, Service) to automatically disappear after 2 minutes without human intervention.
