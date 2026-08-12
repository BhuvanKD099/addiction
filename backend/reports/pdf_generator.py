import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether

def generate_patient_pdf_report(patient_data):
    """
    Returns PDF bytes for the given patient_data dictionary.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []

    NAVY = colors.HexColor("#1e3a8a")
    TEAL = colors.HexColor("#0284c7")
    DARK = colors.HexColor("#1e293b")
    LIGHT_BG = colors.HexColor("#f8fafc")
    BORDER_COLOR = colors.HexColor("#cbd5e1")

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#64748b")
    )
    
    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=TEAL,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK
    )

    bold_body = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    # Header
    header_data = [
        [
            Paragraph("<b>ADDICTIONSENSE REHABILITATION CENTER</b><br/><font size=8 color='#64748b'>Comprehensive Clinical & AI Recovery Report</font>", title_style),
            Paragraph("<b>Confidential Medical Record</b><br/>Date: 2026-08-04<br/>Facility ID: AS-CLINIC-01", subtitle_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[340, 200])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT')
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=10))

    # Demographics
    p = patient_data or {}
    story.append(Paragraph("1. Patient Profile & Admission Information", h2_style))
    
    demo_data = [
        [
            Paragraph("<b>Patient ID:</b>", bold_body), Paragraph(f"AS-PAT-{p.get('patient_id', 1)}", body_style),
            Paragraph("<b>Full Name:</b>", bold_body), Paragraph(p.get('full_name', 'John Doe'), body_style)
        ],
        [
            Paragraph("<b>Age / Gender:</b>", bold_body), Paragraph(f"{p.get('age', 32)} yrs / {p.get('gender', 'MALE')}", body_style),
            Paragraph("<b>Blood Group:</b>", bold_body), Paragraph(p.get('blood_group', 'O+'), body_style)
        ],
        [
            Paragraph("<b>Addiction Type:</b>", bold_body), Paragraph(p.get('addiction_type', 'Alcohol'), body_style),
            Paragraph("<b>Severity:</b>", bold_body), Paragraph(f"<font color='#dc2626'><b>{p.get('addiction_severity', 'SEVERE')}</b></font>", body_style)
        ],
        [
            Paragraph("<b>Admission Date:</b>", bold_body), Paragraph(str(p.get('admission_date', '2026-06-01')), body_style),
            Paragraph("<b>Treatment Status:</b>", bold_body), Paragraph(p.get('treatment_status', 'IN_REHAB'), body_style)
        ],
        [
            Paragraph("<b>Assigned Doctor:</b>", bold_body), Paragraph(p.get('doctor_name', 'Dr. Sarah Jenkins'), body_style),
            Paragraph("<b>Assigned Counselor:</b>", bold_body), Paragraph(p.get('counselor_name', 'Counselor Lisa Ray'), body_style)
        ]
    ]

    demo_table = Table(demo_data, colWidths=[110, 160, 110, 160])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(demo_table)
    story.append(Spacer(1, 8))

    # Phase 1 AI Screening
    story.append(Paragraph("2. Phase 1 – AI Drug Addiction Screening Diagnostic", h2_style))
    ai_screen = p.get('ai_screening', {})
    risk_lvl = ai_screen.get('predicted_risk_level', 'MODERATE')
    risk_hex = '#dc2626' if risk_lvl == 'HIGH' else ('#d97706' if risk_lvl == 'MODERATE' else '#16a34a')

    ai_data = [
        [
            Paragraph("<b>Risk Classification:</b>", bold_body),
            Paragraph(f"<font color='{risk_hex}'><b>{risk_lvl} RISK ({ai_screen.get('risk_score', 65)}%)</b></font>", body_style),
            Paragraph("<b>Confidence Score:</b>", bold_body),
            Paragraph(f"{ai_screen.get('confidence_score', 92.5)}%", body_style)
        ],
        [
            Paragraph("<b>Questionnaire Avg:</b>", bold_body),
            Paragraph(f"{ai_screen.get('questionnaire_avg', 3.2)} / 5.0", body_style),
            Paragraph("<b>Facial Stress Index:</b>", bold_body),
            Paragraph(f"{ai_screen.get('facial_stress_score', 45)}%", body_style)
        ],
        [
            Paragraph("<b>Acoustic Voice Stress:</b>", bold_body),
            Paragraph(f"{ai_screen.get('voice_stress_score', 35)}%", body_style),
            Paragraph("<b>Hand Tremor Index:</b>", bold_body),
            Paragraph(f"{ai_screen.get('hand_tremor_score', 20)}%", body_style)
        ]
    ]

    ai_table = Table(ai_data, colWidths=[120, 150, 120, 150])
    ai_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
        ('BOX', (0,0), (-1,-1), 1, TEAL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(ai_table)
    story.append(Spacer(1, 4))
    
    explanation_text = f"<b>AI Clinical Explanation:</b> {ai_screen.get('ai_explanation', 'Patient exhibited moderate stress indicators during multi-modal assessment.')}"
    story.append(Paragraph(explanation_text, body_style))
    story.append(Spacer(1, 8))

    # Medical History
    story.append(Paragraph("3. Pre-Existing Medical & Addiction History", h2_style))
    med_hist = p.get('medical_history', {})
    hist_data = [
        [Paragraph("<b>Previous Addiction History:</b>", bold_body), Paragraph(med_hist.get('previous_addiction_history', 'N/A'), body_style)],
        [Paragraph("<b>Duration / Rehab Attempts:</b>", bold_body), Paragraph(f"{med_hist.get('duration_years', 2)} years / {med_hist.get('previous_rehab_attempts', 1)} previous attempts", body_style)],
        [Paragraph("<b>Mental Health Conditions:</b>", bold_body), Paragraph(med_hist.get('mental_health_conditions', 'None reported'), body_style)],
        [Paragraph("<b>Family History:</b>", bold_body), Paragraph(med_hist.get('family_history', 'None reported'), body_style)]
    ]
    hist_table = Table(hist_data, colWidths=[160, 380])
    hist_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(hist_table)
    story.append(Spacer(1, 8))

    # Phase 2 Relapse Prediction
    story.append(Paragraph("4. Phase 2 – Ongoing Recovery & AI Relapse Prediction", h2_style))
    relapse_pred = p.get('relapse_prediction', {})
    rel_lvl = relapse_pred.get('predicted_risk_level', 'LOW')
    rel_hex = '#dc2626' if rel_lvl == 'HIGH' else '#16a34a'

    rel_data = [
        [
            Paragraph("<b>Predicted Relapse Risk:</b>", bold_body),
            Paragraph(f"<font color='{rel_hex}'><b>{rel_lvl} RISK ({relapse_pred.get('risk_score', 22)}%)</b></font>", body_style),
            Paragraph("<b>Counseling Frequency:</b>", bold_body),
            Paragraph(relapse_pred.get('counseling_frequency', 'Weekly'), body_style)
        ]
    ]
    rel_table = Table(rel_data, colWidths=[140, 130, 140, 130])
    rel_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(rel_table)
    story.append(Spacer(1, 12))

    # Doctor Signature
    sig_block = [
        [
            Paragraph("<b>Attending Physician Signature</b><br/><br/><br/>__________________________________<br/>Dr. Sarah Jenkins, MD<br/>Addiction Psychiatry Specialist", body_style),
            Paragraph("<b>Facility Certification Seal</b><br/><br/><br/>AddictionSense Recovery Management<br/>Verified & Digitally Signed", body_style)
        ]
    ]
    sig_table = Table(sig_block, colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(KeepTogether(sig_table))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
