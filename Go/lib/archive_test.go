package lib

import "testing"

func TestComressTar(t *testing.T) {
	CompressTar("/Users/shiqiankun/DEV/Go/dest/test.tar", "/Users/shiqiankun/DEV/Go/source/tar")
}

func TestComressZip(t *testing.T) {
	CompressZip("/Users/shiqiankun/DEV/Go/dest/test.zip", "/Users/shiqiankun/DEV/Go/source/zip")
}

func TestDecompressTar(t *testing.T) {
	DecompressTar("/Users/shiqiankun/DEV/Go/dest/test.tar", "/Users/shiqiankun/DEV/Go/dest")
}

func TestDecompressZip(t *testing.T) {
	DecompressZip("/Users/shiqiankun/DEV/Go/dest/test.zip", "/Users/shiqiankun/DEV/Go/dest")
}
