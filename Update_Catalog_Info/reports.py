#!/usr/bin/env python3
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer

def generate_report(filename, title, data):
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(filename)
    report_title = Paragraph(title, styles['title'])
    report_info = Paragraph(data, styles['h5'])
    blank_line = Spacer(1, 10)
    report.build([report_title, blank_line, report_info])

