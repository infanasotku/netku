FROM golang:1.23

WORKDIR /app
COPY ./services/xray/go.mod .
COPY ./services/xray/go.sum .
RUN go mod download
COPY ./services/xray .
ENV GOCACHE=/root/.cache/go-build

RUN --mount=type=cache,target="/root/.cache/go-build" go build
CMD ./xray
