package application

import (
	"expense-tracker/backend/internal/domain"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// MockUserRepository is a mock implementation of UserRepository.
type MockUserRepository struct {
	mock.Mock
}

func (m *MockUserRepository) Create(user *domain.User) error {
	args := m.Called(user)
	return args.Error(0)
}

func (m *MockUserRepository) GetByUsername(username string) (*domain.User, error) {
	args := m.Called(username)
	return args.Get(0).(*domain.User), args.Error(1)
}

func (m *MockUserRepository) GetByID(id string) (*domain.User, error) {
	args := m.Called(id)
	return args.Get(0).(*domain.User), args.Error(1)
}

func TestAuthService_Register(t *testing.T) {
	userRepo := new(MockUserRepository)
	authService := NewAuthService(userRepo)

	userRepo.On("GetByUsername", "testuser").Return(nil, nil)
	userRepo.On("Create", mock.Anything).Return(nil)

	user, err := authService.Register("testuser", "password")

	assert.NoError(t, err)
	assert.NotNil(t, user)
	userRepo.AssertExpectations(t)
}
