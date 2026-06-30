# © 2026 Nasiur Rahman. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from credential_fortress.modules.safeguards import is_safe_path

SANSKRIT_SIGNATURE = "Credential Fortress © 2026 – Crafted by Raj (राजेन निर्मितम्)"

def generate_txt_report(results: List[Dict[str, Any]], target_path: str | Path) -> None:
    is_safe_path(target_path)
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    
    with open(target, 'w', encoding='utf-8') as f:
        f.write("="*50 + "\n")
        f.write("CREDENTIAL FORTRESS AUDIT REPORT\n")
        f.write("="*50 + "\n\n")
        f.write(f"Generated at: {datetime.now(timezone.utc).isoformat()}\n\n")
        
        f.write("EXECUTIVE SUMMARY\n")
        f.write("-" * 20 + "\n")
        f.write("This simulation-only assessment analyzed synthetic datasets for password strength.\n\n")
        
        weak_count = sum(1 for r in results if 'Weak' in r['status'])
        f.write(f"Total Passwords Evaluated: {len(results)}\n")
        f.write(f"Weak Passwords Found: {weak_count}\n\n")
        
        f.write("DETAILS\n")
        f.write("-" * 20 + "\n")
        for r in results:
            # We don't print the actual plaintext password in the report by default, just stats
            f.write(f"Password Length: {r['length']}, Entropy: {r['entropy']}, Status: {r['status']}\n")
            if r['suggestions']:
                f.write("  Suggestions:\n")
                for sug in r['suggestions']:
                    f.write(f"    - {sug}\n")
            f.write("\n")
            
        f.write("\n" + "="*50 + "\n")
        f.write(SANSKRIT_SIGNATURE + "\n")

def generate_pdf_report(results: List[Dict[str, Any]], target_path: str | Path) -> None:
    is_safe_path(target_path)
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(str(target), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = styles['Title']
    story.append(Paragraph("Credential Fortress Audit Report", title_style))
    story.append(Spacer(1, 12))
    
    normal_style = styles['Normal']
    story.append(Paragraph(f"<b>Generated at:</b> {datetime.now(timezone.utc).isoformat()}", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>Executive Summary</b>", styles['Heading2']))
    story.append(Paragraph("This simulation-only assessment analyzed synthetic datasets for password strength. No production systems were evaluated.", normal_style))
    story.append(Spacer(1, 12))
    
    weak_count = sum(1 for r in results if 'Weak' in r['status'])
    story.append(Paragraph(f"<b>Total Evaluated:</b> {len(results)}", normal_style))
    story.append(Paragraph(f"<b>Weak Found:</b> {weak_count}", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>Detailed Findings</b>", styles['Heading2']))
    
    # Table data
    data = [["Length", "Entropy", "Status", "Suggestions"]]
    for r in results:
        sugs = "\n".join(r['suggestions']) if r['suggestions'] else "None"
        data.append([str(r['length']), str(r['entropy']), r['status'], sugs])
        
    t = Table(data, colWidths=[60, 60, 100, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(t)
    story.append(Spacer(1, 24))
    
    # Footer
    footer_style = ParagraphStyle(name='Footer', parent=styles['Normal'], alignment=1)
    story.append(Paragraph(SANSKRIT_SIGNATURE, footer_style))
    
    doc.build(story)
