package lib

import (
	"fmt"
	"os"
	"testing"
	"time"
)

func TestGetArg(t *testing.T) {
	GetArg(4, 4)
}

func TestReadOrder(t *testing.T) {
	var path string
	switch SystemType {
	case "windows":
		path = "D:\\opt\\source\\order.txt"
	case "linux":
		path = "/opt/source/order.txt"
	case "darwin":
		path = "/opt/source/order.txt"
	default:
		path = "/opt/source/order.txt"
	}
	order := ReadOrder(path)
	for e := order.Front(); e != nil; e = e.Next() {
		fmt.Println(e.Value)
	}
}

func TestFileExists(t *testing.T) {
	var path string
	switch SystemType {
	case "windows":
		path = "D:\\opt\\source\\order.txt"
	case "linux":
		path = "/opt/source/order.txt"
	case "darwin":
		path = "/opt/source/order.txt"
	default:
		path = "/opt/source/order.txt"
	}
	FileExists(path)
	want := true
	if got := FileExists(path); got != want {
		t.Errorf("got %v\nwant %v", got, want)
	}
}

func TestDirExists(t *testing.T) {
	var path string
	switch SystemType {
	case "windows":
		path = "D:\\opt\\source"
	case "linux":
		path = "/opt/source"
	case "darwin":
		path = "/opt/source"
	default:
		path = "/opt/source"
	}
	want := true
	if got := DirExists(path); got != want {
		t.Errorf("got %v\nwant %v", got, want)
	}
}

func TestGetFilePrefix(t *testing.T) {
	fileName := "aa.bb"
	want := "aa"
	if got := GetFilePrefix(fileName); got != want {
		t.Errorf("got %v\nwant %v", got, want)
	}
}

func TestGetFileSuffix(t *testing.T) {
	fileName := "aa.bb"
	want := "bb"
	if got := GetFileSuffix(fileName); got != want {
		t.Errorf("got %v\nwant %v", got, want)
	}
}

func TestChTimeMode(t *testing.T) {
	var path string
	switch SystemType {
	case "windows":
		path = "D:\\opt\\source\\stat.txt"
	case "linux":
		path = "/opt/source/stat.txt"
	case "darwin":
		path = "/opt/source/stat.txt"
	default:
		path = "/opt/source/stat.txt"
	}
	atime := time.Date(2009, time.November, 10, 23, 0, 0, 0, time.Local)
	mtime := time.Date(2009, time.November, 10, 23, 0, 0, 0, time.Local)
	ChTimeMode(path, atime, mtime, 0755)
	file, err := os.Lstat(path)
	PrintError(err)
	if got := file.ModTime(); got != mtime {
		t.Errorf("got %v\nwant %v", got, mtime)
	}
	fmt.Println(file.Mode().Perm())
}

func TestKMP(t *testing.T) {
	str := "ATGTGAGCTGGTGTGTGCFAA"
	pattern := "GTGTGCF"
	want := 12
	if got := KMP(str, pattern); got != want {
		t.Errorf("got %v\nwant %v", got, want)
	}
}
