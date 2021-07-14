package lib

import (
	"os"
	"path/filepath"
	"strings"

	"github.com/jlaffaye/ftp"
)

type wants struct {
	packageName string
	localPath   string
	short       string
	code        string
	ftpinfo     ftpInfo
}

type ftpInfo struct {
	addr     string
	username string
	password string
	path     string
}

func DownloadPackage() {
	_, args := GetArg(5, 11)
	ftp := strings.Split(args[4], ":")
	info := ftpInfo{
		addr:     strings.Join([]string{ftp[0], ftp[1]}, ":"),
		username: ftp[2],
		password: ftp[3],
		path:     ftp[4],
	}
	want := wants{
		packageName: args[0],
		localPath:   args[1],
		short:       args[2],
		code:        args[3],
		ftpinfo:     info,
	}
	FtpDownload(want)
}

func FtpDownload(w wants) {
	var c *ftp.ServerConn
	f := ftpcon{
		conn:     c,
		addr:     w.ftpinfo.addr,
		username: w.ftpinfo.username,
		password: w.ftpinfo.password,
	}
	f.Connect()
	f.Login()
	destPath := filepath.Join(w.localPath, w.short, w.code)
	BackupPath(destPath)
	MakeDir(destPath, 0755)
	os.Chdir(destPath)
	f.Chdir(strings.ReplaceAll(filepath.Join(f.CurrentDir(), w.ftpinfo.path), "\\", "/"))
	f.Download(w.packageName)
	f.Quit()
	PrintInfo("Download %v to %v", w.packageName, destPath)
}

func BackupPath(path string) {
	if DirExists(path) {
		os.Rename(path, strings.Join([]string{path, Now}, "_"))
	}
}
