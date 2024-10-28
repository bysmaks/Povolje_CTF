<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if (($username === 'admin' && md5($password) == "0e123456789101112131415161718192") || ($username === 'test' && md5($password) == '098f6bcd4621d373cade4e832627b4f6')) {
        $_SESSION['logged_in'] = true;
        $_SESSION['username'] = $username;
        header("Location: success.php");
    } else {
        header("Location: error.php");
        exit();
    }
} else {
    header("Location: index.html");
    exit();
}
?>
