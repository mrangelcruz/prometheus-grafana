import os
import time
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Counter, make_wsgi_app, ProcessCollector, generate_latest

# Initialize Flask
app = Flask(__name__)

# --- Prometheus metrics ---
REQUEST_COUNT = Counter('flask_requests_total', 'Total number of requests')
PAGE_VIEWS = Counter('flask_page_views_total', 'Page views per endpoint', ['endpoint'])

# Collect Python process-level metrics
ProcessCollector(namespace='python_logger')

# --- Hooks ---
@app.before_request
def before_request():
    REQUEST_COUNT.inc()

# --- Routes ---
@app.route('/')
def home():
    PAGE_VIEWS.labels(endpoint="home").inc()
    return "Welcome to Flask + Prometheus! Visit /login, /dashboard, or /stress/*."

@app.route('/login')
def login():
    PAGE_VIEWS.labels(endpoint="login").inc()
    return "Login page"

@app.route('/dashboard')
def dashboard():
    PAGE_VIEWS.labels(endpoint="dashboard").inc()
    username = session.get('username', 'Guest')
    return f"Welcome to the Dashboard, {username}!"

# --- Stress test routes ---
@app.route('/stress/cpu')
def stress_cpu():
    start = time.time()
    while time.time() - start < 10:  # Burn CPU for 10s
        _ = [x**2 for x in range(10000)]
    return "🔥 CPU stress triggered for 10 seconds"

@app.route('/stress/mem')
def stress_mem():
    big_list = [b"x" * 1024 * 1024 for _ in range(100)]  # ~100 MB
    return f"🧠 Allocated {len(big_list)} MB in memory"

@app.route('/stress/login-requests')
def stress_login_requests():
    command = "for i in {1..100}; do curl -s http://localhost:5000/login > /dev/null; done"
    subprocess.run(command, shell=True, check=True)
    return "⚡ Generated 100 requests to /login"

@app.route('/metrics')
def metrics():
    return generate_latest()

# --- Mount Prometheus /metrics endpoint cleanly ---
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# --- Run app ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
