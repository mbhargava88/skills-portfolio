/*
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
*/

package controller

import (
	"context"
	"fmt"
	"time"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/apimachinery/pkg/util/intstr"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/log"

	appsv1alpha1 "github.com/mbhargava88/ephemeral-env-operator/api/v1alpha1"
)

// minRequeueInterval guards against a zero/negative RequeueAfter being handed
// to controller-runtime when an environment is found to be already past due.
const minRequeueInterval = 5 * time.Second

// EphemeralEnvReconciler reconciles a EphemeralEnv object
type EphemeralEnvReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=apps.myrepo.dev,resources=ephemeralenvs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps.myrepo.dev,resources=ephemeralenvs/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps.myrepo.dev,resources=ephemeralenvs/finalizers,verbs=update
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=events,verbs=create;patch

// Reconcile drives an EphemeralEnv through its lifecycle: it stamps an
// expiry time on first sight, deletes the CR once that TTL has passed
// (letting owner-reference garbage collection remove the child Deployment
// and Service), and otherwise keeps the child Deployment/Service in sync
// and requeues itself to wake up exactly at expiry time.
func (r *EphemeralEnvReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	// Phase 1: fetch the EphemeralEnv instance.
	var env appsv1alpha1.EphemeralEnv
	if err := r.Get(ctx, req.NamespacedName, &env); err != nil {
		return ctrl.Result{}, client.IgnoreNotFound(err)
	}

	// Phase 1: initialize expiresAt/phase on first reconcile.
	if env.Status.ExpiresAt.IsZero() {
		env.Status.ExpiresAt = metav1.NewTime(env.CreationTimestamp.Time.Add(time.Duration(env.Spec.DurationMinutes) * time.Minute))
		env.Status.Phase = string(appsv1alpha1.PhaseInitializing)
		if err := r.Status().Update(ctx, &env); err != nil {
			return ctrl.Result{}, fmt.Errorf("updating initial status: %w", err)
		}
		return ctrl.Result{Requeue: true}, nil
	}

	// Phase 2: expiration check and cleanup.
	if !time.Now().Before(env.Status.ExpiresAt.Time) {
		logger.Info("EphemeralEnv TTL expired, deleting", "name", env.Name, "expiresAt", env.Status.ExpiresAt.Time)
		if err := r.Delete(ctx, &env); err != nil {
			return ctrl.Result{}, client.IgnoreNotFound(err)
		}
		return ctrl.Result{}, nil
	}

	// Phase 3: reconcile the child Deployment and Service.
	if err := r.reconcileDeployment(ctx, &env); err != nil {
		return ctrl.Result{}, fmt.Errorf("reconciling deployment: %w", err)
	}
	if err := r.reconcileService(ctx, &env); err != nil {
		return ctrl.Result{}, fmt.Errorf("reconciling service: %w", err)
	}

	// Phase 4: refresh status and requeue at the exact TTL expiry.
	var deploy appsv1.Deployment
	if err := r.Get(ctx, types.NamespacedName{Name: deploymentName(&env), Namespace: env.Namespace}, &deploy); err != nil {
		return ctrl.Result{}, fmt.Errorf("fetching deployment for status: %w", err)
	}

	env.Status.ReadyReplicas = deploy.Status.ReadyReplicas
	env.Status.ServiceURL = fmt.Sprintf("http://%s.%s.svc.cluster.local:%d", serviceName(&env), env.Namespace, env.Spec.Port)
	env.Status.Phase = string(appsv1alpha1.PhaseActive)
	if err := r.Status().Update(ctx, &env); err != nil {
		return ctrl.Result{}, fmt.Errorf("updating status: %w", err)
	}

	remaining := max(time.Until(env.Status.ExpiresAt.Time), minRequeueInterval)
	return ctrl.Result{RequeueAfter: remaining}, nil
}

func deploymentName(env *appsv1alpha1.EphemeralEnv) string {
	return env.Name + "-deploy"
}

func serviceName(env *appsv1alpha1.EphemeralEnv) string {
	return env.Name + "-svc"
}

func podLabels(env *appsv1alpha1.EphemeralEnv) map[string]string {
	return map[string]string{"app": env.Name}
}

// reconcileDeployment ensures the workload Deployment for env exists and
// matches spec.image/spec.port/spec.replicas.
func (r *EphemeralEnvReconciler) reconcileDeployment(ctx context.Context, env *appsv1alpha1.EphemeralEnv) error {
	replicas := int32(1)
	if env.Spec.Replicas != nil {
		replicas = *env.Spec.Replicas
	}

	deploy := &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      deploymentName(env),
			Namespace: env.Namespace,
		},
	}

	_, err := controllerutil.CreateOrUpdate(ctx, r.Client, deploy, func() error {
		labels := podLabels(env)
		deploy.Spec.Replicas = &replicas
		deploy.Spec.Selector = &metav1.LabelSelector{MatchLabels: labels}
		deploy.Spec.Template = corev1.PodTemplateSpec{
			ObjectMeta: metav1.ObjectMeta{Labels: labels},
			Spec: corev1.PodSpec{
				Containers: []corev1.Container{
					{
						Name:  "workload",
						Image: env.Spec.Image,
						Ports: []corev1.ContainerPort{
							{ContainerPort: env.Spec.Port},
						},
					},
				},
			},
		}
		return controllerutil.SetControllerReference(env, deploy, r.Scheme)
	})
	return err
}

// reconcileService ensures a ClusterIP Service exists, routing spec.port to
// the pods managed by the Deployment above.
func (r *EphemeralEnvReconciler) reconcileService(ctx context.Context, env *appsv1alpha1.EphemeralEnv) error {
	svc := &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name:      serviceName(env),
			Namespace: env.Namespace,
		},
	}

	_, err := controllerutil.CreateOrUpdate(ctx, r.Client, svc, func() error {
		svc.Spec.Type = corev1.ServiceTypeClusterIP
		svc.Spec.Selector = podLabels(env)
		svc.Spec.Ports = []corev1.ServicePort{
			{
				Port:       env.Spec.Port,
				TargetPort: intstr.FromInt32(env.Spec.Port),
			},
		}
		return controllerutil.SetControllerReference(env, svc, r.Scheme)
	})
	return err
}

// SetupWithManager sets up the controller with the Manager.
func (r *EphemeralEnvReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&appsv1alpha1.EphemeralEnv{}).
		Owns(&appsv1.Deployment{}).
		Owns(&corev1.Service{}).
		Complete(r)
}
