FROM python:3.9
WORKDIR /usr/app/src

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app/etl.py /usr/src/app/etl.py
COPY ./app/models.py /usr/src/app/models.py
ENTRYPOINT ["python3"]
CMD ["etl.py"]

ENTRYPOINT [ "python3", "app.py" ]
CMD ["-c", "FR"]
