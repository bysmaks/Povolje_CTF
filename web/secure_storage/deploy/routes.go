package main

import (
	"database/sql"
	"encoding/json"
	"errors"
	"github.com/labstack/echo/v4"
	"github.com/labstack/gommon/log"
	"net/http"
	"path/filepath"
	"strings"
	"time"
)

type PageData struct {
	Username   string
	Password   string
	IsPaidUser bool

	UserRootFolderSize float64
	Files              []string
	Folders            []string

	FolderName string
	InFolder   bool

	ErrorMessage string
}

func setupRoutes(e *echo.Echo) {
	e.Static("/static", "static")

	e.GET("/", indexRouteGet, noLoginRequiredMW)
	e.GET("/signup", signUpRouteGet, noLoginRequiredMW)
	e.GET("/signin", signInRouteGet, noLoginRequiredMW)

	e.POST("/signup", signUpRoutePost, noLoginRequiredMW)
	e.POST("/signin", signInRoutePost, noLoginRequiredMW)

	e.GET("/storage", storageRouteGet, loginRequiredMW)

	e.GET("/subscription", subscriptionRouteGet, loginRequiredMW)

	e.GET("/file/:file", downloadFileRouteGet, loginRequiredMW)
	e.POST("/upload_file", uploadFileRoutePost, loginRequiredMW)

	e.GET("/folder/:folderName", folderRouteGet, loginRequiredMW, paidUserRequiredMW)
	e.GET("/file/:file/folder/:folderName", downloadFileFromFolderRouteGet, loginRequiredMW, paidUserRequiredMW)

	e.POST("/create_folder", createFolderRoutePost, loginRequiredMW, paidUserRequiredMW)
	e.POST("/upload_file/folder/:folderName", uploadFileToFolderRoutePost, loginRequiredMW, paidUserRequiredMW)

	e.GET("/logout", logoutRoute, loginRequiredMW)

}

func indexRouteGet(c echo.Context) error {
	return c.Render(http.StatusOK, "index.html", nil)
}

func signUpRouteGet(c echo.Context) error {
	return c.Render(http.StatusOK, "signup.html", nil)
}

func signUpRoutePost(c echo.Context) error {
	var (
		user = User{}
		ctx  = c.Request().Context()
	)

	data := c.FormValue("data")
	if len(data) == 0 {
		return c.Render(http.StatusBadRequest, "signup.html", PageData{
			ErrorMessage: "Bad request, change request and try again",
		})
	}

	if err := json.Unmarshal([]byte(data), &user); err != nil {
		return c.Render(http.StatusBadRequest, "signup.html", PageData{
			ErrorMessage: "Bad request, change request and try again",
		})
	}

	if len(user.Username) == 0 {
		return c.Render(http.StatusBadRequest, "signup.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Имя пользователя не может быть пустым",
		})
	}

	if len(user.Username) >= 50 {
		return c.Render(http.StatusBadRequest, "signup.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Имя пользователя не может быть длиннее 50 символов",
		})
	}

	if len(user.Password) == 0 {
		return c.Render(http.StatusBadRequest, "signup.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Пароль не может быть пустым",
		})
	}

	if len(user.Password) < 8 {
		return c.Render(http.StatusBadRequest, "signup.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Пароль должен быть длиннее 8 символов",
		})
	}

	var err error
	rawPassword := user.Password
	user.Password, err = HashPassword(rawPassword)
	if err != nil {
		log.Errorf("got err on password hashing: %+v", err)
		return c.Render(http.StatusBadRequest, "signup.html", PageData{
			Username:     user.Username,
			Password:     rawPassword,
			ErrorMessage: "Что-то пошло не так, попробуйте ещё раз, но чуть позже",
		})
	}

	createdUser, err := db.CreateUser(ctx, user)
	if err != nil {
		if isUniqueViolation(err) {
			return c.Render(http.StatusBadRequest, "signup.html", PageData{
				Username:     user.Username,
				Password:     rawPassword,
				ErrorMessage: "Имя пользователя уже занято",
			})
		}

		log.Errorf("got err on user creating: %+v", err)
		return c.Render(http.StatusInternalServerError, "signup.html", PageData{
			Username:     user.Username,
			Password:     rawPassword,
			ErrorMessage: "Что-то пошло не так, попробуйте ещё раз, но чуть позже",
		})
	}

	authToken, err := encodeUserInJwt(createdUser)
	if err != nil {
		log.Errorf("got err on user encode in jwt: %+v", err)
		return c.Render(http.StatusInternalServerError, "signup.html", PageData{
			Username:     createdUser.Username,
			Password:     rawPassword,
			ErrorMessage: "Что-то пошло не так, попробуйте ещё раз, но чуть позже",
		})
	}
	c.SetCookie(&http.Cookie{
		Name:    "auth",
		Value:   authToken,
		Expires: time.Now().AddDate(0, 0, 1),
	})

	return c.Redirect(http.StatusFound, "/storage")
}

