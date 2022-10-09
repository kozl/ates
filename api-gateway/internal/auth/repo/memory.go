package repo

type InMemoryRepository struct {
	users map[string]*User
}

func NewInMemoryRepository() *InMemoryRepository {
	return &InMemoryRepository{
		users: make(map[string]*User),
	}
}

func (r *InMemoryRepository) GetUser(username string) (*User, error) {
	user, ok := r.users[username]
	if !ok {
		return nil, ErrUserNotFound
	}
	return user, nil
}

func (r *InMemoryRepository) AddUser(user *User) error {
	_, ok := r.users[user.Username]
	if ok {
		return ErrUserAlreadyExists
	}
	r.users[user.Username] = user
	return nil
}
