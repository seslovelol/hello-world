package lib

import (
	"bufio"
	"os"
	"path/filepath"
	"strings"

	"github.com/jlaffaye/ftp"
)

type needs struct {
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
	needs := needs{
		packageName: args[0],
		localPath:   args[1],
		short:       args[2],
		code:        args[3],
		ftpinfo:     info,
	}
	FtpDownload(needs)
	md5Old := ReadFile(strings.Join([]string{needs.packageName, "md5"}, "."))
	md5New := GetFileMd5(needs.packageName)
	if compareMd5(md5Old, md5New) {
		PrintInfo("0")
	} else {
		PrintInfo("-1")
	}
}

func FtpDownload(n needs) {
	var c *ftp.ServerConn
	f := ftpcon{
		conn:     c,
		addr:     n.ftpinfo.addr,
		username: n.ftpinfo.username,
		password: n.ftpinfo.password,
	}
	f.Connect()
	f.Login()
	destPath := filepath.Join(n.localPath, n.short, n.code)
	BackupPath(destPath)
	MakeDir(destPath, 0755)
	os.Chdir(destPath)
	f.Chdir(strings.ReplaceAll(filepath.Join(f.CurrentDir(), n.ftpinfo.path), "\\", "/"))
	md5File := strings.Join([]string{n.packageName, "md5"}, ".")
	f.Download(n.packageName)
	f.Download(md5File)
	f.Quit()
	PrintInfo("Download %v to %v", n.packageName, destPath)
	PrintInfo("Download %v to %v", md5File, destPath)
}

func BackupPath(path string) {
	if DirExists(path) {
		os.Rename(path, strings.Join([]string{path, Now}, "_"))
	}
}

func ReadFile(path string) string {
	file, err := os.Open(path)
	PrintError(err)
	defer file.Close()
	reader := bufio.NewReader(file)
	line, err := reader.ReadString('\n')
	PrintError(err)
	return line
}

func compareMd5(md5Old, md5New string) bool {
	md5Old = md5Old[2 : len(md5Old)-2]
	PrintInfo("Remote md5: %v\n", md5Old)
	PrintInfo("Local  md5: %v\n", md5New)
	return md5Old == md5New
}