func signInRouteGet(c echo.Context) error {
	return c.Render(http.StatusOK, "signin.html", nil)
}

func signInRoutePost(c echo.Context) error {
	var (
		user = User{}
		ctx  = c.Request().Context()
	)

	data := c.FormValue("data")
	if len(data) == 0 {
		return c.Render(http.StatusBadRequest, "signin.html", PageData{
			ErrorMessage: "Bad request, change request and try again",
		})
	}

	if err := json.Unmarshal([]byte(data), &user); err != nil {
		return c.Render(http.StatusBadRequest, "signin.html", PageData{
			ErrorMessage: "Bad request, change request and try again",
		})
	}

	if len(user.Username) == 0 {
		return c.Render(http.StatusBadRequest, "signin.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Имя пользователя не может быть пустым",
		})
	}

	if len(user.Password) == 0 {
		return c.Render(http.StatusBadRequest, "signin.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Пароль не может быть пустым",
		})
	}

	userFromDb, err := db.GetUserByUsername(ctx, user.Username)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return c.Render(http.StatusBadRequest, "signin.html", PageData{
				Username:     user.Username,
				Password:     user.Password,
				ErrorMessage: "Неверные имя пользователя или пароль",
			})
		}

		log.Errorf("got err on get user by username: %+v", err)
		return c.Render(http.StatusInternalServerError, "signin.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Что-то пошло не так, попробуйте ещё раз, но чуть позже",
		})
	}

	if !CheckPassword(userFromDb.Password, user.Password) {
		return c.Render(http.StatusBadRequest, "signin.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Неверные имя пользователя или пароль",
		})
	}

	authToken, err := encodeUserInJwt(userFromDb)
	if err != nil {
		log.Errorf("got err on encoding user in jwt: %+v", err)
		return c.Render(http.StatusInternalServerError, "signin.html", PageData{
			Username:     user.Username,
			Password:     user.Password,
			ErrorMessage: "Что-то пошло не так, попробуйте ещё раз, но чуть позже",
		})
	}
	c.SetCookie(&http.Cookie{
		Name:    "auth",
		Value:   authToken,
		Expires: time.Now().AddDate(0, 0, 1),
	})

	return c.Redirect(http.StatusFound, "/storage")
}

func storageRouteGet(c echo.Context) error {
	var (
		user = c.Get("user").(User)
	)

	userRootPath := GetUserRootPath(user)

	if err := CreateFolder(userRootPath); err != nil {
		return c.Render(http.StatusInternalServerError, "storage.html", PageData{
			ErrorMessage: "Что-то пошло не так, попробуй вернуться чуть позже",
		})
	}

	// Получаем общий вес хранилища юзера
	userRootFolderSize, err := FolderSize(userRootPath)
	if err != nil {
		return c.Render(http.StatusInternalServerError, "storage.html", PageData{
			ErrorMessage: "Что-то пошло не так, попробуй вернуться чуть позже",
		})
	}

	files, folders, err := ListFilesAndDirectories(userRootPath)
	if err != nil {
		return c.Render(http.StatusInternalServerError, "storage.html", PageData{
			ErrorMessage: "Что-то пошло не так, попробуй вернуться чуть позже",
		})
	}

	errMsg := c.QueryParam("error")
	if errMsg != "" {
		return c.Render(http.StatusOK, "storage.html", PageData{
			Username:           user.Username,
			IsPaidUser:         user.IsPaid,
			UserRootFolderSize: userRootFolderSize,
			Files:              files,
			Folders:            folders,
			ErrorMessage:       errMsg,
		})
	}

	return c.Render(http.StatusOK, "storage.html", PageData{
		Username:           user.Username,
		IsPaidUser:         user.IsPaid,
		UserRootFolderSize: userRootFolderSize,
		Files:              files,
		Folders:            folders,
	})
}

func uploadFileRoutePost(c echo.Context) error {
	var (
		user         = c.Get("user").(User)
		userRootPath = GetUserRootPath(user)
	)

	file, err := c.FormFile("file")
	if err != nil {
		return c.Redirect(http.StatusFound, "/storage?error=Что-то пошло не так, попробуйте ещё раз, но чуть позже")
	}

	if file.Size > 5*1024 {
		return c.Redirect(http.StatusFound, "/storage?error=Нельзя загрузить файл больше 5kb")
	}

	if err := UploadFile(userRootPath, file); err != nil {
		log.Errorf("got err on upload file: %+v", err)
		return c.Redirect(http.StatusFound, "/storage?error=Что-то пошло не так, попробуйте ещё раз, но чуть позже")
	}

	return c.Redirect(http.StatusFound, "/storage")
}

