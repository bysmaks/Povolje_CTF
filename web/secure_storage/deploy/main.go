package main

import (
	"context"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"html/template"
)

func main() {
	ctx := context.Background()
	// Echo instance
	e := echo.New()
	e.Renderer = &Template{
		templates: template.Must(template.ParseGlob("templates/*.html")),
	}
	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	InitDatabase(ctx)

	// Routes
	setupRoutes(e)

	// Start server
	e.Logger.Fatal(e.Start(":9000"))
}
