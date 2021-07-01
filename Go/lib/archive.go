package lib

import (
	"archive/tar"
	"archive/zip"
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"golang.org/x/text/encoding/simplifiedchinese"
	"golang.org/x/text/transform"
)

var SystemType = runtime.GOOS

func FileExists(path string) bool {
	_, err := os.Lstat(path)
	return !os.IsNotExist(err)
}

func MakeDir(path string) {
	err := os.MkdirAll(path, 0755)
	PrintError(err)
}

func DecompressTar(tarFilePath, destPath string) {
	file, err := os.Open(tarFilePath)
	PrintError(err)
	defer file.Close()
	tr := tar.NewReader(file)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		PrintError(err)
		if hdr.Typeflag == tar.TypeDir {
			MakeDir(filepath.Join(destPath, hdr.Name))
		}
	}
	file.Seek(0, io.SeekStart)
	tr = tar.NewReader(file)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		PrintError(err)
		if hdr.Typeflag == tar.TypeReg {
			ExtractFile(tr, filepath.Join(destPath, hdr.Name))
		}
	}
	file.Seek(0, io.SeekStart)
	tr = tar.NewReader(file)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		PrintError(err)
		ChTimeMode(filepath.Join(destPath, hdr.Name), time.Now(), hdr.FileInfo().ModTime(), hdr.FileInfo().Mode().Perm())
	}
}

func DecompressZip(zipFilePath, destPath string) {
	zr, err := zip.OpenReader(zipFilePath)
	PrintError(err)
	defer zr.Close()
	for _, hdr := range zr.File {
		if hdr.FileInfo().IsDir() {
			MakeDir(filepath.Join(destPath, DecodeName(hdr.Name)))
		}
	}
	for _, hdr := range zr.File {
		if hdr.FileInfo().IsDir() {
			continue
		} else {
			file, err := hdr.Open()
			PrintError(err)
			fmt.Println(hdr.Name)
			fmt.Println(DecodeName(hdr.Name))
			ExtractFile(file, filepath.Join(destPath, DecodeName(hdr.Name)))
			file.Close()
		}
	}
	for _, hdr := range zr.File {
		ChTimeMode(filepath.Join(destPath, DecodeName(hdr.Name)), time.Now(), hdr.Modified, hdr.FileInfo().Mode().Perm())
	}
}

func CompressTar(destPath, sourcePath string) {
	file, err := os.Create(destPath)
	PrintError(err)
	defer file.Close()
	tw := tar.NewWriter(file)
	defer tw.Close()
	err = filepath.Walk(sourcePath, func(path string, info os.FileInfo, err error) error {
		PrintError(err)
		hdr, err := tar.FileInfoHeader(info, "")
		PrintError(err)
		hdr.Name = strings.TrimLeft(path, filepath.Dir(sourcePath)+string(filepath.Separator))
		err = tw.WriteHeader(hdr)
		PrintError(err)

		if !info.Mode().IsRegular() {
			return nil
		}

		CompressFile(path, tw)
		return err
	})
	PrintError(err)
}

func CompressZip(destPath, sourcePath string) {
	file, err := os.Create(destPath)
	PrintError(err)
	defer file.Close()
	zw := zip.NewWriter(file)
	defer zw.Close()
	err = filepath.Walk(sourcePath, func(path string, info os.FileInfo, err error) error {
		PrintError(err)
		hdr, err := zip.FileInfoHeader(info)
		PrintError(err)
		hdr.Name = strings.TrimLeft(path, filepath.Dir(sourcePath)+string(filepath.Separator))
		if info.IsDir() {
			hdr.Name += string("/")
		}

		w, err := zw.CreateHeader(hdr)
		PrintError(err)

		if !info.Mode().IsRegular() {
			return nil
		}

		CompressFile(path, w)
		return err
	})
	PrintError(err)
}

func DecompressModuleFromTar() {

}

func DecompressModuleFromZip() {

}

func DecodeName(name string) string {
	in := bytes.NewReader([]byte(name))
	decoder := transform.NewReader(in, simplifiedchinese.GB18030.NewDecoder())
	out, _ := ioutil.ReadAll(decoder)
	return string(out)
}

func ExtractFile(data io.Reader, filename string) {
	if FileExists(filename) {
		file, err := os.OpenFile(filename, os.O_RDWR|os.O_CREATE, 0755)
		PrintError(err)
		defer file.Close()
		_, err = io.Copy(file, data)
		PrintError(err)
	} else {
		file, err := os.Create(filename)
		PrintError(err)
		defer file.Close()
		_, err = io.Copy(file, data)
		PrintError(err)
	}
}

func CompressFile(filePath string, wr io.Writer) {
	file, err := os.Open(filePath)
	PrintError(err)
	defer file.Close()
	_, err = io.Copy(wr, file)
	PrintError(err)
}

func ChTimeMode(filename string, atime time.Time, mtime time.Time, mode os.FileMode) {
	err := os.Chmod(filename, mode)
	PrintError(err)
	err = os.Chtimes(filename, atime, mtime)
	PrintError(err)
}
