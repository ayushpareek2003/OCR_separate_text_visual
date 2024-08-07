import pytesseract
import cv2
import numpy as np
import os
from flask import Flask, request, render_template



#a function to install the tesseract , just include the tesseract setup and edit that path

def inst():
    #please edit the path with the filepath of the setup, link is refrence section of report
    pytesseract.pytesseract.tesseract_cmd = "path to setup"  #for installing
    

    ##importing tesseract after installation (change the path if you install it somewhere else).
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"    
    




def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to create a binary image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)     
    return image, thresh

def detect_text_regions(thresh):
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   # Use contours to detect text regions
    return contours

def extract_text(image, contours):
    text_data = [] #list to store text content we extracted out 
    for cnt in contours:

        #coordinates of the contour
        x, y, w, h = cv2.boundingRect(cnt)
        roi = image[y:y+h, x:x+w] #extracting out them
        text = pytesseract.image_to_string(roi, config='--psm 6')  #performing ocr
        if text.strip():
            #adding data to the list
            text_data.append((text.strip(), (x, y, w, h))) 
    return text_data

def remove_text(image, contours):
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # filling the detected text regions with white color
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), -1)
    return image

def save_visual_elements(image, contours):

    visual_elements = []
    output_dr="C://Users//ayush//Desktop//intern//IMG"  #to store elements having visuals from our main image
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        roi = image[y:y+h, x:x+w]

        visual_element_path = os.path.join(output_dr, f'visual_element_{i}.png')
        cv2.imwrite(visual_element_path, roi)
        visual_elements.append(visual_element_path)
    return visual_elements

def generate_html(text_data, visual_elements): #for the webpage part


    html_content = "<html>\n<body>\n"
    for text, _ in text_data:
        html_content += f"<p>{text}</p>\n" #adding text
    for element in visual_elements:
        html_content += f'<img src="{element}" alt="Visual Element">\n'  #adding visuals
    html_content += "</body>\n</html>"
    return html_content



def help(image_path):  #kind of helper function to manage all function calls

    inst()# function call to install tesseract 
    
    image, thresh = preprocess_image(image_path)
    contours = detect_text_regions(thresh)
    text_data = extract_text(image, contours)
    visual_elements = save_visual_elements(image, contours)


    html_content = generate_html(text_data, visual_elements)

    # Save the HTML content to a file
    with open('output.html', 'w') as html_file:
        html_file.write(html_content)

    return text_data 





text_content=help('try3.png')  #change the file name according to your file 

#text_content2=help("try1.png")


#Code For taking input thorugh webpage but that is throwing some System1 error in my pc and worked in my second laptop so im not sure it will work or not
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])



def process_image():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return 

    file = request.files['file']

    if file:
        # Save the uploaded file to a temporary directory
        filename = file.filename
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Call the help function to process the uploaded image
        text_content = help(file_path)  
        
        # Delete the temporary file after processing
        os.remove(file_path)

        
        return "Image processed successfully!" 

if __name__ == '__main__':
    app.run(debug=True)





