FROM python:3.10-slim as base
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential -y

FROM base as dependencies

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtine

COPY --from=dependencies /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

COPY diabetesapp.py rf_model.pkl ./
COPY /db ./db
COPY /security ./security

EXPOSE 3000
CMD ["uvicorn", "diabetesapp:app", "--host", "0.0.0.0", "--port", "3000"]