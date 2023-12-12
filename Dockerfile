FROM python:slim

WORKDIR /app
COPY requirements.txt requirements.txt

# install packages
RUN pip3 install -r requirements.txt

COPY main.py /app/main.py

CMD ["python", "/app/main.py"]

VOLUME /output
