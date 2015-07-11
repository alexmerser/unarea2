# coding=utf-8
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/about")
def hello():
    return ("NGINX Plus is the HTTP operating system for the modern web application.\n"
            "     Whether you’re delivering content, streaming video or audio, or deploying complex web services, \n"
            "     NGINX Plus is the optimal platform to connect your users to your applications.\n"
            "\n"
            "The high-performance, efficient HTTP processing engine in NGINX Plus handles desktop, "
            "mobile, and API traffic equally well before switching and routing each request to the correct service.\n"
            " Companies deploy NGINX Plus to manage the complexities and pitfalls associated with HTTP and to make \n"
            "their web applications more responsive, scalable, fast, and secure.\n")
