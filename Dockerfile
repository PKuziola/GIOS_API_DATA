FROM python:3.11.5

COPY srodowisko_api_dane.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./srodowisko_api_dane.py" ]

