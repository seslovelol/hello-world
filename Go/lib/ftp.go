package lib

import (
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/jlaffaye/ftp"
)

type ftpcon struct {
	conn     *ftp.ServerConn
	addr     string
	username string
	password string
}

// Connect connects to the specified address with optional options.
func (f *ftpcon) Connect() {
	var err error
	var c *ftp.ServerConn
	for i := 0; i < 3; i++ {
		c, err = ftp.Dial(f.addr, ftp.DialWithTimeout(5*time.Second))
		if err == nil {
			PrintInfo("Connect to %v successfully", f.addr)
			break
		}
		PrintInfo("%v Reconnect to %v", i, f.addr)
	}
	PrintError(err)
	f.conn = c
}

// login authenticates the client with specified user and password.
func (f *ftpcon) Login() {
	err := f.conn.Login(f.username, f.password)
	PrintError(err)
}

// CurrentDir issues a PWD FTP command, which Returns the path of the current directory.
func (f *ftpcon) CurrentDir() string {
	var path string
	path, err := f.conn.CurrentDir()
	PrintError(err)
	return path
}

// ChangeDir issues a CWD FTP command, which changes the current directory to the specified path.
func (f *ftpcon) Chdir(path string) {
	err := f.conn.ChangeDir(path)
	PrintError(err)
}

// MakeDir issues a MKD FTP command to create the specified directory on the remote FTP server.
func (f *ftpcon) MakeDir(path string) {
	for i, p := range strings.Split(path, "/") {
		if i == 0 {
			continue
		}
		err := f.conn.ChangeDir(p)
		if err != nil {
			err = f.conn.MakeDir(p)
			PrintError(err)
			err = f.conn.ChangeDir(p)
			PrintError(err)
		}
	}
}

// Download issues a RETR FTP command to fetch the specified file from the remote FTP server.
func (f *ftpcon) Download(filename string) {
	rd, err := f.conn.Retr(filename)
	PrintError(err)
	defer rd.Close()
	wr, err := os.OpenFile(filename, os.O_CREATE|os.O_RDWR, 0755)
	PrintError(err)
	defer wr.Close()
	_, err = io.Copy(wr, rd)
	PrintError(err)
}

// Upload issues a STOR FTP command to store a file to the remote FTP server. Stor creates the specified file with the content of the io.Reader.
func (f *ftpcon) Upload(filePath string) {
	filename := filepath.Base(filePath)
	rd, err := os.Open(filePath)
	PrintError(err)
	defer rd.Close()
	err = f.conn.Stor(filename, rd)
	PrintError(err)
}

// Quit issues a QUIT FTP command to properly close the connection from the remote FTP server.
func (f *ftpcon) Quit() {
	err := f.conn.Quit()
	PrintError(err)
}
