FROM python:3.9

WORKDIR /app

COPY device.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "device.py"]