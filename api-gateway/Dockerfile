FROM golang:1.19 as builder

WORKDIR /src
COPY . /src

RUN CGO_ENABLED=0 GOOS=linux go build -o app ./cmd/main.go


FROM alpine:3.16  
RUN apk --no-cache add ca-certificates

WORKDIR /app/

COPY --from=builder /src/app .

CMD ["./app"]
