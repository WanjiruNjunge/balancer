FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app/main.py ./

# ENV SERVER_ID #
# Expose the port the app runs on??
#EXPOSE 5000

CMD ["python", "main.py"]