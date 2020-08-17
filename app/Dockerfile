FROM python:3.7
WORKDIR /usr/src/upload
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python","upload.py"]
COPY . .