package main

import (
	"os"
	"strconv"
)

type CFG struct {
	JwtSecret []byte
	Port      int
	PgUrl     string
}

var cfg CFG

func init() {
	cfg.JwtSecret = []byte(os.Getenv("JWT_SECRET"))

	portStr := os.Getenv("PORT")
	if portStr == "" {
		portStr = "8080"
	}

	port, err := strconv.Atoi(portStr)
	if err != nil {
		panic("can't parse PORT environment variable")
	}
	cfg.Port = port
	cfg.PgUrl = os.Getenv("PG_URL")
}

func Config() CFG {
	return cfg
}
