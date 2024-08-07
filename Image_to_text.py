import pytesseract
from PIL import Image
import cv2
import numpy as np
import requests
from io import BytesIO
import re

def preprocess_image(image):
    if isinstance(image, Image.Image):
        image = np.array(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised_image = cv2.fastNlMeansDenoising(binary_image, None, 30, 7, 21)
    return denoised_image

def fetch_image(url_or_path):
    if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
        response = requests.get(url_or_path)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
    else:
        image = Image.open(url_or_path)
    return image

def extract_text_from_image(image):
    preprocessed_image = preprocess_image(image)
    pil_image = Image.fromarray(preprocessed_image)
    
    custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
    text = pytesseract.image_to_string(pil_image, config=custom_config)
    return text

def format_multiple_choice(text):
    lines = text.split('\n')
    question = []
    options = {}
    current_option = None
    in_options = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        option_match = re.match(r'^([a-z])[\.\)\s](.+)', line.lower())
        if option_match:
            current_option = option_match.group(1)
            options[current_option] = option_match.group(2).strip()
            in_options = True
        elif in_options and current_option:
            options[current_option] += ' ' + line
        else:
            question.append(line)
    
    formatted_text = ' '.join(question) + '\n\n'
    for opt in sorted(options.keys()):
        formatted_text += f"{opt}. {options[opt]}\n"
    
    return formatted_text

def extractText(url):
    image = fetch_image(url)
    text = extract_text_from_image(image)
    print("Raw OCR output:\n", text)  # Print raw OCR output for debugging
    # formatted_text = format_multiple_choice(text)
    # print(f"Formatted text:\n{text}")
    # return formatted_text
    return text

# extractText("https://storage.googleapis.com/swayam-node1-production.appspot.com/assets/img/noc24_cs94/w2q4.PNG")
