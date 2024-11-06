from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def redirect_to_localhost():
    response = Response("", 302)
    response.headers['Content-type'] = 'text/plain'
    response.headers.add('Location', "http://localhost")
    return response


if __name__ == '__main__':
    app.run("0.0.0.0",port=5000)