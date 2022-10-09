// Package api provides primitives to interact with the openapi HTTP API.
//
// Code generated by github.com/deepmap/oapi-codegen version v1.10.1 DO NOT EDIT.
package api

import (
	"time"

	openapi_types "github.com/deepmap/oapi-codegen/pkg/types"
)

const (
	BearerAuthScopes = "bearerAuth.Scopes"
)

// Defines values for AuthSignUpRole.
const (
	AuthSignUpRoleAccountant AuthSignUpRole = "accountant"

	AuthSignUpRoleDeveloper AuthSignUpRole = "developer"

	AuthSignUpRoleManager AuthSignUpRole = "manager"
)

// AccountsSummary defines model for AccountsSummary.
type AccountsSummary struct {
	BalanceByDay   *[]BalanceEntry `json:"balanceByDay,omitempty"`
	CurrentBalance *int            `json:"currentBalance,omitempty"`
}

// AuditLogEntry defines model for AuditLogEntry.
type AuditLogEntry struct {
	Action        string    `json:"action"`
	BalanceChange int       `json:"balanceChange"`
	DateTime      time.Time `json:"dateTime"`
	TaskID        string    `json:"taskID"`
}

// AuthSignIn defines model for AuthSignIn.
type AuthSignIn struct {
	Login    string `json:"login"`
	Password string `json:"password"`
}

// AuthSignUp defines model for AuthSignUp.
type AuthSignUp struct {
	Login    string          `json:"login"`
	Password string          `json:"password"`
	Role     *AuthSignUpRole `json:"role,omitempty"`
}

// AuthSignUpRole defines model for AuthSignUp.Role.
type AuthSignUpRole string

// BadRequestError defines model for BadRequestError.
type BadRequestError struct {
	Error struct {
		Reason string `json:"reason"`
	} `json:"error"`
}

// BalanceEntry defines model for BalanceEntry.
type BalanceEntry struct {
	Balance int                `json:"balance"`
	Date    openapi_types.Date `json:"date"`
}

// CreateTaskIn defines model for CreateTaskIn.
type CreateTaskIn struct {
	Assignee    string `json:"assignee"`
	Description string `json:"description"`
}

// ForbiddenError defines model for ForbiddenError.
type ForbiddenError struct {
	Error struct {
		Reason string `json:"reason"`
	} `json:"error"`
}

// GetAccountsSummaryResult defines model for GetAccountsSummaryResult.
type GetAccountsSummaryResult struct {
	Result AccountsSummary `json:"result"`
}

// GetAllAccountsResult defines model for GetAllAccountsResult.
type GetAllAccountsResult struct {
	Result []UserAccount `json:"result"`
}

// GetMyAccountResult defines model for GetMyAccountResult.
type GetMyAccountResult struct {
	Result MyAccount `json:"result"`
}

// GetTaskResult defines model for GetTaskResult.
type GetTaskResult struct {
	Result Task `json:"result"`
}

// GetTaskStatsResult defines model for GetTaskStatsResult.
type GetTaskStatsResult struct {
	Result TaskStats `json:"result"`
}

// ListTask defines model for ListTask.
type ListTask struct {
	Assignee string `json:"assignee"`
	Id       string `json:"id"`
	Status   string `json:"status"`
}

// ListTasksResult defines model for ListTasksResult.
type ListTasksResult struct {
	Result []ListTask `json:"result"`
}

// MyAccount defines model for MyAccount.
type MyAccount struct {
	AuditLog *[]AuditLogEntry `json:"auditLog,omitempty"`
	Balance  *int             `json:"balance,omitempty"`
}

// NotFoundError defines model for NotFoundError.
type NotFoundError struct {
	Error struct {
		Reason string `json:"reason"`
	} `json:"error"`
}

// OkResult defines model for OkResult.
type OkResult struct {
	Result struct {
		Ok bool `json:"ok"`
	} `json:"result"`
}

// Task defines model for Task.
type Task struct {
	Assignee    string    `json:"assignee"`
	CreatedAt   time.Time `json:"createdAt"`
	Description string    `json:"description"`
	Id          string    `json:"id"`
	UpdatedAt   time.Time `json:"updatedAt"`
}

// TaskStats defines model for TaskStats.
type TaskStats struct {
	MostExpensiveTaskCost *int    `json:"mostExpensiveTaskCost,omitempty"`
	MostExpensiveTaskId   *string `json:"mostExpensiveTaskId,omitempty"`
}

// UnauthorizedError defines model for UnauthorizedError.
type UnauthorizedError struct {
	Error struct {
		Reason string `json:"reason"`
	} `json:"error"`
}

// UserAccount defines model for UserAccount.
type UserAccount struct {
	Balance *int    `json:"balance,omitempty"`
	UserID  *string `json:"userID,omitempty"`
}

// SignInJSONBody defines parameters for SignIn.
type SignInJSONBody AuthSignIn

// SignUpJSONBody defines parameters for SignUp.
type SignUpJSONBody AuthSignUp

// GetAccountsSummaryParams defines parameters for GetAccountsSummary.
type GetAccountsSummaryParams struct {
	// Дата начала периода
	From *openapi_types.Date `json:"from,omitempty"`

	// Дата конца периода
	To *openapi_types.Date `json:"to,omitempty"`
}

// CreateTaskJSONBody defines parameters for CreateTask.
type CreateTaskJSONBody CreateTaskIn

// GetTaskStatsParams defines parameters for GetTaskStats.
type GetTaskStatsParams struct {
	// Дата начала периода
	From *openapi_types.Date `json:"from,omitempty"`

	// Дата конца периода
	To *openapi_types.Date `json:"to,omitempty"`
}

// SignInJSONRequestBody defines body for SignIn for application/json ContentType.
type SignInJSONRequestBody SignInJSONBody

// SignUpJSONRequestBody defines body for SignUp for application/json ContentType.
type SignUpJSONRequestBody SignUpJSONBody

// CreateTaskJSONRequestBody defines body for CreateTask for application/json ContentType.
type CreateTaskJSONRequestBody CreateTaskJSONBody
