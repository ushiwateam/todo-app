FROM python:3.11

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv $VIRTUAL_ENV

WORKDIR /code

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN python -m pytest -v

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
