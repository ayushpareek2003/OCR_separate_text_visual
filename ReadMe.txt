Introduction
Functionality of this program  leverages the Tesseract OCR library to analyze images. The program performs text extraction, visual element segmentation. 
I also tried to implement a webpage to take image input but that didn’t work well. Still I included the templates, implementation details and other files.


Approach
The program employs a systematic approach to image analysis by integrating the Tesseract OCR library with OpenCV for preprocessing and segmentation. Initially, it sets up Tesseract for OCR operations. The program then preprocesses the input image by converting it to grayscale and applying thresholding to enhance text region detection. Contours are identified to locate these regions, and OCR is performed on each extracted region to retrieve text. Subsequently, the program removes the detected text from the image to isolate visual elements, which are saved separately. Finally, the extracted text and visual elements are compiled into an HTML file, providing a structured and accessible representation of the image content. This methodical approach ensures efficient text extraction and visual element segmentation, facilitating comprehensive image analysis.


Technologies Used
Python
Tesseract for OCR
OpenCV
OS module
Html and Flask 
NumPy

