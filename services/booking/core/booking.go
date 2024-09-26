package core

import (
	"errors"
	"strings"
	"time"

	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/input"
)

type PageType int64

const (
	BOOKING PageType = iota
	LOGIN
	UNKNOWN
)

type BookingStatus int64

const (
	BOOKED BookingStatus = iota
	WAIT_UNBOOKED
	UNBOOKED
	EMPTY
)

// Checks page type.
func checkPage(page *rod.Page) PageType {
	url := page.MustInfo().URL

	if strings.Contains(url, "Login") {
		return LOGIN
	}
	if strings.Contains(url, "DevicesCurrent") {
		return BOOKING
	}

	return UNKNOWN
}

// Checks booking status.
// Browser must be at booking page.
func checkStatus(page *rod.Page) BookingStatus {
	err := rod.Try(func() {
		page.Timeout(time.Second).MustElementR("h1", "Список прачечных пуст!")
	})
	if err == nil {
		return EMPTY
	}

	err = rod.Try(func() {
		page.Timeout(time.Second).MustElementR(".device", "Отменить бронь")
	})
	if err == nil {
		return BOOKED
	}

	err = rod.Try(func() {
		page.Timeout(time.Second).MustElementR(".device", "Забронировать")
	})
	if err != nil {
		return WAIT_UNBOOKED
	}

	return UNBOOKED
}

// Logs in into personal account. Browser must be at login page.
func login(page *rod.Page, email string, password string) error {
	if checkPage(page) != LOGIN {
		return errors.New("login page not openned")
	}

	page.MustElement("#Email").MustInput(email)
	page.MustElement("#Password").MustInput(password).MustType(input.Enter)

	err := rod.Try(func() {
		page.Timeout(time.Second*2).MustElementR("li", "Неверный логин или пароль")
	})
	if err == nil {
		return errors.New("bad credentials")
	}

	for {
		url := page.MustInfo().URL
		if !strings.Contains(url, "Login") {
			break
		}
		time.Sleep(time.Second)
	}

	return nil
}

// Waits until at least one machine will be unbooked.
// Browser must be at booking page.
func waitUnbooked(page *rod.Page) error {
	//#region Checks
	if checkPage(page) != BOOKING {
		return errors.New("booking page not openned")
	}

	err := rod.Try(func() {
		page.Timeout(time.Second).MustElementR(".device", "Отменить бронь")
	})
	if err == nil {
		return errors.New("machine already booked")
	}
	//#endregion
	_ = rod.Try(func() {
		page.Timeout(time.Minute*5).MustElementR(".device", "Забронировать")
	})
	return nil
}

// Waits until booking over.
// Browser must be at booking page.
func waitBookingOver(page *rod.Page) error {
	//#region Checks
	if checkPage(page) != BOOKING {
		return errors.New("booking page not openned")
	}

	err := rod.Try(func() {
		page.Timeout(time.Second).MustElementR(".device", "Отменить бронь")
	})
	if err != nil {
		return errors.New("no booking machines")
	}
	//#endregion

	_ = rod.Try(func() {
		page.Timeout(time.Minute*5).MustElementR(".device", "Забронировать")
	})
	return nil
}

/*
Books best washing machine.
Browser must be at booking page.
At least one machine must be unbooked.
Returns remaining washing time for selected machine.
*/
func book(page *rod.Page) (string, error) {
	//#region Checks
	if checkPage(page) != BOOKING {
		return "", errors.New("booking page not openned")
	}

	err := rod.Try(func() {
		page.Timeout(time.Second).MustElementR(".device", "Забронировать")
	})
	if err != nil {
		return "", errors.New("no machines for booking")
	}
	//#endregion

	// Confirm booking.
	confirm := func(device *rod.Element) error {
		bookingButton := device.MustElement("button")
		bookingButton.MustClick()

		modal := page.MustElement(".modal")
		confirmButton := modal.MustElementR("button", "Забронировать")
		confirmButton.MustClick()

		err := rod.Try(func() {
			page.Timeout(time.Second*5).MustElementR(".device", "Отменить бронь")
		})

		if err != nil {
			return errors.New("undefined error while booking")
		}
		return nil
	}

	// Selects best machine.
	deviceGroup := page.MustElement(".device-group")

	// Selects free machine if exist.
	exist, freeMachine, _ := deviceGroup.HasR(".device", "Свободна")

	if exist {
		return "00:00", confirm(freeMachine)
	}

	// Selects the machine with the least amount of washing time remaining.
	devices := deviceGroup.MustElements(".device")
	bestTime := "99:99" // Inits with max value.
	bestIndex := -1

	for index, device := range devices {
		unbooked, _, _ := device.HasR("button", "Забронировать")
		hasTimer := device.MustHas("[title='Время до конца стирки']")
		if !unbooked || !hasTimer {
			continue
		}

		time := device.MustElement("[title='Время до конца стирки']").MustText()

		if time < bestTime {
			bestTime = time
			bestIndex = index
		}
	}

	if bestIndex == -1 {
		return "", errors.New("no machines for booking")
	}

	return bestTime, confirm(devices[bestIndex])
}
