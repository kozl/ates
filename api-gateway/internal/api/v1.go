package api

import (
	"net/http"

	"github.com/kozl/ates/api-gateway/internal/generated/api"
)

type V1 struct{}

// Залогиниться в системе
// (POST /auth/sign-in)
func (a *V1) SignIn(w http.ResponseWriter, r *http.Request) {
	panic("not implemented") // TODO: Implement
}

// Зарегистрироваться в системе
// (POST /auth/sign-up)
func (a *V1) SignUp(w http.ResponseWriter, r *http.Request) {
	panic("not implemented") // TODO: Implement
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
	panic("not implemented") // TODO: Implement
}

// Создать задачу
// (POST /v1/tasks)
func (a *V1) CreateTask(w http.ResponseWriter, r *http.Request) {
	panic("not implemented") // TODO: Implement
}

// Распределить задачи по исполнителям
// (POST /v1/tasks/assign)
func (a *V1) AssignTasks(w http.ResponseWriter, r *http.Request) {
	panic("not implemented") // TODO: Implement
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
