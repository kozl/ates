FROM golang:1.19 as builder

WORKDIR /src
COPY . /src

RUN GOOS=linux go build -o app ./cmd/main.go


FROM debian:11  
RUN apt-get update && apt-get install -y ca-certificates

WORKDIR /app/

COPY --from=builder /src/app .

CMD ["./app"]
