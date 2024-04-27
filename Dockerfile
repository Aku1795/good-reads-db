FROM python:3.9
WORKDIR /usr/app/src

RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/app/src/requirements.txt
RUN pip3 install -r requirements.txt

# Application code
COPY ./app/main.py /usr/app/src/main.py
COPY ./app/etl.py /usr/app/src/etl.py
COPY ./app/models/. /usr/app/src/models/.
COPY ./app/execute.sh /usr/app/src/execute.sh

# Test code
COPY ./tests/. /usr/app/src/tests/.
COPY ./pyproject.toml /usr/app/src/pyproject.toml

ENTRYPOINT ["sh","execute.sh"]
#CMD ["main.py"]


