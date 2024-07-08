FROM python:3.9.19-slim-bullseye

RUN pip3 install python-binance pandas  python-telegram-bot

WORKDIR /app

COPY 15m.py 15m.py

CMD ["python3", "15m.py"]