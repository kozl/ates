package usecase

type Authorizer interface {
	SignIn(username, password string) (string, error)
	SignUp(username, password, role string) (string, error)
	ValidateToken(token string) (*Claims, error)
}
