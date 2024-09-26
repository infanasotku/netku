FROM golang:1.23

WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY . .
ENV GOCACHE=/root/.cache/go-build

# Install chrome dependencies
RUN apt-get update
RUN apt-get clean
RUN apt-get autoremove
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -f -y ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

RUN --mount=type=cache,target="/root/.cache/go-build" go build
CMD ./booking
