package events

type UserCreated struct {
	Login string `json:"login"`
	Role  string `json:"role"`
}
