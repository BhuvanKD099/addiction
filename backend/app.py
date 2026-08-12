from flask import Flask
from flask_cors import CORS
from config import Config

from utils.database import mysql
from auth.password import bcrypt
from auth.jwt_handler import jwt

from routes.auth import auth_bp
from routes.doctors import doctor_bp
from routes.patients import patient_bp
from routes.appointments import appointment_bp
from routes.progress import progress_bp
from routes.dashboard import dashboard_bp
from routes.relapse import relapse_bp
from routes.reports import reports_bp
from routes.medications import medications_bp
from routes.counselling import counselling_bp
from routes.addictionsense import addictionsense_bp
from routes.counselors import counselors_bp
from routes.resources import resources_bp
from routes.notifications import notifications_bp
from routes.ai import ai_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

# Initialize Extensions
mysql.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(doctor_bp, url_prefix="/doctors")
app.register_blueprint(patient_bp, url_prefix="/patients")
app.register_blueprint(appointment_bp, url_prefix="/appointments")
app.register_blueprint(progress_bp, url_prefix="/progress")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(relapse_bp, url_prefix="/relapse")
app.register_blueprint(reports_bp, url_prefix="/reports")
app.register_blueprint(medications_bp, url_prefix="/medications")
app.register_blueprint(counselling_bp, url_prefix="/counselling")
app.register_blueprint(counselling_bp, url_prefix="/counseling", name="counseling_alias")
app.register_blueprint(addictionsense_bp, url_prefix="/addictionsense")
app.register_blueprint(counselors_bp, url_prefix="/counselors")
app.register_blueprint(resources_bp, url_prefix="/resources")
app.register_blueprint(notifications_bp, url_prefix="/notifications")
app.register_blueprint(ai_bp, url_prefix="/ai")


@app.route("/")
def home():
    return {
        "system": "AddictionSense AI Recovery Management System API",
        "status": "Online",
        "version": "2.0.0"
    }, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
