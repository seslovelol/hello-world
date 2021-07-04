package lib

import (
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/jlaffaye/ftp"
)

func FtpConnect(addr string) *ftp.ServerConn {
	c, err := ftp.Dial(addr, ftp.DialWithTimeout(5*time.Second))
	PrintError(err)
	return c
}

func FtpLogin(c *ftp.ServerConn, user, password string) {
	err := c.Login(user, password)
	PrintError(err)
}

func FtpCurrentDir(c *ftp.ServerConn) string {
	var path string
	path, err := c.CurrentDir()
	PrintError(err)
	return path
}

func FtpChdir(c *ftp.ServerConn, path string) {
	err := c.ChangeDir(path)
	PrintError(err)
}

func FtpMkdir(c *ftp.ServerConn, path string) {
	for i, p := range strings.Split(path, "/") {
		if i == 0 {
			continue
		}
		err := c.ChangeDir(p)
		if err != nil {
			err = c.MakeDir(p)
			PrintError(err)
			err = c.ChangeDir(p)
			PrintError(err)
		}
	}
}

func FtpDownload(c *ftp.ServerConn, filename string) {
	rd, err := c.Retr(filename)
	PrintError(err)
	defer rd.Close()
	wr, err := os.OpenFile(filename, os.O_CREATE|os.O_RDWR, 0755)
	PrintError(err)
	defer wr.Close()
	_, err = io.Copy(wr, rd)
	PrintError(err)
}

func FtpUpload(c *ftp.ServerConn, filePath string) {
	filename := filepath.Base(filePath)
	rd, err := os.Open(filePath)
	PrintError(err)
	defer rd.Close()
	err = c.Stor(filename, rd)
	PrintError(err)
}

func FtpQuit(c *ftp.ServerConn) {
	err := c.Quit()
	PrintError(err)
}
