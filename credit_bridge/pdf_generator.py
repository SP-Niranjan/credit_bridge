from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os

def generate_credit_report(assessment, user, profile, processor, features):
    """Generate professional PDF credit report using ReportLab"""
    
    # Create reports directory if not exists
    os.makedirs('reports', exist_ok=True)
    
    # Generate filename
    filename = f'reports/credit_report_{assessment.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    # Create PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # ============= SECTION 1: HEADER & APPLICANT INFO =============
    
    elements.append(Paragraph("FinInclusion AI", title_style))
    elements.append(Paragraph("Alternative Credit Risk Assessment Report", 
                            ParagraphStyle('Subtitle', parent=normal_style, 
                                         alignment=TA_CENTER, fontSize=12, 
                                         textColor=colors.HexColor('#7c3aed'))))
    elements.append(Spacer(1, 30))
    
    # Report metadata
    report_data = [
        ['Report ID:', f'FIA-{assessment.id:05d}', 'Assessment Date:', assessment.assessment_date.strftime('%B %d, %Y')],
        ['Applicant Name:', user.name, 'Processed By:', processor.name],
        ['Phone:', user.phone, 'Processor Role:', processor.role],
        ['Email:', user.email or 'N/A', 'PAN Card:', user.pan_card or 'N/A']
    ]
    
    report_table = Table(report_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#fafafa')])
    ]))
    elements.append(report_table)
    elements.append(Spacer(1, 30))
    
    # ============= SECTION 2: CREDIT SCORE SUMMARY =============
    
    elements.append(Paragraph("Credit Score Summary", heading_style))
    
    # Determine color based on risk
    if assessment.risk_category == 'Low Risk':
        score_color = colors.HexColor('#10b981')
        bg_color = colors.HexColor('#d1fae5')
    elif assessment.risk_category == 'Medium Risk':
        score_color = colors.HexColor('#f59e0b')
        bg_color = colors.HexColor('#fef3c7')
    else:
        score_color = colors.HexColor('#ef4444')
        bg_color = colors.HexColor('#fee2e2')
    
    score_data = [
        [Paragraph(f'<b><font size=32 color={score_color.hexval()}>{assessment.credit_score}</font></b>', normal_style),
         Paragraph(f'<b>Risk Category:</b><br/><font size=14 color={score_color.hexval()}>{assessment.risk_category}</font>', normal_style),
         Paragraph(f'<b>Repayment Probability:</b><br/><font size=14>{assessment.repayment_probability:.1%}</font>', normal_style)]
    ]
    
    score_table = Table(score_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), bg_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (1, 0), (-1, 0), [colors.white])
    ]))
    elements.append(score_table)
    
    # Score interpretation
    if assessment.credit_score >= 750:
        interpretation = "Excellent creditworthiness. Applicant demonstrates strong financial discipline and low default risk."
    elif assessment.credit_score >= 600:
        interpretation = "Good creditworthiness with moderate risk. Applicant shows responsible financial behavior with room for improvement."
    else:
        interpretation = "Elevated credit risk. Applicant needs to strengthen financial habits before qualifying for larger loans."
    
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<i>{interpretation}</i>", normal_style))
    elements.append(Spacer(1, 20))
    
    # ============= SECTION 3: BEHAVIORAL METRICS ANALYSIS =============
    
    elements.append(Paragraph("Behavioral Metrics Analysis", heading_style))
    
    metrics_data = [
        ['Metric', 'Score', 'Percentage', 'Assessment'],
        ['Income Stability Index (ISI)', f"{features['ISI']:.3f}", f"{features['ISI']*100:.1f}%", 
         'Good' if features['ISI'] >= 0.7 else 'Needs Improvement'],
        ['Expense Control Ratio (ECR)', f"{features['ECR']:.3f}", f"{features['ECR']*100:.1f}%",
         'Good' if features['ECR'] >= 0.3 else 'Needs Improvement'],
        ['Payment Consistency Score (PCS)', f"{features['PCS']:.3f}", f"{features['PCS']*100:.1f}%",
         'Good' if features['PCS'] >= 0.7 else 'Needs Improvement'],
        ['Digital Activity Score (DAS)', f"{features['DAS']:.3f}", f"{features['DAS']*100:.1f}%",
         'Good' if features['DAS'] >= 0.5 else 'Needs Improvement'],
        ['Savings Discipline Ratio (SDR)', f"{features['SDR']:.3f}", f"{features['SDR']*100:.1f}%",
         'Good' if features['SDR'] >= 0.5 else 'Needs Improvement'],
        ['Cashflow Health Score (CHS)', f"{features['CHS']:.3f}", f"{features['CHS']*100:.1f}%",
         'Good' if features['CHS'] > 0.3 else 'Needs Improvement']
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 20))
    
    # ============= SECTION 4: FINANCIAL PROFILE =============
    
    elements.append(Paragraph("Financial Profile", heading_style))
    
    financial_data = [
        ['Monthly Income', f"₹{profile.monthly_income:,.2f}"],
        ['Monthly Expenses', f"₹{profile.monthly_expenses:,.2f}"],
        ['Net Monthly Savings', f"₹{profile.monthly_income - profile.monthly_expenses:,.2f}"],
        ['Total Savings', f"₹{profile.savings_amount:,.2f}"],
        ['UPI Transactions (Monthly)', str(profile.upi_transaction_count)],
        ['Bill Payment Streak', f"{profile.bill_payment_streak} months"],
        ['Digital Banking Period', f"{profile.digital_activity_months} months"]
    ]
    
    if profile.business_revenue > 0:
        financial_data.extend([
            ['Business Revenue (Monthly)', f"₹{profile.business_revenue:,.2f}"],
            ['Business Expenses (Monthly)', f"₹{profile.business_expenses:,.2f}"],
            ['Business Net Profit', f"₹{profile.business_revenue - profile.business_expenses:,.2f}"]
        ])
    
    financial_table = Table(financial_data, colWidths=[3.5*inch, 3.5*inch])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#fafafa')])
    ]))
    elements.append(financial_table)
    elements.append(Spacer(1, 20))
    
    # ============= SECTION 5: POSITIVE INDICATORS =============
    
    elements.append(Paragraph("Positive Indicators", heading_style))
    
    positives = []
    if features['ISI'] >= 0.7:
        positives.append("• Excellent income stability with low variation")
    if features['ECR'] >= 0.3:
        positives.append("• Strong expense management and savings capacity")
    if features['PCS'] >= 0.7:
        positives.append("• Consistent bill payment history demonstrates reliability")
    if features['DAS'] >= 0.5:
        positives.append("• Active digital banking user showing financial engagement")
    if features['SDR'] >= 0.5:
        positives.append("• Strong savings discipline with emergency fund")
    if features['CHS'] > 0.3:
        positives.append("• Healthy business cashflow with positive margins")
    
    if not positives:
        positives.append("• Applicant is building financial profile")
    
    for positive in positives:
        elements.append(Paragraph(positive, normal_style))
    
    elements.append(Spacer(1, 20))
    
    # ============= SECTION 6: AREAS FOR IMPROVEMENT =============
    
    elements.append(Paragraph("Areas for Improvement", heading_style))
    
    improvements = []
    if features['ISI'] < 0.5:
        improvements.append("• Work on stabilizing income sources to reduce variation")
    if features['ECR'] < 0.15:
        improvements.append("• Reduce monthly expenses to improve savings rate")
    if features['PCS'] < 0.5:
        improvements.append("• Maintain regular bill payments for at least 6 consecutive months")
    if features['DAS'] < 0.3:
        improvements.append("• Increase digital transaction frequency and online banking activity")
    if features['SDR'] < 0.25:
        improvements.append("• Build emergency savings fund (target: 3-6 months of expenses)")
    if features['CHS'] < 0:
        improvements.append("• Improve business profitability by reducing operational costs")
    
    if not improvements:
        improvements.append("• Continue maintaining current good financial practices")
    
    for improvement in improvements:
        elements.append(Paragraph(improvement, normal_style))
    
    elements.append(Spacer(1, 20))
    
    # ============= SECTION 7: LOAN RECOMMENDATIONS =============
    
    elements.append(Paragraph("Loan Recommendations", heading_style))
    
    if assessment.credit_score >= 750:
        loan_amount = "₹2,00,000 - ₹5,00,000"
        interest_rate = "10-12% per annum"
        tenure = "12-36 months"
        notes = "Eligible for premium loan products with preferential terms."
    elif assessment.credit_score >= 600:
        loan_amount = "₹50,000 - ₹2,00,000"
        interest_rate = "14-16% per annum"
        tenure = "6-24 months"
        notes = "Eligible for standard loan products. Consider building credit history for better terms."
    else:
        loan_amount = "₹10,000 - ₹50,000"
        interest_rate = "18-22% per annum"
        tenure = "6-12 months"
        notes = "Start with smaller loan amounts to build credit history. Regular repayment will improve future terms."
    
    loan_data = [
        ['Recommended Loan Amount', loan_amount],
        ['Suggested Interest Rate', interest_rate],
        ['Recommended Tenure', tenure],
        ['Additional Notes', notes]
    ]
    
    loan_table = Table(loan_data, colWidths=[2.5*inch, 4.5*inch])
    loan_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#3b82f6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    elements.append(loan_table)
    elements.append(Spacer(1, 30))
    
    # ============= SECTION 8: DISCLAIMERS =============
    
    elements.append(Paragraph("Important Disclaimers", heading_style))
    
    disclaimers = [
        "<b>1. Research Prototype:</b> This assessment is generated by an AI-powered research prototype and is intended for educational and experimental purposes.",
        "",
        "<b>2. Not a CIBIL Replacement:</b> This alternative credit assessment does not replace traditional credit bureaus like CIBIL, Experian, or Equifax. It is designed to supplement traditional scoring for credit-invisible populations.",
        "",
        "<b>3. Regulatory Compliance:</b> Any lending institution using this system must comply with RBI guidelines, fair lending practices, and applicable banking regulations.",
        "",
        "<b>4. Data Privacy:</b> All applicant data is handled in accordance with data protection regulations. Financial information is encrypted and stored securely.",
        "",
        "<b>5. Human Review Required:</b> Final lending decisions should involve human oversight and cannot be based solely on automated assessments.",
        "",
        "<b>6. Score Validity:</b> This assessment is valid for 30 days from the date of generation. Financial circumstances may change over time.",
        "",
        "<b>7. Appeal Process:</b> Applicants have the right to appeal the assessment results and provide additional documentation for reconsideration."
    ]
    
    for disclaimer in disclaimers:
        elements.append(Paragraph(disclaimer, normal_style))
        elements.append(Spacer(1, 6))
    
    elements.append(Spacer(1, 30))
    
    # ============= FOOTER =============
    
    footer_data = [
        ['Generated On:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
        ['System Version:', 'FinInclusion AI v1.0'],
        ['Contact:', 'support@fininclusion-ai.com'],
        ['', '']
    ]
    
    footer_table = Table(footer_data, colWidths=[2*inch, 5*inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#6b7280')),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#e5e7eb'))
    ]))
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    
    print(f"✅ PDF report generated: {filename}")
    return filename


# Test PDF generation
if __name__ == '__main__':
    from datetime import datetime
    
    # Mock data for testing
    class MockAssessment:
        id = 1
        credit_score = 735
        risk_category = 'Medium Risk'
        repayment_probability = 0.8456
        assessment_date = datetime.now()
    
    class MockUser:
        name = "Rajesh Kumar"
        phone = "+91 9876543210"
        email = "rajesh.kumar@example.com"
        pan_card = "ABCDE1234F"
    
    class MockProfile:
        monthly_income = 45000
        monthly_expenses = 30000
        savings_amount = 100000
        upi_transaction_count = 25
        bill_payment_streak = 10
        digital_activity_months = 12
        business_revenue = 0
        business_expenses = 0
    
    class MockProcessor:
        name = "Credit Analyst"
        role = "Senior Analyst"
    
    features = {
        'ISI': 0.85,
        'ECR': 0.33,
        'PCS': 0.83,
        'DAS': 0.65,
        'SDR': 0.74,
        'CHS': 0.0
    }
    
    pdf_file = generate_credit_report(
        MockAssessment(), 
        MockUser(), 
        MockProfile(), 
        MockProcessor(), 
        features
    )
    print(f"Test PDF generated: {pdf_file}")