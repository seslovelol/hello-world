package lib

import "testing"

func TestLogger(t *testing.T) {
	v := "World"
	PrintInfo("Hello, %v", v)
}
