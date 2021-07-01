package downloadpackage 

import (
	"lib"
	"fmt"
)

func GetArg() {
	fmt.Println("Get")
}

func main() {
	GetArg()
	a := 1
	lib.PrintInfo("%v", a)
}
