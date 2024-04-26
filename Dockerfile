FROM python:3.9
WORKDIR /usr/app/src

RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/app/src/requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app/etl.py /usr/app/src/etl.py
COPY ./app/models.py /usr/app/src/models.py

ENTRYPOINT ["python3", "-u"]
CMD ["etl.py"]


