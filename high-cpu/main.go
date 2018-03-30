package main

import (
	"crypto/md5"
	"fmt"
	"time"
)

func main() {
	fmt.Println("starting hashing")

	stop := make(chan bool)

	go func() {
		hash := md5.New()

		t := []byte("test")
		for {
			select {
			case <-stop:
				return
			default:
				time.Sleep(time.Second * 1)
				for i := 0; i < 20; i++ {
					t = hash.Sum(t)
					fmt.Printf("%x\n", t)
				}
			}
		}
	}()

	time.Sleep(time.Second * 20)
	stop <- true
}
