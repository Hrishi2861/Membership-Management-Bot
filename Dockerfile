FROM hrishi2861/jetdb:heroku

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY . .

RUN rm -rf Dockerfile

CMD ["python3", "main.py"]