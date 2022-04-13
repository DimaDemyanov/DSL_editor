FROM python:3

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8083

CMD [ "python", "./main.py" ]