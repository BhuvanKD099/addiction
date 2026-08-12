-- AddictionSense Seed Data
USE ai_drug_recovery_system;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE audit_logs;
TRUNCATE TABLE notifications;
TRUNCATE TABLE educational_resources;
TRUNCATE TABLE habit_tracker;
TRUNCATE TABLE addiction_sense_assessments;
TRUNCATE TABLE relapse_assessments;
TRUNCATE TABLE relapse_records;
TRUNCATE TABLE appointments;
TRUNCATE TABLE counseling_sessions;
TRUNCATE TABLE medications;
TRUNCATE TABLE progress;
TRUNCATE TABLE medical_histories;
TRUNCATE TABLE patients;
TRUNCATE TABLE counselors;
TRUNCATE TABLE doctors;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Users (Password: password123)
INSERT INTO users (user_id, full_name, email, password_hash, role, status) VALUES
(1, 'System Admin', 'admin@recovery.org', '$2b$12$4Plx5Q38cBW8kvtlA6vzDeNFlIDeQPkGWp0SFzEXBOsMrky490/A6', 'ADMIN', 'ACTIVE'),
(2, 'Dr. Sarah Jenkins', 'sarah.jenkins@hospital.org', '$2b$12$4Plx5Q38cBW8kvtlA6vzDeNFlIDeQPkGWp0SFzEXBOsMrky490/A6', 'DOCTOR', 'ACTIVE'),
(3, 'Dr. Robert Chen', 'robert.chen@hospital.org', '$2b$12$4Plx5Q38cBW8kvtlA6vzDeNFlIDeQPkGWp0SFzEXBOsMrky490/A6', 'DOCTOR', 'ACTIVE'),
(4, 'Counselor Lisa Ray', 'lisa.ray@counseling.org', '$2b$12$4Plx5Q38cBW8kvtlA6vzDeNFlIDeQPkGWp0SFzEXBOsMrky490/A6', 'COUNSELOR', 'ACTIVE'),
(5, 'John Doe', 'john.doe@gmail.com', '$2b$12$4Plx5Q38cBW8kvtlA6vzDeNFlIDeQPkGWp0SFzEXBOsMrky490/A6', 'PATIENT', 'ACTIVE'),
(6, 'Emily Watson', 'emily.watson@gmail.com', '$2b$12$4Plx5Q38cBW8kvtlA6vzDeNFlIDeQPkGWp0SFzEXBOsMrky490/A6', 'PATIENT', 'ACTIVE'),
(7, 'Michael Brown', 'michael.brown@gmail.com', '$2b$12$4Plx5Q38cBW8kvtlA6vzDeNFlIDeQPkGWp0SFzEXBOsMrky490/A6', 'PATIENT', 'ACTIVE');

-- 2. Doctors
INSERT INTO doctors (doctor_id, user_id, specialization, phone, experience_years, qualification, hospital_name) VALUES
(1, 2, 'Addiction Psychiatry', '+1 555-0101', 12, 'MD, PhD in Neuropsychiatry', 'Apollo Recovery Center'),
(2, 3, 'Substance Rehabilitation', '+1 555-0102', 8, 'MD, Board Certified Addictionology', 'Practo Care Rehabilitation');

-- 3. Counselors
INSERT INTO counselors (counselor_id, user_id, specialization, phone, experience_years, qualification) VALUES
(1, 4, 'Cognitive Behavioral Therapy', '+1 555-0301', 7, 'M.Sc. Clinical Psychology, Licensed Counselor');

-- 4. Patients
INSERT INTO patients (patient_id, user_id, doctor_id, counselor_id, age, gender, phone, blood_group, address, emergency_contact, admission_date, addiction_type, addiction_severity, treatment_status) VALUES
(1, 5, 1, 1, 32, 'MALE', '+1 555-0201', 'O+', '124 Maple St, Springfield', '+1 555-9901', '2026-06-01', 'Alcohol', 'SEVERE', 'IN_REHAB'),
(2, 6, 1, 1, 28, 'FEMALE', '+1 555-0202', 'A+', '456 Oak Ave, Riverdale', '+1 555-9902', '2026-06-15', 'Opioids', 'SEVERE', 'IN_REHAB'),
(3, 7, 2, 1, 41, 'MALE', '+1 555-0203', 'B+', '789 Pine Rd, Hill Valley', '+1 555-9903', '2026-07-01', 'Cannabis', 'MODERATE', 'OUTPATIENT');

