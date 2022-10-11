package events

type EventProducer interface {
	ProduceUserCreated(login, role string) error
}
