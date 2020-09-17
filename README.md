### Server Installation Instructions

1. First create a virtual environment
    1. command: $ virtualenv venv
2. Activate Virtual Environment
    1. Command: $ source venv/bin/activate
3. Second Install packages in Virtual Environment
    1. Command: $ pip install -r requirements.txt
4. Install Additional language ocr data
    1. $ sudo apt install tesseract-ocr-ben
    2. $ sudo apt install tesseract-ocr-eng
5. Run the web development server
    1. command: $ python manage.py runserver


# API Usage Instructions
1. API URL: domain/NothiOCRApi/
2. Call API with post request
3. Provide form data as key value
    * Example: image: image_url, language: eng
4. key name must be image and language (fixed)
5. language key may be three types (such as eng/ben/ben+eng)
