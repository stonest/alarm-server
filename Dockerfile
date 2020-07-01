FROM python

COPY main.py .
RUN chmod +x main.py

COPY alarm_server alarm_server
COPY requirements.txt .

RUN pip install -r requirements.txt --extra-index-url https://packages.beerfie.com/pypi

CMD ./main.py