package lib

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/jlaffaye/ftp"
)

func TestFtpConnect(t *testing.T) {
	var c *ftp.ServerConn
	f := ftpcon{
		conn:     c,
		addr:     "rocky.com:21",
		username: "ftp1",
		password: "ftp123",
	}
	f.Connect()
	f.Login()
	f.Quit()
}

func TestFtpFtpUpload(t *testing.T) {
	var sourcePath, destPath string
	switch SystemType {
	case "windows":
		sourcePath = "D:\\opt\\source\\test.tar"
		destPath = "a/b/c"
	case "linux":
		sourcePath = "/opt/source/test.tar"
		destPath = "a/b/c"
	case "darwin":
		sourcePath = "/opt/source/test.tar"
		destPath = "a/b/c"
	default:
		sourcePath = "/opt/source/test.tar"
		destPath = "a/b/c"
	}
	var c *ftp.ServerConn
	f := ftpcon{
		conn:     c,
		addr:     "rocky.com:21",
		username: "ftp1",
		password: "ftp123",
	}
	f.Connect()
	f.Login()
	destPath = strings.ReplaceAll(filepath.Join(f.CurrentDir(), destPath), "\\", "/")
	f.MakeDir(destPath)
	f.Upload(sourcePath)
	f.Quit()
}

func TestFtpDownload(t *testing.T) {
	var sourcePath, destPath string
	switch SystemType {
	case "windows":
		sourcePath = "a/b/c"
		destPath = "/opt/dest/ftp"
	case "linux":
		sourcePath = "a/b/c"
		destPath = "/opt/dest/ftp"
	case "darwin":
		sourcePath = "a/b/c"
		destPath = "/opt/dest/ftp"
	default:
		sourcePath = "a/b/c"
		destPath = "/opt/dest/ftp"
	}
	var c *ftp.ServerConn
	f := ftpcon{
		conn:     c,
		addr:     "rocky.com:21",
		username: "ftp1",
		password: "ftp123",
	}
	f.Connect()
	f.Login()
	MakeDir(destPath, 0755)
	os.Chdir(destPath)
	f.Chdir(strings.ReplaceAll(filepath.Join(f.CurrentDir(), sourcePath), "\\", "/"))
	f.Download("test.tar")
	f.Quit()
}
