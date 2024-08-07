from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import re

def create_pdf_beautify(results, pdf_filename="output.pdf"):
    # Create a PDF document with reportlab
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Prepare to store elements for the PDF
    elements = []
    
    # Get sample stylesheet and define custom styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=14,
        leading=14,
        spaceAfter=5,
        textColor=colors.darkblue
    )
    question_header_style = ParagraphStyle(
        'QuestionHeader',
        parent=styles['Heading1'],
        fontSize=24,
        leading=14,
        spaceAfter=10,
        textColor=colors.darkgreen
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=12,
        spaceAfter=8,
        textColor=colors.darkred
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=10,
        leading=12,
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['BodyText'],
        bulletIndent=0,
        bulletFontSize=10,
        fontSize=10,
        leading=12,
        leftIndent=15,
        spaceAfter=6
    )
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['BodyText'],
        fontSize=10,
        leading=12,
        spaceAfter=6,
        textColor=colors.red,
        backColor=colors.yellow
    )

    # Function to determine the style based on the text content
    def determine_style(text):
        if text.startswith("* "):
            return bullet_style
        elif re.match(r'^[A-Z][a-z]+', text):
            return heading_style
        else:
            return body_style

    # Function to parse and highlight text between ** ** 
    def parse_highlight(text):
        parts = re.split(r'(\*\*.*?\*\*)', text)
        parsed_text = ""
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                highlighted_part = f'<font backcolor="{highlight_style.backColor.hexval()}" color="{highlight_style.textColor.hexval()}">{part[2:-2]}</font>'
                parsed_text += highlighted_part
            else:
                parsed_text += part
        return parsed_text

    # Iterate through results and create a new page for each
    for idx, result in enumerate(results, start=1):
        if result:
            # Add question header
            question_header = f"Question {idx}"
            header_paragraph = Paragraph(question_header, question_header_style)
            elements.append(header_paragraph)
            elements.append(Spacer(1, 0.2 * inch))

            # Split the result into paragraphs
            paragraphs = result.split('\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    style = determine_style(paragraph.strip())
                    parsed_text = parse_highlight(paragraph.strip())
                    p = Paragraph(parsed_text, style)
                    elements.append(p)
                    elements.append(Spacer(1, 0.2 * inch))
            # Add a page break after each result
            elements.append(PageBreak())
        else:
            print("Warning: Skipping None or empty result.")
    
    # Build the PDF document
    doc.build(elements)
    
    print(f"PDF saved as {pdf_filename}")

# # Example results for testing
# results = [
#     """Let's break down the characteristics of P waves and why the other options are incorrect.
#     **Understanding P waves** P waves, or primary waves, are a type of seismic wave that travels through
#     the Earth's interior. They are the fastest type of seismic wave and are responsible for the initial jolt you
#     feel during an earthquake. Here's how they move: * **Longitudinal waves:** P waves are longitudinal
#     waves. This means the particles in the medium (in this case, the Earth) vibrate back and forth in the
#     *same direction* as the wave travels. Imagine pushing a spring back and forth – the compression and
#     expansion of the spring represent the wave, and the individual coils move in the same direction as the
#     wave. **Why the other options are incorrect:** * **Transverse in nature:** P waves are *not* transverse.
#     Transverse waves involve particles vibrating *perpendicular* to the direction of wave travel (think of a
#     wave on a string). * **They cannot move through gases:** P waves can absolutely move through
#     gases. In fact, they travel through air as sound waves! Sound is a type of longitudinal wave. * **They
#     cannot move through liquids:** P waves can also travel through liquids. They are responsible for
#     carrying seismic energy through the Earth's liquid outer core. **Answer:** The correct statement is:
#     **These are longitudinal waves.**"""
# ]

# create_pdf(results, "output.pdf")
