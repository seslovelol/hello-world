package lib

import (
	"io"
	"log"
	"os"
	"path/filepath"
)

func Logger() *log.Logger {
	var path string
	switch SystemType {
	case "windows":
		path = "D:\\Go\\log\\run.log"
	default:
		path = "/Users/shiqiankun/DEV/Go/log/run.log"
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

func PrintError(err error) {
	if err != nil {
		logger.Fatal(err)
	}
}

func PrintInfo(format string, v ...interface{}) {
	logger.Printf(format, v...)
}
