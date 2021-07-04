package lib

import (
	"fmt"
	"os"
)

func GetArg() (int, []string) {
	fmt.Println(os.Args)
	args := []string{"a", "b"}
	length := len(args)
	return length, args
}
