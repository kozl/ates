package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/sirupsen/logrus"

	impl "github.com/kozl/ates/api-gateway/internal/api"
	"github.com/kozl/ates/api-gateway/internal/api/auth"
	"github.com/kozl/ates/api-gateway/internal/api/validator"
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
		validator.OapiRequestValidator(swagger),
		auth.NewJWTContextMiddleware(),
	)

	apiV1 := &impl.V1{}
	api.HandlerFromMux(apiV1, r)

	log.Info("Starting http server at :8080")
	http.ListenAndServe(":8080", r) // nolint: errcheck
}
