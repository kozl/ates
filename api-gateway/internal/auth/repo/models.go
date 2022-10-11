package repo

const (
	DeveloperRole  = "developer"
	ManagerRole    = "manager"
	AccountantRole = "accountant"
)

type User struct {
	ID       int64  `json:"id"`
	Username string `json:"username"`
	Password string `json:"password"`
	Role     string `json:"role"`
}
