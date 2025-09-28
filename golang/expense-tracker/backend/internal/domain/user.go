package domain

import (
	"time"

	"golang.org/x/crypto/bcrypt"
)

// User represents a user in the system.

type User struct {
	ID        string    `json:"id"`
	Username  string    `json:"username"`
	Password  string    `json:"-" db:"password"`
	CreatedAt time.Time `json:"created_at"`
}

// HashPassword hashes the user's password.
func (u *User) HashPassword() error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	u.Password = string(hashedPassword)
	return nil
}

// CheckPassword checks if the provided password is correct.
func (u *User) CheckPassword(password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.Password), []byte(password))
	return err == nil
}

// UserRepository defines the interface for user persistence.

type UserRepository interface {
	Create(user *User) error
	GetByUsername(username string) (*User, error)
	GetByID(id string) (*User, error)
}
