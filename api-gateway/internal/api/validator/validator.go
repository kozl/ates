package validator

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/getkin/kin-openapi/openapi3"
	"github.com/getkin/kin-openapi/openapi3filter"
	"github.com/getkin/kin-openapi/routers"
	"github.com/getkin/kin-openapi/routers/gorillamux"
	"github.com/kozl/ates/api-gateway/internal/generated/api"
)

func OapiRequestValidator(swagger *openapi3.T) func(next http.Handler) http.Handler {
	// TODO: authentication
	authNFunc := openapi3filter.NoopAuthenticationFunc

	router, err := gorillamux.NewRouter(swagger)
	if err != nil {
		panic(err)
	}

	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

			if code, err := validateRequest(r, router, authNFunc); err != nil {
				switch code {
				case http.StatusBadRequest:
					errDto := api.BadRequestError{
						Error: struct {
							Reason string "json:\"reason\""
						}{Reason: err.Error()},
					}
					w.WriteHeader(http.StatusBadRequest)
					json.NewEncoder(w).Encode(errDto) // nolint: errcheck
				case http.StatusUnauthorized:
					errDto := api.UnauthorizedError{
						Error: struct {
							Reason string "json:\"reason\""
						}{Reason: err.Error()},
					}
					w.WriteHeader(http.StatusUnauthorized)
					json.NewEncoder(w).Encode(errDto) // nolint: errcheck
				default:
					http.Error(w, err.Error(), code)
				}
				return
			}

			next.ServeHTTP(w, r)
		})
	}

}

func validateRequest(r *http.Request, router routers.Router, authNFunc openapi3filter.AuthenticationFunc) (int, error) {

	// Find route
	route, pathParams, err := router.FindRoute(r)
	if err != nil {
		return http.StatusBadRequest, err // We failed to find a matching route for the request.
	}

	// Validate request
	requestValidationInput := &openapi3filter.RequestValidationInput{
		Request:    r,
		PathParams: pathParams,
		Route:      route,
		Options: &openapi3filter.Options{
			AuthenticationFunc: authNFunc,
		},
	}

	if err := openapi3filter.ValidateRequest(context.Background(), requestValidationInput); err != nil {
		switch e := err.(type) {
		case *openapi3filter.RequestError:
			// We've got a bad request
			// Split up the verbose error by lines and return the first one
			// openapi errors seem to be multi-line with a decent message on the first
			errorLines := strings.Split(e.Error(), "\n")
			return http.StatusBadRequest, fmt.Errorf(errorLines[0])
		case *openapi3filter.SecurityRequirementsError:
			return http.StatusUnauthorized, err
		default:
			// This should never happen today, but if our upstream code changes,
			// we don't want to crash the server, so handle the unexpected error.
			return http.StatusInternalServerError, fmt.Errorf("error validating route: %s", err.Error())
		}
	}

	return http.StatusOK, nil
}
