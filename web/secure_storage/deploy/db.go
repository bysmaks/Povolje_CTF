package main

import (
	"context"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"
)

type DB struct {
	pool *pgxpool.Pool
}

var db DB

func InitDatabase(ctx context.Context) {
	pool, err := pgxpool.New(ctx, Config().PgUrl)
	if err != nil {
		panic(err)
	}
	db.pool = pool
}

func (db *DB) CreateUser(ctx context.Context, user User) (User, error) {
	q := `INSERT INTO users (username, password_hash, is_paid) VALUES ($1, $2, $3) RETURNING user_id, username, password_hash, is_paid`

	if err := db.pool.QueryRow(ctx, q, user.Username, user.Password, user.IsPaid).Scan(
		&user.UserId,
		&user.Username,
		&user.Password,
		&user.IsPaid,
	); err != nil {
		return User{}, err
	}
	return user, nil
}

func (db *DB) GetUserByUsername(ctx context.Context, username string) (User, error) {
	q := `SELECT user_id, username, password_hash, is_paid FROM users WHERE username = $1`

	var user User
	if err := db.pool.QueryRow(ctx, q, username).Scan(
		&user.UserId,
		&user.Username,
		&user.Password,
		&user.IsPaid,
	); err != nil {
		return User{}, err
	}
	return user, nil
}

func (db *DB) GetUserByUserId(ctx context.Context, userId int64) (User, error) {
	q := `SELECT user_id, username, password_hash, is_paid FROM users WHERE user_id = $1`

	var user User
	if err := db.pool.QueryRow(ctx, q, userId).Scan(
		&user.UserId,
		&user.Username,
		&user.Password,
		&user.IsPaid,
	); err != nil {
		return User{}, err
	}
	return user, nil
}

func (db *DB) Close() {
	db.pool.Close()
}

func isUniqueViolation(err error) bool {
	if pgErr, ok := err.(*pgconn.PgError); ok {
		return pgErr.Code == "23505"
	}
	return false
}
