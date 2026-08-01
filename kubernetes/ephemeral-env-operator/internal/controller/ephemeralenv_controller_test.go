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
	"time"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"

	appsv1alpha1 "github.com/mbhargava88/ephemeral-env-operator/api/v1alpha1"
)

var _ = Describe("EphemeralEnv Controller", Ordered, func() {
	const resourceName = "test-resource"

	ctx := context.Background()
	typeNamespacedName := types.NamespacedName{Name: resourceName, Namespace: "default"}
	reconciler := &EphemeralEnvReconciler{}

	BeforeAll(func() {
		reconciler.Client = k8sClient
		reconciler.Scheme = k8sClient.Scheme()

		By("creating the EphemeralEnv custom resource")
		resource := &appsv1alpha1.EphemeralEnv{
			ObjectMeta: metav1.ObjectMeta{Name: resourceName, Namespace: "default"},
			Spec: appsv1alpha1.EphemeralEnvSpec{
				Image:           "nginx:alpine",
				Port:            80,
				DurationMinutes: 60,
			},
		}
		Expect(k8sClient.Create(ctx, resource)).To(Succeed())
	})

	AfterAll(func() {
		resource := &appsv1alpha1.EphemeralEnv{}
		err := k8sClient.Get(ctx, typeNamespacedName, resource)
		if err == nil {
			Expect(k8sClient.Delete(ctx, resource)).To(Succeed())
		}
	})

	It("stamps expiresAt and phase=Initializing on the first reconcile", func() {
		_, err := reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
		Expect(err).NotTo(HaveOccurred())

		var env appsv1alpha1.EphemeralEnv
		Expect(k8sClient.Get(ctx, typeNamespacedName, &env)).To(Succeed())
		Expect(env.Status.Phase).To(Equal(string(appsv1alpha1.PhaseInitializing)))
		Expect(env.Status.ExpiresAt.IsZero()).To(BeFalse())
	})

	It("creates the owned Deployment and Service and moves to phase=Active", func() {
		_, err := reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
		Expect(err).NotTo(HaveOccurred())

		var deploy appsv1.Deployment
		Expect(k8sClient.Get(ctx, types.NamespacedName{Name: resourceName + "-deploy", Namespace: "default"}, &deploy)).To(Succeed())
		Expect(deploy.Spec.Template.Spec.Containers).To(HaveLen(1))
		Expect(deploy.Spec.Template.Spec.Containers[0].Image).To(Equal("nginx:alpine"))
		Expect(deploy.OwnerReferences).To(HaveLen(1))

		var svc corev1.Service
		Expect(k8sClient.Get(ctx, types.NamespacedName{Name: resourceName + "-svc", Namespace: "default"}, &svc)).To(Succeed())
		Expect(svc.Spec.Ports).To(HaveLen(1))
		Expect(svc.Spec.Ports[0].Port).To(Equal(int32(80)))
		Expect(svc.OwnerReferences).To(HaveLen(1))

		var env appsv1alpha1.EphemeralEnv
		Expect(k8sClient.Get(ctx, typeNamespacedName, &env)).To(Succeed())
		Expect(env.Status.Phase).To(Equal(string(appsv1alpha1.PhaseActive)))
		Expect(env.Status.ServiceURL).To(Equal("http://test-resource-svc.default.svc.cluster.local:80"))
	})

	It("deletes the CR (and, via GC, its children) once the TTL has passed", func() {
		var env appsv1alpha1.EphemeralEnv
		Expect(k8sClient.Get(ctx, typeNamespacedName, &env)).To(Succeed())
		env.Status.ExpiresAt = metav1.NewTime(time.Now().Add(-time.Minute))
		Expect(k8sClient.Status().Update(ctx, &env)).To(Succeed())

		_, err := reconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
		Expect(err).NotTo(HaveOccurred())

		Eventually(func() bool {
			return errors.IsNotFound(k8sClient.Get(ctx, typeNamespacedName, &appsv1alpha1.EphemeralEnv{}))
		}).Should(BeTrue())
	})
})
