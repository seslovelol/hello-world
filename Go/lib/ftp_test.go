package lib

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestFtpConnect(t *testing.T) {
	addr := "rocky.com:21"
	c := FtpConnect(addr)
	FtpLogin(c, "ftp1", "fhd123")
	FtpQuit(c)
}

func TestFtpFtpUpload(t *testing.T) {
	addr := "rocky.com:21"
	c := FtpConnect(addr)
	FtpLogin(c, "ftp1", "fhd123")
	source := "/Users/shiqiankun/DEV/Go/source/aa.log"
	dest := "a/b/c"
	dest = strings.ReplaceAll(filepath.Join(FtpCurrentDir(c), dest), "\\", "/")
	FtpMkdir(c, dest)
	FtpUpload(c, source)
	FtpQuit(c)
}

func TestFtpDownload(t *testing.T) {
	addr := "rocky.com:21"
	c := FtpConnect(addr)
	FtpLogin(c, "ftp1", "fhd123")
	source := "a/b/c"
	dest := "/Users/shiqiankun/DEV/Go/dest"
	err := os.Chdir(dest)
	PrintError(err)
	FtpChdir(c, strings.ReplaceAll(filepath.Join(FtpCurrentDir(c), source), "\\", "/"))
	FtpDownload(c, "aa.log")
	FtpQuit(c)
}
