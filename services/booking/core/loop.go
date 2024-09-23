package core

import (
	"log/slog"
	"sync"

	"github.com/google/uuid"

	"github.com/charmbracelet/log"
	"github.com/go-rod/rod"
)

type Loop struct {
	id       string
	email    string
	password string
	logger   *slog.Logger
	browser  *rod.Browser
	page     *rod.Page
	cancel   func()
	quit     chan bool
	mu       *sync.Mutex
}

func createLoop(email string, password string, parentLogger *log.Logger) *Loop {
	id := uuid.New().String()
	logger := createSubLogger(id, parentLogger)

	browser := rod.New().MustConnect()

	loop := Loop{id: id, email: email, password: password, logger: logger, browser: browser, mu: &sync.Mutex{}}

	return &loop
}

// Runs booking loop in new goroutine
func (loop *Loop) run() {
	loop.quit = make(chan bool)
	page := loop.browser.MustPage("https://lk.1clc.ru/").MustWaitStable()
	loop.page, loop.cancel = page.WithCancel()
	go loop.runConcurency()
}

// Stops loop
func (loop *Loop) stop() {
	defer loop.mu.Unlock()
	loop.mu.Lock()
	select {
	case <-loop.quit:
		// Loop already stopped
		return
	default:
		loop.logger.Info("Loop stopping...")
		loop.quit <- true
		loop.cancel()
	}
}

// Waits while loop stop
func (loop *Loop) wait() {
	for {
		val, opened := <-loop.quit
		if !opened {
			return
		}
		loop.mu.Lock()
		loop.quit <- val
		loop.mu.Unlock()
	}
}

// Runs loop in concurency mod. Internal method.
func (loop *Loop) runConcurency() {
	defer close(loop.quit)
	loop.logger.Info("Loop started", "email", loop.email)

	// Loop
	for {
		select {
		case <-loop.quit:
			loop.logger.Info("Loop stopped")
			return
		default:
			loop.next()
		}
	}
}

// Next loop tick
func (loop *Loop) next() {

	pageType := checkPage(loop.page)

	switch pageType {
	case UNKNOWN:
		loop.logger.Error("UKNOWN page found")
		loop.stop()
		return

	case LOGIN:
		loop.logger.Info("Logging in...")
		err := login(loop.page, loop.email, loop.password)
		if err != nil {
			loop.logger.Error("Error occured while logging in", "err", err)
			loop.stop()
			return
		}
		loop.logger.Info("Logged in successful")

	case BOOKING:
		status := checkStatus(loop.page)

		switch status {
		case UNBOOKED:
			loop.logger.Info("Booking machine...")
			time, err := book(loop.page)
			if err != nil {
				loop.logger.Error("Error occured while booking", "err", err)
				loop.stop()
				return
			}
			loop.logger.Info("Booked successful", "remaining", time)
		case BOOKED:
			loop.logger.Info("Waiting until booking over...")
			err := waitBookingOver(loop.page)
			if err != nil {
				loop.logger.Error("Error occured while waiting booking over", "err", err)
				loop.stop()
				return
			}

		case WAIT_UNBOOKED:
			loop.logger.Info("Waiting until unbooked...")
			err := waitUnbooked(loop.page)
			if err != nil {
				loop.logger.Error("Error occured while waiting unbooked", "err", err)
				loop.stop()
				return
			}
		}
	}

}
