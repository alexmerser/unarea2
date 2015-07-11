# coding=utf-8
from flask import Flask
from unarea_core.settings.default import configure_app

app = Flask(__name__)
configure_app(app)

@app.route("/")
def hello():
    return "YOLO!!!"


@app.route("/about")
def about():
    return ("NGINX Plus is the HTTP operating system for the modern web application.\n"
            "     Whether you’re delivering content, streaming video or audio, or deploying complex web services, \n"
            "     NGINX Plus is the optimal platform to connect your users to your applications.\n"
            "\n"
            "The high-performance, efficient HTTP processing engine in NGINX Plus handles desktop, "
            "mobile, and API traffic equally well before switching and routing each request to the correct service.\n"
            " Companies deploy NGINX Plus to manage the complexities and pitfalls associated with HTTP and to make \n"
            "their web applications more responsive, scalable, fast, and secure.\n")


@app.route("/simple")
def simple():
    return ("Nginx is a fast and flexible HTTP server written in C.\n"
            "You can install it with the nginx package on Ubuntu:!\n")