-- 5. Medical History
INSERT INTO medical_histories (history_id, patient_id, previous_addiction_history, duration_years, previous_rehab_attempts, existing_diseases, mental_health_conditions, family_history, previous_medications, previous_counseling) VALUES
(1, 1, 'Heavy alcohol consumption (6-8 drinks daily)', 5.5, 1, 'Hypertension', 'Generalized Anxiety Disorder', 'Father had history of alcoholism', 'Disulfiram', 'CBT 6 sessions in 2024'),
(2, 2, 'Prescription opioid misuse following knee surgery', 2.0, 0, 'Chronic lower back pain', 'Mild Depression', 'None reported', 'Tramadol, Oxycodone', 'None');

-- 6. Daily Progress Logs
INSERT INTO progress (progress_id, patient_id, progress_date, mood, sleep_quality, appetite, withdrawal_level, craving_level, medication_adherence, counseling_attendance, stress_level, weight_kg, bp_systolic, bp_diastolic, oxygen_level, recovery_score, counselor_notes, doctor_remarks) VALUES
(1, 1, '2026-07-28', 'Good', 'Good', 'Normal', 3, 4, 1, 1, 3, 74.5, 122, 80, 98, 75, 'Patient showing improved coping mechanisms.', 'Stable baseline.'),
(2, 1, '2026-08-01', 'Excellent', 'Very Good', 'Good', 2, 2, 1, 1, 2, 75.0, 120, 78, 99, 85, 'Significant craving reduction.', 'Continue current dosage.'),
(3, 2, '2026-07-29', 'Bad', 'Poor', 'Low', 7, 8, 0, 1, 8, 58.2, 134, 88, 97, 42, 'High craving following stress.', 'Increased monitoring protocol.'),
(4, 2, '2026-08-02', 'Normal', 'Fair', 'Normal', 5, 6, 1, 1, 5, 58.5, 126, 82, 98, 58, 'Withdrawal symptoms stabilizing.', 'Keep daily checkins active.');

-- 7. Medications
INSERT INTO medications (medication_id, patient_id, doctor_id, medication_name, dosage, frequency, morning, afternoon, night, start_date, end_date, status, taken_status, side_effects, doctor_notes) VALUES
(1, 1, 1, 'Naltrexone', '50mg', 'Once Daily', 1, 0, 0, '2026-06-02', '2026-12-02', 'ACTIVE', 'TAKEN', 'Mild morning nausea', 'Take with food'),
(2, 1, 1, 'Acamprosate', '333mg', 'Three times daily', 1, 1, 1, '2026-06-02', '2026-12-02', 'ACTIVE', 'TAKEN', 'None', 'Maintains GABA balance'),
(3, 2, 1, 'Buprenorphine', '8mg', 'Twice daily', 1, 0, 1, '2026-06-16', '2026-11-16', 'ACTIVE', 'TAKEN', 'Drowsiness', 'Do not alter dose without consultation');

-- 8. Counseling Sessions
INSERT INTO counseling_sessions (session_id, patient_id, counselor_id, session_date, discussion_topics, patient_participation, mood_assessment, session_summary, recommendations, homework, next_session_date) VALUES
(1, 1, 1, '2026-07-25', 'Stress triggers & peer pressure refusal skills', 'ACTIVE', 'CALM', 'Patient engaged deeply in roleplay scenarios.', 'Practice deep breathing when craving strikes', 'Journal evening craving triggers', '2026-08-08'),
(2, 2, 1, '2026-07-30', 'Managing physical withdrawal discomfort & mood swings', 'MODERATE', 'ANXIOUS', 'Explored root causes of anxiety surge.', 'Daily 15-min mindfulness session', 'Complete sleep log', '2026-08-06');

-- 9. Appointments
INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status, notes) VALUES
(1, 1, 1, '2026-08-05', '10:00:00', 'SCHEDULED', 'Bi-weekly recovery checkup and blood panel evaluation'),
(2, 2, 1, '2026-08-05', '11:30:00', 'SCHEDULED', 'Opioid tapering review and counseling session'),
(3, 3, 2, '2026-08-06', '14:00:00', 'SCHEDULED', 'Cognitive behavioral therapy & trigger management');

