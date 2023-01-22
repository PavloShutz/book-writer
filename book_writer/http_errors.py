"""Describing different HTTP errors."""

from flask import render_template


def page_not_found(e):
    """Returning page with 404 error code"""
    return render_template("errors/404.html"), 404


def internal_server_error(e):
    """Returning page with 500 error code"""
    return render_template("errors/500.html"), 500
