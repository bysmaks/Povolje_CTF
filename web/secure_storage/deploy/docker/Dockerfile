FROM golang:1.23.1 AS builder

WORKDIR /app

COPY ../go.mod ../go.sum ./

RUN go mod download

COPY .. .

RUN CGO_ENABLED=0 GOOS=linux go build -o app

FROM alpine:latest


RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app/
RUN mkdir -p /app/users && \
    chown -R appuser:appgroup /app/users && \
    chmod -R 755 /app && \
    chmod 775 /app/users

RUN echo "ctf{to_marsh4l_or_not_t0_mar5hal_tha7_1s_the_path_trav3rsal}" >> flag.txt
USER appuser

COPY --from=builder /app/ .

CMD ["./app"]
