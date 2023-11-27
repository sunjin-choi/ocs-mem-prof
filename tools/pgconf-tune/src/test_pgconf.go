package main

import (
	"fmt"

	"github.com/quasoft/pgconf/conf"
)

func main() {
	c, err := conf.Open("/etc/postgresql/13/main/postgresql.conf")
	if err != nil {
		panic("Could not open conf file: " + err.Error())
	}

	// StringK automatically dequotes values
	dest, err := c.StringK("log_destination")
	if err != nil || dest != "syslog" {
		// If key was not set or has the wrong value
		fmt.Println("log_destination value is not what we want, changing it now")
		c.SetStringK("log_destination", "syslog") // SetStringK automatically quotes values if necessary
	}

	err = c.WriteFile("postgresql.conf.tmp", 0644)
	if err != nil {
		panic("Could not save file: " + err.Error())
	}
}
