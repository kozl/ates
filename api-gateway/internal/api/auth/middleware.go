package auth

import (
	"context"
	"net/http"
	"strings"
)

type contextKey string

const JWTTokenContextKey = contextKey("JWTTokenContextKey")

func NewJWTContextMiddleware() func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			val := r.Header.Get("Authorization")
			if val == "" || !strings.HasPrefix(val, "Bearer ") {
				next.ServeHTTP(w, r)
				return
			}
			token := strings.TrimPrefix(val, "Bearer ")
			ctx := context.WithValue(r.Context(), JWTTokenContextKey, token)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

func GetJWTTokenFromContext(ctx context.Context) string {
	token, ok := ctx.Value(JWTTokenContextKey).(string)
	if !ok {
		return ""
	}
	return token
}
