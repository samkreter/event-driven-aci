FROM golang:1.9.2 as builder
WORKDIR  /go/src/high-cpu
COPY . /go/src/high-cpu
#RUN go get -u github.com/golang/dep/cmd/dep
#RUN dep ensure
# RUN go test ./...
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o worker .

FROM alpine:latest
RUN apk --update add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/high-cpu .
CMD ["./worker"]
