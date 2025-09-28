package application

import (
	"errors"
	"expense-tracker/backend/internal/domain"
	"log"

	"github.com/google/uuid"
)

// AuthService provides user authentication services.

type AuthService struct {
	userRepo domain.UserRepository
}

// NewAuthService creates a new AuthService.
func NewAuthService(userRepo domain.UserRepository) *AuthService {
	return &AuthService{userRepo: userRepo}
}

// Register registers a new user.
func (s *AuthService) Register(username, password string) (*domain.User, error) {
	user, err := s.userRepo.GetByUsername(username)
	if err == nil && user != nil {
		return nil, errors.New("user already exists")
	}

	newUser := &domain.User{
		ID:       uuid.New().String(),
		Username: username,
		Password: password,
	}

	if err := newUser.HashPassword(); err != nil {
		return nil, err
	}

	if err := s.userRepo.Create(newUser); err != nil {
		return nil, err
	}

	return newUser, nil
}

// Login logs in a user.
func (s *AuthService) Login(username, password string) (*domain.User, error) {
	user, err := s.userRepo.GetByUsername(username)
	if err != nil {
		return nil, err
	}

	// --- DIAGNOSTIC LOG ---
	log.Printf("Retrieved user for login: %+v\n", user)
	// ----------------------

	if !user.CheckPassword(password) {
		return nil, errors.New("invalid password")
	}

	return user, nil
}
