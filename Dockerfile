FROM python:3.7-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY .env .env
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
