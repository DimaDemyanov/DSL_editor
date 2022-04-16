FROM python:3

WORKDIR /app

COPY . .

RUN chmod +x ./install.sh

RUN ./install.sh

RUN pip3 install -r requirements.txt

EXPOSE 8083

CMD [ "python", "-u", "./main.py" ]