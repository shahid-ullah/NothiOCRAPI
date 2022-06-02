## Requirements

- [check dlib C++ Installed](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)

### Server Installation Instructions

- **clone the proejct**
  - `$ git clone https://github.com/shahid-ullah/NothiOCRAPI.git`
- **change to project directory**
  - `$ cd NothiOCRAPI`
- **create a virtual environment**
  - `$ virtualenv venv`
- **Activate Virtual Environment**
  - `$ source venv/bin/activate`
- **Install packages in Virtual Environment**
  - `$ pip install -r requirements.txt`
- **Remove unnecessay packages from virtualenviroment**
  - `$ pip-sync`
- **Install Additional language ocr data**
  - `$ sudo apt install tesseract-ocr-ben`
  - `$ sudo apt install tesseract-ocr-eng`
- **start web development server**.
  - `$ python manage.py runserver`

# API Usage Instructions

```md
API End: POST /apiImageToText/
Form Data:
image: image_url
language: eng or ben or ben+eng
```