func downloadFileRouteGet(c echo.Context) error {
	var (
		user         = c.Get("user").(User)
		userRootPath = GetUserRootPath(user)
		file         = c.Param("file")
	)

	if file == "" {
		return c.Redirect(http.StatusFound, "/storage?error=Имя файла для скачивания не может быть пустым")
	}

	// Prevent path traversal
	fileSplit := strings.Split(file, "/")

	return c.File(filepath.Join(userRootPath, fileSplit[len(fileSplit)-1]))
}

func createFolderRoutePost(c echo.Context) error {
	var (
		user         = c.Get("user").(User)
		userRootPath = GetUserRootPath(user)
		folder       = c.FormValue("folderName")
	)

	if folder == "" {
		return c.Redirect(http.StatusFound, "/storage?error=Название папки не может быть пустым")
	}

	if err := CreateFolder(userRootPath); err != nil {
		return c.Redirect(http.StatusFound, "/storage?error=Что-то пошло не так попробуйте ещё раз, но чуть позже")
	}

	if err := CreateFolder(filepath.Join(userRootPath, folder)); err != nil {
		return c.Redirect(http.StatusFound, "/storage?error=Что-то пошло не так попробуйте ещё раз, но чуть позже")
	}

	return c.Redirect(http.StatusFound, "/storage")
}

func folderRouteGet(c echo.Context) error {
	var (
		user         = c.Get("user").(User)
		userRootPath = GetUserRootPath(user)
		folder       = c.Param("folderName")
	)

	userRootFolderSize, err := FolderSize(userRootPath)
	if err != nil {
		return c.Render(http.StatusInternalServerError, "storage.html", PageData{
			ErrorMessage: "Что-то пошло не так, попробуй вернуться чуть позже",
		})
	}

	if folder == "" {
		return c.Redirect(http.StatusFound, "/storage?error=Название папки не может быть пустым")
	}

	files, folders, err := ListFilesAndDirectories(filepath.Join(userRootPath, folder))
	if err != nil {
		return c.Redirect(http.StatusFound, "/storage?error=Что-то пошло не так попробуйте ещё раз, но чуть позже")
	}

	return c.Render(http.StatusOK, "storage.html", PageData{
		Username:           user.Username,
		IsPaidUser:         user.IsPaid,
		UserRootFolderSize: userRootFolderSize,
		Files:              files,
		Folders:            folders,
		FolderName:         folder,
		InFolder:           true,
	})
}

func uploadFileToFolderRoutePost(c echo.Context) error {
	var (
		user         = c.Get("user").(User)
		userRootPath = GetUserRootPath(user)
		folder       = c.Param("folderName")
	)

	file, err := c.FormFile("file")
	if err != nil {
		return c.Redirect(http.StatusFound, "/storage?error=Что-то пошло не так, попробуйте ещё раз, но чуть позже")
	}

	if file.Size > 5*1024 {
		return c.Redirect(http.StatusFound, "/storage?error=Нельзя загрузить файл больше 5kb")
	}

	if err := UploadFile(filepath.Join(userRootPath, folder), file); err != nil {
		log.Errorf("got err on upload file: %+v", err)
		return c.Redirect(http.StatusFound, "/storage?error=Что-то пошло не так, попробуйте ещё раз, но чуть позже")
	}

	return c.Redirect(http.StatusFound, "/folder/"+folder)
}

func downloadFileFromFolderRouteGet(c echo.Context) error {
	var (
		user         = c.Get("user").(User)
		userRootPath = GetUserRootPath(user)
		file         = c.Param("file")
		folderName   = c.Param("folderName")
	)

	if file == "" {
		return c.Redirect(http.StatusFound, "/storage?error=Имя файла для скачивания не может быть пустым")
	}

	if folderName == "" {
		return c.Redirect(http.StatusFound, "/storage?error=Имя папки не может быть пустым")
	}

	// Prevent path traversal
	fileSplit := strings.Split(file, "/")

	return c.File(filepath.Join(userRootPath, folderName, fileSplit[len(fileSplit)-1]))
}

func subscriptionRouteGet(c echo.Context) error {
	var (
		user = c.Get("user").(User)
	)

	return c.Render(http.StatusOK, "subscription.html", PageData{
		Username: user.Username,
	})
}

func logoutRoute(c echo.Context) error {
	c.SetCookie(&http.Cookie{
		Name:   "auth",
		MaxAge: -1,
	})
	return c.Redirect(http.StatusFound, "/")
}
