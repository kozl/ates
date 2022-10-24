package api

import (
	"encoding/json"
	"net/http"

	"github.com/kozl/ates/api-gateway/internal/generated/api"
)

func sendAPIError(w http.ResponseWriter, code int, reason string) {
	switch code {
	case http.StatusNotFound:
		errDto := api.NotFoundError{
			Error: struct {
				Reason string "json:\"reason\""
			}{Reason: reason},
		}
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(errDto)
	case http.StatusForbidden:
		errDto := api.ForbiddenError{
			Error: struct {
				Reason string "json:\"reason\""
			}{Reason: reason},
		}
		w.WriteHeader(http.StatusForbidden)
		json.NewEncoder(w).Encode(errDto)
	case http.StatusBadRequest:
		errDto := api.BadRequestError{
			Error: struct {
				Reason string "json:\"reason\""
			}{Reason: reason},
		}
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(errDto)
	default:
		http.Error(w, reason, code)
	}
}

func sendOkResult(w http.ResponseWriter, result bool) {
	out := api.OkResult{
		Result: struct {
			Ok bool "json:\"ok\""
		}{Ok: result},
	}
	err := json.NewEncoder(w).Encode(out)
	if err != nil {
		panic(err)
	}
}

func sendJSON(w http.ResponseWriter, data interface{}) {
	err := json.NewEncoder(w).Encode(data)
	if err != nil {
		panic(err)
	}
}

func copyHeader(src, dst http.Header) http.Header {
	for k, v := range src {
		dst[k] = v
	}
	return dst
}
