FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 61616

#ENV NAME World

CMD ["python", "hashing.py"]