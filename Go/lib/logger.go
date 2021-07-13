package lib

import (
	"errors"
	"io"
	"log"
	"os"
	"path/filepath"
)

// Logger creates a log handler.
func Logger() *log.Logger {
	var path string
	switch SystemType {
	case "windows":
		path = "D:\\opt\\log\\run.log"
	case "linux":
		path = "/opt/log/run.log"
	case "darwin":
		path = "/opt/log/run.log"
	default:
		path = "/opt/log/run.log"
	}
	err := os.MkdirAll(filepath.Dir(path), 0755)
	if err != nil {
		log.Fatal(err)
	}
	file, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0755)
	if err != nil {
		log.Fatal(err)
	}
	writers := []io.Writer{
		os.Stdout,
		file,
	}
	logger := log.New(io.MultiWriter(writers...), "", log.LstdFlags|log.Lshortfile)
	return logger
}

var logger = Logger()

// PrintError prints errors and followes by a call to os.Exit(1).
func PrintError(err error) {
	if err != nil {
		logger.Fatal(err)
	}
}

// PrintInfo calls l.Output to print to the logger.
// Arguments are handled in the manner of fmt.Printf.
func PrintInfo(format string, v ...interface{}) {
	logger.Printf(format, v...)
}

// ExitError prints errors and followes by a call to os.Exit(1).
func ExitError(err string) {
	newErr := errors.New(err)
	logger.Fatal(newErr)
}
