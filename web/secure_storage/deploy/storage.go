package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"math"
	"mime/multipart"
	"os"
	"path/filepath"
	"strings"
)

const usersFoldersPath = "users"

func init() {
	if err := CreateFolder(usersFoldersPath); err != nil {
		panic(err)
	}
}

// FolderSize - возвращает размер папки в килобайтах
func FolderSize(path string) (float64, error) {
	var size int64
	err := filepath.Walk(path, func(_ string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			size += info.Size()
		}
		return nil
	})

	return TruncateFloat64(float64(size)/1024, 2), err
}

func ListFilesAndDirectories(folderPath string) ([]string, []string, error) {
	var files []string
	var directories []string

	info, err := os.Stat(folderPath)
	if os.IsNotExist(err) || !info.IsDir() {
		return nil, nil, fmt.Errorf("folder does not exist or is not a directory: %s", folderPath)
	}

	items, err := os.ReadDir(folderPath)
	if err != nil {
		return nil, nil, err
	}

	for _, item := range items {
		if item.IsDir() {
			directories = append(directories, item.Name())
		} else {
			files = append(files, item.Name())
		}
	}

	return files, directories, nil
}

func FolderExists(path string) bool {
	info, err := os.Stat(path)
	if os.IsNotExist(err) {
		return false
	}
	return info.IsDir()
}

func CreateFolder(path string) error {
	if !FolderExists(path) {
		err := os.Mkdir(path, os.ModePerm)
		if err != nil {
			return err
		}
	}
	return nil
}

func UploadFile(path string, file *multipart.FileHeader) error {
	f, err := file.Open()
	if err != nil {
		return err
	}
	defer func(f multipart.File) { _ = f.Close() }(f)

	fileContent, err := io.ReadAll(f)
	if err != nil {
		return err
	}

	// Prevent path traversal
	fileNameSplit := strings.Split(file.Filename, "/")

	if err := os.WriteFile(filepath.Join(path, fileNameSplit[len(fileNameSplit)-1]), fileContent, 0444); err != nil {
		return err
	}
	return nil
}

func GetUserRootPath(user User) string {
	return fmt.Sprintf("%s/%s_%s", usersFoldersPath, user.Username, hashString(user.Username))
}

func hashString(input string) string {
	hasher := sha256.New()
	hasher.Write([]byte(input))
	hash := hasher.Sum(nil)
	return hex.EncodeToString(hash)
}

func TruncateFloat64(value float64, precision int) float64 {
	multiplier := math.Pow(10, float64(precision))
	truncated := math.Trunc(value*multiplier) / multiplier
	if math.IsNaN(truncated) {
		return 0.0
	}
	return truncated
}
