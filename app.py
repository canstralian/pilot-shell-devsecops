import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_talisman import Talisman

load_dotenv()

FLASK_ENV = os.environ.get("FLASK_ENV", "production")

app = Flask(__name__)

# --------------------------------------------------------------------------- #
# Configuration                                                                #
# --------------------------------------------------------------------------- #

if FLASK_ENV == "development":
    app.config.update(
        DEBUG=True,
        TESTING=False,
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production"),
        DATABASE_URL=os.environ.get("DATABASE_URL", "sqlite:///dev.db"),
    )
    logging.basicConfig(level=logging.DEBUG)
else:
    # Production: require SECRET_KEY to be set explicitly; never fall back to a
    # hard-coded value so that a misconfigured deployment fails loudly.
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable must be set in production")

    app.config.update(
        DEBUG=False,
        TESTING=False,
        SECRET_KEY=secret_key,
        DATABASE_URL=os.environ.get("DATABASE_URL", "sqlite:///prod.db"),
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

# --------------------------------------------------------------------------- #
# Security headers via flask-talisman                                          #
# --------------------------------------------------------------------------- #

CSP = {
    "default-src": "'self'",
    "script-src": "'self'",
    "style-src": "'self'",
    "img-src": ["'self'", "data:"],
    "font-src": "'self'",
    "object-src": "'none'",
    "frame-ancestors": "'none'",
}

# Hugging Face Spaces terminates TLS at the edge, so force_https must be
# disabled inside the container; HSTS is still sent to the browser.
talisman = Talisman(
    app,
    force_https=False,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    strict_transport_security_include_subdomains=True,
    strict_transport_security_preload=True,
    content_security_policy=CSP,
    referrer_policy="strict-origin-when-cross-origin",
    feature_policy={
        "geolocation": "'none'",
        "microphone": "'none'",
        "camera": "'none'",
    },
    frame_options="DENY",
    x_content_type_options=True,
    x_xss_protection=False,
    session_cookie_secure=FLASK_ENV != "development",
    session_cookie_http_only=True,
    session_cookie_samesite="Lax",
)

# --------------------------------------------------------------------------- #
# Routes                                                                       #
# --------------------------------------------------------------------------- #


@app.route("/")
def index():
    return jsonify({"status": "ok", "env": FLASK_ENV})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


# --------------------------------------------------------------------------- #
# Entry-point (development only — production uses Gunicorn)                   #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=FLASK_ENV == "development")
