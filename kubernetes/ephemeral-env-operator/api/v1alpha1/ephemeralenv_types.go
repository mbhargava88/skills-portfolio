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

package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EphemeralEnvSpec defines the desired state of EphemeralEnv
type EphemeralEnvSpec struct {
	// Image is the container image to run (e.g., nginx:alpine).
	// +kubebuilder:validation:Required
	// +kubebuilder:validation:MinLength=1
	Image string `json:"image"`

	// Port is the container port on which the workload listens.
	// +kubebuilder:validation:Required
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:validation:Maximum=65535
	Port int32 `json:"port"`

	// DurationMinutes is the lifetime of the environment in minutes before deletion.
	// +kubebuilder:validation:Required
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:validation:Maximum=1440
	DurationMinutes int32 `json:"durationMinutes"`

	// Replicas is the desired replica count for the underlying workload deployment.
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:default=1
	// +optional
	Replicas *int32 `json:"replicas,omitempty"`
}

// EphemeralEnvPhase represents the lifecycle phase of an EphemeralEnv.
type EphemeralEnvPhase string

const (
	PhaseInitializing EphemeralEnvPhase = "Initializing"
	PhaseActive       EphemeralEnvPhase = "Active"
	PhaseExpired      EphemeralEnvPhase = "Expired"
)

// EphemeralEnvStatus defines the observed state of EphemeralEnv
type EphemeralEnvStatus struct {
	// ExpiresAt is the timestamp calculated at creation time indicating when
	// the environment expires (creation/initialization time + durationMinutes).
	// +optional
	ExpiresAt metav1.Time `json:"expiresAt,omitempty"`

	// Phase is the current lifecycle phase: Initializing, Active, or Expired.
	// +optional
	Phase string `json:"phase,omitempty"`

	// ReadyReplicas is the number of ready pods reported by the underlying Deployment.
	// +optional
	ReadyReplicas int32 `json:"readyReplicas,omitempty"`

	// ServiceURL is the cluster-internal endpoint string for the managed Service.
	// +optional
	ServiceURL string `json:"serviceURL,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:printcolumn:name="Phase",type=string,JSONPath=`.status.phase`
// +kubebuilder:printcolumn:name="Image",type=string,JSONPath=`.spec.image`
// +kubebuilder:printcolumn:name="Expires At",type=string,JSONPath=`.status.expiresAt`
// +kubebuilder:printcolumn:name="Ready",type=integer,JSONPath=`.status.readyReplicas`

// EphemeralEnv is the Schema for the ephemeralenvs API
type EphemeralEnv struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   EphemeralEnvSpec   `json:"spec,omitempty"`
	Status EphemeralEnvStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// EphemeralEnvList contains a list of EphemeralEnv
type EphemeralEnvList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []EphemeralEnv `json:"items"`
}

func init() {
	SchemeBuilder.Register(&EphemeralEnv{}, &EphemeralEnvList{})
}
