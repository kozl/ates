package events

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"gopkg.in/confluentinc/confluent-kafka-go.v1/kafka"
)

var (
	topic    = "auth.UserCreated"
	numparts = 1
)

type KafkaEventProducer struct {
	kafka *kafka.Producer
}

func MustNewKafkaEventProducer(bootstrapServers string) *KafkaEventProducer {
	p, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": bootstrapServers,
	})
	if err != nil {
		panic(fmt.Errorf("kafka producer creation err: %w", err))
	}

	a, err := kafka.NewAdminClientFromProducer(p)
	if err != nil {
		panic(fmt.Errorf("kafka admin client creation err: %w", err))
	}
	_, err = a.CreateTopics(
		context.Background(),
		[]kafka.TopicSpecification{
			{
				Topic:             topic,
				NumPartitions:     numparts,
				ReplicationFactor: 1,
			},
		},
		kafka.SetAdminOperationTimeout(10*time.Second),
	)
	if err != nil {
		panic(fmt.Errorf("kafka topic creation err: %w", err))
	}

	return &KafkaEventProducer{kafka: p}
}

func (p *KafkaEventProducer) ProduceUserCreated(login, role string) error {
	event := UserCreated{
		Login: login,
		Role:  role,
	}

	data, err := json.Marshal(event)
	if err != nil {
		return fmt.Errorf("json marshal err: %w", err)
	}

	err = p.kafka.Produce(&kafka.Message{
		TopicPartition: kafka.TopicPartition{
			Topic:     &topic,
			Partition: kafka.PartitionAny,
		},
		Value: data,
	}, nil)

	if err != nil {
		return fmt.Errorf("kafka produce err: %w", err)
	}

	return nil

}
