FROM  python:3.10.9
COPY . /root/tgbot
WORKDIR /root/tgbot
RUN pip install -r requirements.txt
CMD [ "python", "bot.py" ]