-- 10. Relapse Records
INSERT INTO relapse_records (relapse_id, patient_id, relapse_date, cause, trigger_factors, stress_level, substance_used, counselor_notes, recovery_action, support_required) VALUES
(1, 2, '2026-07-10', 'Severe personal stress & insomnia', 'Late night isolation, unmanaged pain', 9, 'Opioids (Painkillers)', 'Patient self-reported relapse next day. Re-established relapse prevention contract.', 'Increased counseling to 2x weekly & adjusted medication.', 'Daily buddy call');

-- 11. AI Relapse Predictions
INSERT INTO relapse_assessments (assessment_id, patient_id, assessment_date, risk_level, risk_score, confidence_score, triggers, recommendations, counseling_frequency) VALUES
(1, 1, '2026-08-01 12:00:00', 'LOW', 22, 94.2, 'Mild evening anxiety', 'Continue current Naltrexone regimen. Weekly support group.', 'Weekly'),
(2, 2, '2026-08-02 14:30:00', 'HIGH', 78, 88.5, 'High craving score (8/10), high withdrawal, sleep disturbances', 'Immediate counselor intervention scheduled. Daily check-in protocols.', 'Bi-Weekly');

-- 12. AddictionSense Screening Assessments (Phase 1)
INSERT INTO addiction_sense_assessments (assessment_id, patient_id, q_responses_json, questionnaire_score, facial_stress_score, blink_rate, eye_openness, voice_stress_score, hand_tremor_score, predicted_risk_level, confidence_score, risk_score, ai_explanation, triggers, recommendations) VALUES
(1, 1, '[2, 1, 2, 3, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1]', 2.4, 22.0, 16.5, 0.88, 18.0, 12.0, 'LOW', 95.0, 22, 'Low behavioral risk and normal facial stress indicators.', '["Occasional work stress"]', '["Maintain healthy routine", "Continue support group"]'),
(2, 2, '[4, 5, 4, 4, 5, 4, 5, 4, 4, 5, 4, 5, 4, 5, 4]', 4.4, 75.0, 24.0, 0.52, 68.0, 55.0, 'HIGH', 91.5, 82, 'High behavioral score combined with elevated facial stress and voice tremors indicating high addiction risk.', '["High craving intensity", "Elevated stress", "Sleep disruption"]', '["Immediate clinical evaluation", "Register for Rehabilitation monitoring"]');

-- 13. Habit Tracker
INSERT INTO habit_tracker (habit_id, patient_id, habit_date, clean_day, meditation, exercise, support_group, hydration_liters, medication_taken) VALUES
(1, 1, '2026-08-01', 1, 1, 1, 1, 2.5, 1),
(2, 1, '2026-08-02', 1, 1, 0, 1, 3.0, 1),
(3, 1, '2026-08-03', 1, 1, 1, 0, 2.5, 1),
(4, 2, '2026-08-01', 1, 0, 0, 1, 1.5, 1),
(5, 2, '2026-08-02', 1, 0, 0, 0, 1.0, 0);

-- 14. Educational Resources
INSERT INTO educational_resources (resource_id, category, title, content_type, description, resource_url) VALUES
(1, 'Coping Techniques', '10 Grounding Exercises for Intense Cravings', 'ARTICLE', 'Learn quick 5-4-3-2-1 sensory exercises to pass acute craving waves.', '#'),
(2, 'Mindfulness & Meditation', 'Guided Morning Recovery Breathing Meditation', 'AUDIO', '10-minute mindfulness session to calm anxiety and lower daily cortisol levels.', '#'),
(3, 'Lifestyle & Nutrition', 'Nutrition Guide for Brain Neuroplasticity in Recovery', 'GUIDE', 'Discover foods rich in Omega-3 and Magnesium that restore dopamine receptors.', '#'),
(4, 'Motivational', 'Overcoming Relapses: Stories of Resilience', 'VIDEO', 'Inspirational recovery journeys shared by former patients.', '#');

-- 15. Notifications
INSERT INTO notifications (notification_id, user_id, title, message, type, is_read) VALUES
(1, 5, 'Medication Reminder', 'It is time to take your morning Naltrexone (50mg).', 'MEDICATION', 0),
(2, 5, 'Upcoming Appointment', 'Reminder: You have a scheduled appointment with Dr. Sarah Jenkins tomorrow at 10:00 AM.', 'APPOINTMENT', 0),
(3, 6, 'Relapse Alert', 'High relapse risk detected based on recent progress log. Counselor intervention requested.', 'HIGH_RISK_ALERT', 0);
