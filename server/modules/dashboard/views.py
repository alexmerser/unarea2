# -*- coding: utf-8 -*-

__author__ = "lissomort"

from flask import Blueprint, render_template



mod = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates')

# main
@mod.route('/')
def main():
    return "DASH"
