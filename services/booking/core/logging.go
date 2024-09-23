package core

import (
	"log/slog"
	"os"
	"time"

	"github.com/charmbracelet/lipgloss"
	"github.com/charmbracelet/log"
)

// Creates new loop logger.
func initLogger() *log.Logger {
	logger := log.NewWithOptions(os.Stdout, log.Options{
		ReportTimestamp: true,
		TimeFormat:      time.DateTime,
		Prefix:          "[LOOP]",
	})

	styles := log.DefaultStyles()
	styles.Keys["err"] = lipgloss.NewStyle().Foreground(lipgloss.Color("204"))
	styles.Values["err"] = lipgloss.NewStyle().Bold(true)
	styles.Keys["email"] = lipgloss.NewStyle().Foreground(lipgloss.Color("99"))
	styles.Values["email"] = lipgloss.NewStyle().Bold(true)

	logger.SetStyles(styles)

	return logger
}

// Creates loop sublogger.
func createSubLogger(id string, parent *log.Logger) *slog.Logger {
	return slog.New(parent).With("id", id)
}
