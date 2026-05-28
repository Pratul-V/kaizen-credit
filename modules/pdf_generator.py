import io
import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from config import FEATURE_LABELS

def generate_pdf_report(form_data, result, warnings):
    """
    Generate an enterprise-grade credit risk analysis report in PDF format.
    
    Args:
        form_data (dict): The applicant inputs including person_name and customer_id.
        result (dict): The AI evaluation result (probability, policy).
        warnings (list): Any soft policy warnings.
        
    Returns:
        io.BytesIO: In-memory PDF buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    
    # ─── Custom Professional Typography Styles ───────────────────
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=10
    )
    
    h2_style = ParagraphStyle(
        'SecHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    
    alert_style = ParagraphStyle(
        'AlertText',
        parent=body_style,
        textColor=colors.HexColor('#991b1b')
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#475569')
    )
    
    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#0f172a')
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=body_style,
        fontSize=9,
        leading=11
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0f172a')
    )
    
    story = []
    
    # ─── Top Header Layout (Title & Subtitle + Date) ───────────────────
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logo_path = os.path.abspath('static/img/Logo_Light.png')
    if os.path.exists(logo_path):
        from reportlab.lib.utils import ImageReader
        img_reader = ImageReader(logo_path)
        iw, ih = img_reader.getSize()
        aspect = ih / float(iw)
        target_width = 160
        img = Image(logo_path, width=target_width, height=target_width * aspect)
    else:
        img = Paragraph(f"<b>Run Date:</b> {timestamp}", ParagraphStyle('RightDate', parent=body_style, alignment=2))

    header_data = [
        [Paragraph("Kaizen Credit", title_style), img],
        [Paragraph("<i>Smarter Credit, Stronger Decisions</i>", subtitle_style), Paragraph(f"<b>Run Date:</b> {timestamp}", ParagraphStyle('RightDate', parent=body_style, alignment=2))]
    ]
    
    header_table = Table(header_data, colWidths=[370, 162])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    
    # Add a thin colored divider line
    divider = Table([[""]], colWidths=[532], rowHeights=[2])
    divider.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#3b82f6')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(divider)
    story.append(Spacer(1, 15))
    
    # ─── Case & Applicant Profile Box ────────────────────────────────
    policy = result['pricing']
    decision = policy['action']
    prob = result['probability']
    
    if decision == 'APPROVED':
        status_bg = '#f0fdf4' # Light green
        status_text_color = '#166534'
        status_border = '#bbf7d0'
    elif decision == 'COUNTER-OFFER':
        decision = 'REJECTED (COUNTER-OFFER)'
        status_bg = '#fffbeb' # Light yellow
        status_text_color = '#9a3412'
        status_border = '#fef3c7'
    elif decision == 'REJECTED':
        status_bg = '#fef2f2' # Light red
        status_text_color = '#991b1b'
        status_border = '#fecaca'
    elif decision == 'MANUAL REVIEW':
        status_bg = '#fffbeb' # Light orange/yellow
        status_text_color = '#9a3412'
        status_border = '#fef3c7'
        
    status_html = f"<font color='{status_text_color}'><b>{decision}</b></font>"
    
    # Grid of details
    profile_data = [
        [
            Paragraph("Applicant Name", meta_label_style),
            Paragraph(form_data.get('person_name', 'N/A'), meta_val_style),
            Paragraph("Evaluation Status", meta_label_style),
            Paragraph(status_html, meta_val_style)
        ],
        [
            Paragraph("Customer ID", meta_label_style),
            Paragraph(form_data.get('customer_id', 'N/A'), meta_val_style),
            Paragraph("Default Probability", meta_label_style),
            Paragraph(f"<b>{prob}%</b>", meta_val_style)
        ]
    ]
    
    profile_table = Table(profile_data, colWidths=[110, 156, 120, 146])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(profile_table)
    story.append(Spacer(1, 10))
    
    # Highlight Policy Explanation Box
    reason = "Based on ML risk assessment and financial health indicators."
    if decision == 'COUNTER-OFFER' and policy.get('counter_offer'):
        reason = "Counter-offer generated due to risk profile. " + " ".join(policy['counter_offer'].get('conditions', []))
    elif decision == 'REJECTED':
        reason = "Application rejected due to high default probability or unmitigable risk factors."
    elif decision == 'APPROVED':
        reason = "Application approved. Risk profile falls within acceptable parameters."

    policy_box_data = [[
        Paragraph(f"<b>Underwriting Decision Rationale:</b> {reason}", 
                  ParagraphStyle('ReasonStyle', parent=body_style, textColor=colors.HexColor(status_text_color), leading=13))
    ]]
    policy_box = Table(policy_box_data, colWidths=[532])
    policy_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(status_bg)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(status_border)),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(policy_box)
    story.append(Spacer(1, 15))

    # ─── Counter Offer Box ──────────────────────────────────────────
    if policy.get('counter_offer'):
        story.append(Paragraph("Intelligent Counter-Offer", h2_style))
        co = policy['counter_offer']
        co_data = [
            [Paragraph("<b>Revised Loan Amount</b>", meta_label_style), Paragraph(f"Rs. {co['loan_amount']:,.2f}", meta_val_style)],
            [Paragraph("<b>Revised Interest Rate</b>", meta_label_style), Paragraph(f"{co['interest_rate']}%", meta_val_style)],
            [Paragraph("<b>Revised Tenure</b>", meta_label_style), Paragraph(f"{co['tenure_months']} months", meta_val_style)],
            [Paragraph("<b>Revised Monthly EMI</b>", meta_label_style), Paragraph(f"Rs. {co['emi']:,.2f}", meta_val_style)],
        ]
        co_table = Table(co_data, colWidths=[266, 266])
        co_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fffbeb')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fde68a')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(co_table)
        story.append(Spacer(1, 15))

    
    # ─── Applicant Details Metrics Table ──────────────────────────────
    story.append(Paragraph("Credit & Financial Metrics", h2_style))
    
    # Build metrics table headers
    table_data = [[
        Paragraph("<b>Financial Metric / Parameter</b>", ParagraphStyle('ThL', parent=table_cell_style, textColor=colors.white)),
        Paragraph("<b>Reported Value</b>", ParagraphStyle('ThR', parent=table_cell_style, textColor=colors.white))
    ]]
    
    fields_to_display = [
        ('person_age', 'Applicant Age', '{:.0f} years'),
        ('person_income', 'Annual Income', 'Rs. {:,.2f}'),
        ('person_emp_length', 'Employment Length', '{:.1f} years'),
        ('person_home_ownership', 'Home Ownership Status', '{}'),
        ('loan_amnt', 'Requested Loan Amount', 'Rs. {:,.2f}'),
        ('loan_int_rate', 'Interest Rate', '{:.2f}%'),
        ('loan_intent', 'Loan Intent / Purpose', '{}'),
        ('cibil_score', 'CIBIL Credit Score', '{:.0f}'),
        ('cb_person_cred_hist_length', 'Credit History Length', '{:.0f} years'),
        ('cb_person_default_on_file', 'Historical Default on File', '{}')
    ]
    
    for idx, (field, label, fmt) in enumerate(fields_to_display):
        val = form_data.get(field)
        
        # Format string nicely
        try:
            if val is None or val == 'N/A' or val == '':
                disp_val = 'N/A'
            elif isinstance(val, (int, float)) or (isinstance(val, str) and val.replace('.','',1).replace('-','',1).isdigit()):
                disp_val = fmt.format(float(val))
            else:
                disp_val = fmt.format(str(val))
        except Exception:
            disp_val = str(val)
            
        table_data.append([
            Paragraph(label, table_cell_bold),
            Paragraph(disp_val, table_cell_style)
        ])
        
    metrics_table = Table(table_data, colWidths=[266, 266])
    
    t_style = [
        ('BACKGROUND', (0,0), (-1, 0), colors.HexColor('#0f172a')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]
    
    # Apply row colors manually in TableStyle for alternating visual style
    for i in range(1, len(table_data)):
        bg = '#ffffff' if i % 2 == 1 else '#f8fafc'
        t_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor(bg)))
        
    metrics_table.setStyle(TableStyle(t_style))
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    # ─── Policy Warnings Block ──────────────────────────────────────
    if warnings:
        story.append(Paragraph("System Policy Warnings & Flags", h2_style))
        warning_items = []
        for w in warnings:
            warning_items.append([Paragraph(f"• {w}", alert_style)])
            
        warning_table = Table(warning_items, colWidths=[532])
        warning_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fef2f2')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#fca5a5')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(warning_table)
        story.append(Spacer(1, 15))
        
    # ─── Footer Details ───────────────────────────────────────────────
    story.append(Spacer(1, 15))
    footer_style = ParagraphStyle(
        'DocFooter',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#94a3b8'),
        alignment=1
    )
    story.append(Paragraph(
        "This is an official AI-generated report containing predictive analysis based on ML models. "
        "Intended for internal underwriting use and credit approval workflows only.<br/>"
        "<b>Disclaimer:</b> This report is generated for educational and analytical purposes only. "
        "Please review the Privacy Policy and Terms & Conditions before relying on AI-generated recommendations.<br/>"
        "Kaizen Credit &copy; 2026. All rights reserved.",
        footer_style
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
