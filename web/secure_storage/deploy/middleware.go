package main

import (
	"fmt"
	"github.com/golang-jwt/jwt"
	"github.com/labstack/echo/v4"
	"net/http"
)

func loginRequiredMW(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		authCookie, err := c.Cookie("auth")
		if err != nil {
			return c.Redirect(http.StatusFound, "/signin")
		}

		token, err := jwt.Parse(authCookie.Value, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
			}
			return Config().JwtSecret, nil
		})

		if err != nil || !token.Valid {
			c.SetCookie(&http.Cookie{
				Name:   "auth",
				MaxAge: -1,
			})
			return c.Redirect(http.StatusFound, "/signin")
		}

		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok {
			c.SetCookie(&http.Cookie{
				Name:   "auth",
				MaxAge: -1,
			})
			return c.Redirect(http.StatusFound, "/signin")
		}

		userID, ok := claims["id"].(float64)
		if !ok {
			c.SetCookie(&http.Cookie{
				Name:   "auth",
				MaxAge: -1,
			})
			return c.Redirect(http.StatusFound, "/signin")
		}

		user, err := db.GetUserByUserId(c.Request().Context(), int64(userID))
		if err != nil {
			c.SetCookie(&http.Cookie{
				Name:   "auth",
				MaxAge: -1,
			})
			return c.Redirect(http.StatusFound, "/signin")
		}

		c.Set("user", user)
		return next(c)
	}
}

func noLoginRequiredMW(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		_, err := c.Cookie("auth")
		if err == nil {
			return c.Redirect(http.StatusFound, "/storage")
		}

		return next(c)
	}
}

func paidUserRequiredMW(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		// Get user from context
		user, ok := c.Get("user").(User)
		if !ok {
			return c.Redirect(http.StatusFound, "/signin")
		}

		if !user.IsPaid {
			return c.Redirect(http.StatusFound, "/storage?error=Работа с папками доступна только платным юзерам")
		}

		return next(c)
	}
}
