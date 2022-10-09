package repo

import "errors"

var (
	ErrUserNotFound      = errors.New("user not found")
	ErrUserAlreadyExists = errors.New("user already exists")
)

type Repository interface {
	GetUser(username string) (*User, error)
	AddUser(user *User) error
}
