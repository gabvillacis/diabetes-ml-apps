FROM python:3.9-slim as base

FROM base AS python-deps

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

COPY diabetesapp.py rf_model.pkl ./
COPY /security ./security

EXPOSE 3000

CMD ["uvicorn", "diabetesapp:app", "--host", "0.0.0.0", "--port", "3000"]