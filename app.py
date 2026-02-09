import os
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail

from routes.auth_routes import auth_bp
from routes.question_routes import question_bp
from routes.web_routes import web_bp
from routes.youtube_routes import youtube_bp
from routes.quiz_routes import quiz_bp
from routes.compains_routes import compains_bp
from routes.result_routes import result_bp
from routes.s3_routes import upload_bp
from routes.user_token_routes import token_bp
from mangum import Mangum

app = Flask(__name__)

# -------------------- CONFIG --------------------
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")        # smtp.gmail.com
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587)) # 587
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

# -------------------- INIT EXTENSIONS --------------------
mail = Mail(app)
app.mail = mail

# -------------------- CORS --------------------
CORS(
    app,
    supports_credentials=True,
    origins=["http://127.0.0.1:5173"]
)

handler = Mangum(app)

# -------------------- ROUTES --------------------

@app.route("/", methods=["GET"])
def home():
    return {
        "message": "Welcome to Smart Quiz API",
        "status": "online",
        "docs": "/api",
        "version": "1.0.0"
    }, 200


app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(question_bp, url_prefix="/api")
app.register_blueprint(web_bp, url_prefix="/api")
app.register_blueprint(youtube_bp, url_prefix="/api")
app.register_blueprint(quiz_bp, url_prefix="/api")
app.register_blueprint(compains_bp, url_prefix="/api")
app.register_blueprint(result_bp, url_prefix="/api")

app.register_blueprint(upload_bp, url_prefix="/api")

app.register_blueprint(token_bp, url_prefix="/api")

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True, port=5050)


