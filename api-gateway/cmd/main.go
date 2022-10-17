package main

import (
	"fmt"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/sirupsen/logrus"

	impl "github.com/kozl/ates/api-gateway/internal/api"
	"github.com/kozl/ates/api-gateway/internal/api/auth"
	"github.com/kozl/ates/api-gateway/internal/api/validator"
	"github.com/kozl/ates/api-gateway/internal/auth/events"
	"github.com/kozl/ates/api-gateway/internal/auth/repo"
	"github.com/kozl/ates/api-gateway/internal/auth/usecase"
	"github.com/kozl/ates/api-gateway/internal/generated/api"
)

func main() {
	var (
		err error
		log = logrus.New()
	)

	defer func() {
		if err := recover(); err != nil {
			log.WithError(fmt.Errorf("%v", err)).Error("panic")
			os.Exit(1)
		}

		if err != nil {
			log.WithError(err).Error("error")
			os.Exit(1)
		}
	}()

	r := chi.NewRouter()
	swagger, err := api.GetSwagger()
	if err != nil {
		return
	}

	r.Use(
		middleware.Recoverer,
		validator.OapiRequestValidator(swagger),
		auth.NewJWTContextMiddleware(),
	)

	userRepo := repo.NewInMemoryRepository()
	authEventProducer := events.MustNewKafkaEventProducer(mustGetEnv("KAFKA_BOOTSTRAP_SERVERS"))
	authorizer := usecase.NewAuthorizer(userRepo, authEventProducer, []byte(mustGetEnv("JWT_SECRET")))

	taskTrackerProxy, err := newProxy("http://task-tracker-app:8000")
	if err != nil {
		return
	}

	apiV1 := impl.NewV1(
		log,
		authorizer,
		taskTrackerProxy,
	)

	api.HandlerFromMux(apiV1, r)

	log.Info("Starting http server at :8080")
	http.ListenAndServe(":8080", r) // nolint: errcheck
}

func mustGetEnv(key string) string {
	v := os.Getenv(key)
	if v == "" {
		panic(fmt.Sprintf("environment variable %s is not set", key))
	}
	return v
}

func newProxy(targetUrl string) (*httputil.ReverseProxy, error) {
	url, err := url.Parse(targetUrl)
	if err != nil {
		return nil, err
	}

	return httputil.NewSingleHostReverseProxy(url), nil
}
