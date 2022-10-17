package api

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httputil"

	"github.com/kozl/ates/api-gateway/internal/api/auth"
	"github.com/kozl/ates/api-gateway/internal/auth/repo"
	"github.com/kozl/ates/api-gateway/internal/auth/usecase"
	"github.com/kozl/ates/api-gateway/internal/generated/api"
	"github.com/sirupsen/logrus"
)

type V1 struct {
	log *logrus.Logger

	taskTrackerProxy *httputil.ReverseProxy
	authorizer       usecase.Authorizer
}

func NewV1(log *logrus.Logger, authorizer usecase.Authorizer, taskTrackerProxy *httputil.ReverseProxy) *V1 {
	return &V1{
		log:              log,
		taskTrackerProxy: taskTrackerProxy,
		authorizer:       authorizer,
	}
}

// Залогиниться в системе
// (POST /auth/sign-in)
func (a *V1) SignIn(w http.ResponseWriter, r *http.Request) {
	var req api.AuthSignIn
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		a.log.WithFields(logrus.Fields{"error": err}).Error("failed to decode request body")
		sendAPIError(w, http.StatusBadRequest, "invalid input format")
		return
	}
	token, err := a.authorizer.SignIn(req.Login, req.Password)
	if err != nil {
		a.log.WithFields(logrus.Fields{"error": err}).Errorf("failed to sign-in")
		sendAPIError(w, http.StatusBadRequest, fmt.Sprintf("failed to sign-in: %s", err))
		return
	}

	sendJSON(w, api.AuthSignInResult{Token: token})
}

// Зарегистрироваться в системе
// (POST /auth/sign-up)
func (a *V1) SignUp(w http.ResponseWriter, r *http.Request) {
	var req api.AuthSignUp
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		a.log.WithFields(logrus.Fields{"error": err}).Error("failed to decode request body")
		sendAPIError(w, http.StatusBadRequest, "invalid input format")
		return
	}
	role := repo.DeveloperRole
	if req.Role != nil {
		role = string(*req.Role)
	}
	token, err := a.authorizer.SignUp(req.Login, req.Password, role)
	if err != nil {
		a.log.WithFields(logrus.Fields{"error": err}).Errorf("failed to sign-up")
		sendAPIError(w, http.StatusBadRequest, fmt.Sprintf("failed to sign-up: %s", err))
		return
	}

	sendJSON(w, api.AuthSignUpResult{Token: token})
}

// Получить данные о счетах всех сотрудников
// (GET /v1/accounts)
func (a *V1) GetAllAccounts(w http.ResponseWriter, r *http.Request) {
	panic("not implemented") // TODO: Implement
}

// Информация о собственном счёте сотрудника
// (GET /v1/accounts/my)
func (a *V1) GetMyAccount(w http.ResponseWriter, r *http.Request) {
	panic("not implemented") // TODO: Implement
}

// Сводная информация о счетах сотрудников
// (GET /v1/accounts/summary)
func (a *V1) GetAccountsSummary(w http.ResponseWriter, r *http.Request, params api.GetAccountsSummaryParams) {
	panic("not implemented") // TODO: Implement
}

// Получить список задач
// (GET /v1/tasks)
func (a *V1) ListTasks(w http.ResponseWriter, r *http.Request) {
	token := auth.GetJWTTokenFromContext(r.Context())
	claims, err := a.authorizer.ValidateToken(token)
	if err != nil {
		a.log.WithFields(logrus.Fields{"error": err}).Error("failed to validate token")
		sendAPIError(w, http.StatusForbidden, "failed to validate token")
		return
	}

	r.Header.Set("X-User", claims.Username)
	r.Header.Set("X-Role", claims.Role)

	a.taskTrackerProxy.ServeHTTP(w, r)
}

// Создать задачу
// (POST /v1/tasks)
func (a *V1) CreateTask(w http.ResponseWriter, r *http.Request) {
	panic("not implemented") // TODO: Implement
}

// Распределить задачи по исполнителям
// (POST /v1/tasks/assign)
func (a *V1) AssignTasks(w http.ResponseWriter, r *http.Request) {
	token := auth.GetJWTTokenFromContext(r.Context())
	claims, err := a.authorizer.ValidateToken(token)
	if err != nil {
		a.log.WithFields(logrus.Fields{"error": err}).Error("failed to validate token")
		sendAPIError(w, http.StatusForbidden, "failed to validate token")
		return
	}

	if claims.Role != repo.ManagerRole {
		a.log.WithFields(logrus.Fields{"error": err}).Error("only managers can assign tasks")
		sendAPIError(w, http.StatusForbidden, "only managers can assign tasks")
		return
	}

	w.Write([]byte("Bang!")) // nolint: errcheck
}

// Получить статистику по стоимости задач
// (POST /v1/tasks/stats)
func (a *V1) GetTaskStats(w http.ResponseWriter, r *http.Request, params api.GetTaskStatsParams) {
	panic("not implemented") // TODO: Implement
}

// Получить информацию о задаче
// (GET /v1/tasks/{taskID})
func (a *V1) GetTask(w http.ResponseWriter, r *http.Request, taskID string) {
	panic("not implemented") // TODO: Implement
}

// Закрыть задачу
// (POST /v1/tasks/{taskID}/close)
func (a *V1) CloseTask(w http.ResponseWriter, r *http.Request, taskID string) {
	panic("not implemented") // TODO: Implement
}
