package domain

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUser_HashPassword(t *testing.T) {
	user := &User{Password: "password"}
	err := user.HashPassword()
	assert.NoError(t, err)
	assert.NotEqual(t, "password", user.Password)
}

func TestUser_CheckPassword(t *testing.T) {
	user := &User{Password: "password"}
	user.HashPassword()

	assert.True(t, user.CheckPassword("password"))
	assert.False(t, user.CheckPassword("wrongpassword"))
}
