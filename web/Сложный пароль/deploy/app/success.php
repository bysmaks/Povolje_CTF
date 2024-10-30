<?php
session_start();

if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    header("Location: index.html");
    exit();
}
if ($_SESSION['username'] === 'test') {
    echo "<p> You just test user, go away! </p>";
    exit();
}

?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/x-icon" href="/favicon.ico?v=2">
    <link rel='shortcut icon' type='image/x-icon' href='/favicon.ico?v=2' />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACCESS GRANTED</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Consolas, monospace;
            background-color: #0a0a0a;
            color: #00ff00;
            overflow: hidden;
        }

        .success-container {
            text-align: center;
            max-width: 600px;
            padding: 20px;
            background-color: #000000;
            border-radius: 8px;
            border: 2px solid #00ff00;
            box-shadow: 0px 0px 15px rgba(0, 255, 0, 0.5);
        }

        h1 {
            color: #00ff00;
            font-size: 36px;
            margin-bottom: 20px;
            animation: blink 1s steps(2, start) infinite;
        }

        p {
            font-size: 18px;
            margin: 10px 0;
            color: #00ff00;
        }
        @keyframes blink {
            50% { opacity: 0; }
        }

        .continue-link {
            color: #00ff00;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            border: 1px solid #00ff00;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        .continue-link:hover {
            background-color: #1a1a1a;
            box-shadow: 0px 0px 10px #00ff00;
        }
    </style>
</head>
<body>
    <div class="success-container">
        <h1>ACCESS GRANTED</h1>
        <p>Authorization successful.</p>
        <p>Welcome, admin!</p>
        <?php 
            $FLAG = getenv("FLAG");
            echo "<p>".$FLAG."</p>";
        ?>
        
        <a href="logout.php" class="continue-link">Log Out</a>
    </div>
</body>
</html>
