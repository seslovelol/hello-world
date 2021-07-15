package lib

import "testing"

func TestComressTar(t *testing.T) {
	var sourcePath, destPath string
	switch SystemType {
	case "windows":
		sourcePath = "D:\\opt\\source\\tar"
		destPath = "D:\\opt\\dest\\test.tar"
	case "linux":
		sourcePath = "/opt/source/tar"
		destPath = "/opt/dest/test.tar"
	case "darwin":
		sourcePath = "/opt/source/tar"
		destPath = "/opt/dest/test.tar"
	default:
		sourcePath = "/opt/source/tar"
		destPath = "/opt/dest/test.tar"
	}
	CompressTar(destPath, sourcePath)
}

func TestComressZip(t *testing.T) {
	var sourcePath, destPath string
	switch SystemType {
	case "windows":
		sourcePath = "D:\\opt\\source\\zip"
		destPath = "D:\\opt\\dest\\test.zip"
	case "linux":
		sourcePath = "/opt/source/zip"
		destPath = "/opt/dest/test.zip"
	case "darwin":
		sourcePath = "/opt/source/zip"
		destPath = "/opt/dest/test.zip"
	default:
		sourcePath = "/opt/source/zip"
		destPath = "/opt/dest/test.zip"
	}
	CompressZip(destPath, sourcePath)
}

func TestDecompressTar(t *testing.T) {
	var sourcePath, destPath string
	switch SystemType {
	case "windows":
		sourcePath = "D:\\opt\\source\\test.tar"
		destPath = "D:\\opt\\dest"
	case "linux":
		sourcePath = "/opt/source/test.tar"
		destPath = "/opt/dest"
	case "darwin":
		sourcePath = "/opt/source/test.tar"
		destPath = "/opt/dest"
	default:
		sourcePath = "/opt/source/test.tar"
		destPath = "/opt/dest"
	}
	DecompressTar(sourcePath, destPath)
}

func TestDecompressZip(t *testing.T) {
	var sourcePath, destPath string
	switch SystemType {
	case "windows":
		sourcePath = "D:\\opt\\source\\test.zip"
		destPath = "D:\\opt\\dest"
	case "linux":
		sourcePath = "/opt/source/test.zip"
		destPath = "/opt/dest"
	case "darwin":
		sourcePath = "/opt/source/test.zip"
		destPath = "/opt/dest"
	default:
		sourcePath = "/opt/source/test.zip"
		destPath = "/opt/dest"
	}
	DecompressZip(sourcePath, destPath)
}
