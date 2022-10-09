package usecase

import (
	"github.com/golang-jwt/jwt"
)

type Claims struct {
	jwt.StandardClaims
	Username string `json:"username"`
	Role     string `json:"role"`
}
