<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/x-icon" href="/favicon.ico?v=2">
    <link rel='shortcut icon' type='image/x-icon' href='/favicon.ico?v=2' />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACCESS DENIED</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: 'Courier New', monospace;
            background-color: #000000;
            color: #00ff00;
            overflow: hidden;
            text-align: center;
            position: relative;
        }

        .error-container {
            width: 600px; 
            height: 350px; 
            padding: 20px;
            border: 1px solid #00ff00;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            background-color: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            overflow-y: auto;
        }

        .message {
            font-size: 18px;
            color: #00ff00;
            opacity: 0;
            transition: opacity 0.3s ease-in;
            margin: 10px 0;
        }

        .visible {
            opacity: 1;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .hacker-text {
            color: #ff0000;
            animation: blink 1s infinite;
            font-size: 32px;
            margin-bottom: 20px;
        }

        .background {
            position: absolute;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(0, 255, 0, 0.05) 20%, transparent 20%) repeat;
            background-size: 20px 20px;
            z-index: 0;
        }
        
        .fbi-alert {
            font-weight: bold;
            text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000;
        }
    </style>
</head>
<body>
    <div class="background"></div>

    <div class="error-container">
        <h1 class="hacker-text">ACCESS DENIED</h1>
        <p class="message" id="msg1">Unauthorized access attempt detected...</p>
        <p class="message" id="msg2">Tracing IP address...</p>
        <p class="message" id="ip-address">IP: <span class="hacker-text" id="ip">192.168.1.1</span></p>
        <p class="message" id="msg3">Locating...</p>
        <p class="message" id="location">Approximate location: <span class="hacker-text" id="geo-location">Unknown</span></p>
        <p class="message fbi-alert" id="msg4">Alerting FBI...</p>
        <p class="message" id="msg5">FBI units en route.</p>
    </div>

    <script>
        const messages = [
            document.getElementById('msg1'),
            document.getElementById('msg2'),
            document.getElementById('ip-address'),
            document.getElementById('msg3'),
            document.getElementById('location'),
            document.getElementById('msg4'),
            document.getElementById('msg5')
        ];

        function showMessages() {
            messages.forEach((msg, index) => {
                setTimeout(() => {
                    msg.classList.add('visible');
                }, index * 2000);
            });
        }

        function httpGet(theUrl)
            {
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.open( "GET", theUrl, false );
                xmlHttp.send( null );
                return xmlHttp.responseText;
            }

        var ip = httpGet("https://wtfismyip.com/text")
        document.getElementById("ip").textContent = ip;
        var location_user;
        fetch("http://ip-api.com/json/" + ip)
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                location_user = data["city"];
                document.getElementById("geo-location").textContent = location_user;
            })
            .catch(function () {
                console.log('Booo');
            });
        window.onload = showMessages;
    </script>

</body>
</html>
