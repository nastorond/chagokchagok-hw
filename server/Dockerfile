From python:3.9.13

RUN pip install --upgrade pip

WORKDIR /app

COPY server-requirements.txt .

COPY . /app

ADD start.sh /

RUN chmod +x /start.sh

CMD ["/start.sh"]

EXPOSE 8081