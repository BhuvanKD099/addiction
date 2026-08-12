-- AddictionSense Database Schema
CREATE DATABASE IF NOT EXISTS ai_drug_recovery_system;
USE ai_drug_recovery_system;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'DOCTOR', 'PATIENT', 'COUNSELOR') NOT NULL DEFAULT 'PATIENT',
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    experience_years INT NOT NULL DEFAULT 0,
    qualification VARCHAR(100) NOT NULL,
    hospital_name VARCHAR(100) DEFAULT 'AddictionSense Recovery Center',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Counselors Table
CREATE TABLE IF NOT EXISTS counselors (
    counselor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    experience_years INT NOT NULL DEFAULT 0,
    qualification VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Patients Table
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doctor_id INT NULL,
    counselor_id INT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    blood_group VARCHAR(10) DEFAULT 'O+',
    address TEXT,
    emergency_contact VARCHAR(20) NOT NULL,
    admission_date DATE NOT NULL,
    addiction_type VARCHAR(100) NOT NULL,
    addiction_severity VARCHAR(50) NOT NULL,
    treatment_status VARCHAR(50) DEFAULT 'IN_REHAB',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL,
    FOREIGN KEY (counselor_id) REFERENCES counselors(counselor_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Medical History Table
CREATE TABLE IF NOT EXISTS medical_histories (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    previous_addiction_history TEXT,
    duration_years FLOAT DEFAULT 1.0,
    previous_rehab_attempts INT DEFAULT 0,
    existing_diseases TEXT,
    mental_health_conditions TEXT,
    family_history TEXT,
    previous_medications TEXT,
    previous_counseling TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Daily Progress Table
CREATE TABLE IF NOT EXISTS progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    progress_date DATE NOT NULL,
    mood VARCHAR(50) NOT NULL,
    sleep_quality VARCHAR(50) DEFAULT 'Good',
    appetite VARCHAR(50) DEFAULT 'Normal',
    withdrawal_level INT NOT NULL CHECK (withdrawal_level BETWEEN 1 AND 10),
    craving_level INT NOT NULL CHECK (craving_level BETWEEN 1 AND 10),
    medication_adherence INT DEFAULT 1,
    counseling_attendance INT DEFAULT 1,
    stress_level INT DEFAULT 3,
    weight_kg FLOAT DEFAULT 70.0,
    bp_systolic INT DEFAULT 120,
    bp_diastolic INT DEFAULT 80,
    oxygen_level INT DEFAULT 98,
    recovery_score INT NOT NULL CHECK (recovery_score BETWEEN 0 AND 100),
    counselor_notes TEXT,
    doctor_remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Medications Table
CREATE TABLE IF NOT EXISTS medications (
    medication_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    morning TINYINT DEFAULT 1,
    afternoon TINYINT DEFAULT 0,
    night TINYINT DEFAULT 1,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    taken_status VARCHAR(20) DEFAULT 'TAKEN',
    side_effects TEXT,
    doctor_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Counseling Sessions Table
CREATE TABLE IF NOT EXISTS counseling_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    counselor_id INT NOT NULL,
    session_date DATE NOT NULL,
    discussion_topics TEXT,
    patient_participation VARCHAR(50) DEFAULT 'ACTIVE',
    mood_assessment VARCHAR(50) DEFAULT 'STABLE',
    session_summary TEXT,
    recommendations TEXT,
    homework TEXT,
    next_session_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (counselor_id) REFERENCES counselors(counselor_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Relapse Records Table
CREATE TABLE IF NOT EXISTS relapse_records (
    relapse_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    relapse_date DATE NOT NULL,
    cause TEXT,
    trigger_factors TEXT,
    stress_level INT DEFAULT 8,
    substance_used VARCHAR(100),
    counselor_notes TEXT,
    recovery_action TEXT,
    support_required TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. AI Relapse Predictions Table
CREATE TABLE IF NOT EXISTS relapse_assessments (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    risk_level VARCHAR(20) NOT NULL,
    risk_score INT NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
    confidence_score FLOAT DEFAULT 90.0,
    triggers TEXT,
    recommendations TEXT,
    counseling_frequency VARCHAR(50) DEFAULT 'Weekly',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. AddictionSense Assessments Table (Phase 1 AI Screening)
CREATE TABLE IF NOT EXISTS addiction_sense_assessments (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NULL,
    q_responses_json TEXT,
    questionnaire_score FLOAT NOT NULL,
    facial_stress_score FLOAT NOT NULL,
    blink_rate FLOAT DEFAULT 16.0,
    eye_openness FLOAT DEFAULT 0.8,
    voice_stress_score FLOAT DEFAULT 0.2,
    hand_tremor_score FLOAT DEFAULT 0.1,
    predicted_risk_level VARCHAR(20) NOT NULL,
    confidence_score FLOAT DEFAULT 92.5,
    risk_score INT NOT NULL,
    ai_explanation TEXT,
    triggers TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 13. Habit Tracker Table
CREATE TABLE IF NOT EXISTS habit_tracker (
    habit_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    habit_date DATE NOT NULL,
    clean_day INT DEFAULT 1,
    meditation INT DEFAULT 0,
    exercise INT DEFAULT 0,
    support_group INT DEFAULT 0,
    hydration_liters FLOAT DEFAULT 2.0,
    medication_taken INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 14. Educational Resources Table
CREATE TABLE IF NOT EXISTS educational_resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(150) NOT NULL,
    content_type VARCHAR(30) NOT NULL DEFAULT 'ARTICLE',
    description TEXT,
    resource_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 15. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(30) DEFAULT 'REMINDER',
    is_read TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 16. Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
