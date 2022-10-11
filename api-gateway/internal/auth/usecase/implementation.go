package usecase

import (
	"fmt"
	"time"

	"github.com/golang-jwt/jwt"
	"github.com/kozl/ates/api-gateway/internal/auth/events"
	"github.com/kozl/ates/api-gateway/internal/auth/repo"
)

type AuthorizerImpl struct {
	userRepo          repo.Repository
	authEventProducer events.EventProducer
	jwtSigningKey     []byte
}

func NewAuthorizer(userRepo repo.Repository, authEventProducer events.EventProducer, jwtSingingKey []byte) Authorizer {
	return &AuthorizerImpl{
		userRepo:          userRepo,
		authEventProducer: authEventProducer,
		jwtSigningKey:     jwtSingingKey}
}

func (a *AuthorizerImpl) SignIn(username, password string) (string, error) {
	user, err := a.userRepo.GetUser(username)
	if err != nil {
		return "", fmt.Errorf("can't get user: %w", err)
	}

	if user.Password != password {
		return "", fmt.Errorf("invalid password")
	}

	return jwtTokenForUser(user, a.jwtSigningKey)
}

func (a *AuthorizerImpl) SignUp(username, password, role string) (string, error) {
	user := &repo.User{
		Username: username,
		Password: password,
		Role:     role,
	}

	err := a.userRepo.AddUser(user)
	if err != nil {
		return "", fmt.Errorf("can't add user: %w", err)
	}

	err = a.authEventProducer.ProduceUserCreated(user.Username, user.Role)
	if err != nil {
		return "", fmt.Errorf("can't produce user created event: %w", err)
	}

	return jwtTokenForUser(user, a.jwtSigningKey)
}

func (a *AuthorizerImpl) ValidateToken(token string) (*Claims, error) {
	claims := &Claims{}
	_, err := jwt.ParseWithClaims(token, claims, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return a.jwtSigningKey, nil
	})
	if err != nil {
		return nil, fmt.Errorf("can't parse token: %w", err)
	}

	return claims, nil
}

func jwtTokenForUser(user *repo.User, key []byte) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, Claims{
		StandardClaims: jwt.StandardClaims{
			IssuedAt:  time.Now().Unix(),
			ExpiresAt: time.Now().Add(time.Hour * 24).Unix(),
		},
		Username: user.Username,
		Role:     user.Role,
	})

	tok, err := token.SignedString(key)
	if err != nil {
		return "", fmt.Errorf("can't sign token: %w", err)
	}
	return tok, nil
}
