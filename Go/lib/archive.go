package lib

import (
	"archive/tar"
	"archive/zip"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// CompressTar compresses a directory to a tar file.
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

// CompressZip compresses a directory to a zip file.
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

// DecompressTar decompresses a tar file to a directory.
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
			MakeDir(filepath.Join(destPath, hdr.Name), hdr.FileInfo().Mode().Perm())
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
		ChTimeMode(filepath.Join(destPath, hdr.Name), hdr.AccessTime, hdr.ModTime, hdr.FileInfo().Mode().Perm())
	}
}

// DecompressZip decompresses a zip file to a directory.
func DecompressZip(zipFilePath, destPath string) {
	zr, err := zip.OpenReader(zipFilePath)
	PrintError(err)
	defer zr.Close()
	for _, hdr := range zr.File {
		decodeName := DecodeName(hdr.Flags, hdr.Name)
		if hdr.FileInfo().IsDir() {
			MakeDir(filepath.Join(destPath, decodeName), hdr.Mode().Perm())
		}
	}
	for _, hdr := range zr.File {
		if hdr.FileInfo().IsDir() {
			continue
		} else {
			file, err := hdr.Open()
			PrintError(err)
			decodeName := DecodeName(hdr.Flags, hdr.Name)
			ExtractFile(file, filepath.Join(destPath, decodeName))
			file.Close()
		}
	}
	for _, hdr := range zr.File {
		decodeName := DecodeName(hdr.Flags, hdr.Name)
		ChTimeMode(filepath.Join(destPath, decodeName), time.Now(), hdr.Modified, hdr.Mode().Perm())
	}
}

// DecompressTar decompresses a tar file to a directory.
// It only decompresses files start with `moduleName`.
func DecompressModuleFromTar(tarFilePath, moduleName, destPath string) {
	tarFilePrefix := GetFilePrefix(tarFilePath)
	prefix := strings.Join([]string{tarFilePrefix, moduleName}, "/")
	srcFile, err := os.Open(tarFilePath)
	PrintError(err)
	defer srcFile.Close()
	tr := tar.NewReader(srcFile)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		PrintError(err)
		if hdr.Typeflag == tar.TypeDir && strings.HasPrefix(hdr.Name, prefix) {
			MakeDir(filepath.Join(destPath, hdr.Name), hdr.FileInfo().Mode().Perm())
		}
	}
	srcFile.Seek(0, io.SeekStart)
	tr = tar.NewReader(srcFile)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		PrintError(err)
		if hdr.Typeflag == tar.TypeReg && strings.HasPrefix(hdr.Name, prefix) {
			ExtractFile(tr, filepath.Join(destPath, hdr.Name))
		}
	}
	srcFile.Seek(0, io.SeekStart)
	tr = tar.NewReader(srcFile)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		PrintError(err)
		if strings.HasPrefix(hdr.Name, prefix) {
			ChTimeMode(filepath.Join(destPath, hdr.Name), hdr.AccessTime, hdr.ModTime, hdr.FileInfo().Mode().Perm())
		}
	}
}

// DecompressZip decompresses a zip file to a directory.
// It only decompresses files start with `moduleName`.
func DecompressModuleFromZip(zipFilePath, moduleName, destPath string) {
	zipFilePrefix := GetFilePrefix(zipFilePath)
	prefix := strings.Join([]string{zipFilePrefix, moduleName}, "/")
	zr, err := zip.OpenReader(zipFilePath)
	PrintError(err)
	defer zr.Close()
	for _, hdr := range zr.File {
		decodeName := DecodeName(hdr.Flags, hdr.Name)
		if hdr.FileInfo().IsDir() && strings.HasPrefix(hdr.Name, prefix) {
			MakeDir(filepath.Join(destPath, decodeName), hdr.Mode().Perm())
		}
	}
	for _, hdr := range zr.File {
		if hdr.FileInfo().IsDir() {
			continue
		} else if strings.HasPrefix(hdr.Name, prefix) {
			file, err := hdr.Open()
			PrintError(err)
			decodeName := DecodeName(hdr.Flags, hdr.Name)
			ExtractFile(file, filepath.Join(destPath, decodeName))
			file.Close()
		}
	}
	for _, hdr := range zr.File {
		decodeName := DecodeName(hdr.Flags, hdr.Name)
		ChTimeMode(filepath.Join(destPath, decodeName), time.Now(), hdr.Modified, hdr.Mode().Perm())
	}
}

// ExtractFile extracts data to a file.
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

// CompressFile writes a file's data to a tar|zip file.
func CompressFile(filePath string, wr io.Writer) {
	file, err := os.Open(filePath)
	PrintError(err)
	defer file.Close()
	_, err = io.Copy(wr, file)
	PrintError(err)
}
