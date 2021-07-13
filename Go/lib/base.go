package lib

import (
	"bufio"
	"bytes"
	"container/list"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"golang.org/x/text/encoding/simplifiedchinese"
	"golang.org/x/text/transform"
)

var SystemType = runtime.GOOS

// GetArg hold the command-line arguments, starting with the program name.
func GetArg(min, max int) (int, []string) {
	args := os.Args
	length := len(args)
	if length < min {
		ExitError("too few argument")
	}
	if length > max {
		ExitError("too mush argument")
	}
	return length, args
}

// FileExists returns the exists of a file.
func FileExists(path string) bool {
	file, err := os.Lstat(path)
	if err != nil {
		return !os.IsNotExist(err)
	}
	return file.Mode().IsRegular()
}

// DirExists returns the exists of a directory.
func DirExists(path string) bool {
	file, err := os.Lstat(path)
	if err != nil {
		return !os.IsNotExist(err)
	}
	return file.Mode().IsDir()
}

// MakeDir creates a directory named path,
// along with any necessary parents, and returns nil,
// or else returns an error.
// The permission bits perm (before umask) are used for all
// directories that MkdirAll creates.
// If path is already a directory, MkdirAll does nothing
// and returns nil.
func MakeDir(path string, perm os.FileMode) {
	err := os.MkdirAll(path, perm)
	PrintError(err)
}

// ReadOrder reads content from a `order.txt` file.
// It read lines from the file and put them into a list.
// A line starts with `#` will be passed.
func ReadOrder(path string) *list.List {
	file, err := os.Open(path)
	PrintError(err)
	defer file.Close()
	reader := bufio.NewReader(file)
	l := list.New()
	for {
		str, err := reader.ReadString('\n')
		if err == io.EOF {
			break
		}
		str = strings.TrimSpace(str)
		if strings.HasPrefix(str, "#") {
			continue
		}
		l.PushBack(str)
	}
	return l
}

// DecodeName decodes a string to `GBK` chinese charset.
func DecodeName(flag uint16, name string) string {
	var decodeName string
	if flag == 0 {
		in := bytes.NewReader([]byte(name))
		decoder := transform.NewReader(in, simplifiedchinese.GB18030.NewDecoder())
		out, _ := io.ReadAll(decoder)
		decodeName = string(out)
	} else {
		decodeName = name
	}
	return decodeName
}

// GetFilePrefix gets a filename's prefix.
func GetFilePrefix(fileName string) string {
	filePrefix := strings.Split(filepath.Base(fileName), ".")[0]
	return filePrefix
}

// GetFileSuffix gets a filename's suffix.
func GetFileSuffix(fileName string) string {
	fileSuffix := strings.Split(filepath.Base(fileName), ".")[1]
	return fileSuffix
}

// ChTimeMode changes a file's access time、make time and permission.
func ChTimeMode(fileName string, atime time.Time, mtime time.Time, mode os.FileMode) {
	err := os.Chtimes(fileName, atime, mtime)
	PrintError(err)
	err = os.Chmod(fileName, mode)
	PrintError(err)
}

// KMP algorithms.
func KMP(str, pattern string) int {
	next := getNext(pattern)
	k := 0
	for i := 0; i < len(str); i++ {
		for k != 0 && str[i] != pattern[k] {
			k = next[k]
		}
		if str[i] == pattern[k] {
			k++
		}
		if k == len(pattern) {
			return i - k + 1
		}
	}
	return -1
}

// getNext gets a string's longest matching prefix.
func getNext(pattern string) []int {
	next := make([]int, len(pattern))
	k := 0
	for i := 2; i < len(pattern); i++ {
		for k != 0 && pattern[k] != pattern[i-1] {
			k = next[k]
		}
		if pattern[k] == pattern[i-1] {
			k++
		}
		next[i] = k
	}
	return next
}
