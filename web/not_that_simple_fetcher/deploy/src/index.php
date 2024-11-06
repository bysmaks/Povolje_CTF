<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SimpleFetcher</title>
    <!-- Bootstrap CSS -->
    <link href="static/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="static/css/styles.css">
</head>
<body class="bg-light">
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'GET' && $_SERVER['REQUEST_URI'] === '/' && ($_SERVER['REMOTE_ADDR'] === '127.0.0.1' || $_SERVER['REMOTE_ADDR'] === '::1')) {
        echo '<div class="alert alert-info">' . getenv('FLAG') . '</div>';
    }
    ?>
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
        <div class="card p-4" style="width: 100%; max-width: 400px;">
            <h1 class="card-title text-center text-primary">Fetch sites without any restrictions!</h1>
            <form id="fetchForm" method="post" action="">
                <div class="form-group">
                    <label for="url">URL</label>
                    <input type="text" class="form-control" id="url" name="url" required>
                </div>
                <button type="submit" class="btn btn-primary mt-3">Fetch</button>
            </form>
            <div id="result" class="mt-3">
                <?php
                if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url'])) {
                    $url = $_POST['url'];
                    // Allow only http and https URI schemes
                    if (!preg_match('/^(http|https):\/\//i', $url) || preg_match('/localhost|127\.|^172\./i', $url)) {
                        echo '<div class="alert alert-danger">Denied by WAF</div>';
                    } else {
                        // Fetch the URL content
                        $ch = curl_init();
                        curl_setopt($ch, CURLOPT_URL, $url);
                        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
                        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1); // Follow redirects
                        $output = curl_exec($ch);
                        curl_close($ch);
                
                        if ($output === false) {
                            echo '<div class="alert alert-danger">Error fetching URL</div>';
                        } else {
                            echo '<div class="alert alert-success">' . htmlspecialchars($output) . '</div>';
                        }
                    }
                }
                ?>
            </div>
        </div>
    </div>
</body>
</html>
