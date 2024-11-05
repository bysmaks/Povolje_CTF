package main

type User struct {
	UserId   int64  `json:"user_id"`
	Username string `json:"username"`
	Password string `json:"password"`
	IsPaid   bool   `json:"is_paid"`
}
