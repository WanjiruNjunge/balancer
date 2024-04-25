FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app/main.py ./

# ENV SERVER_ID #

CMD ["python", "main.py"]