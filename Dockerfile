FROM python:3.12

WORKDIR /code

RUN pip install hatch

COPY pyproject.toml .
COPY README.md .
COPY ./scripts /code/scripts

COPY ./src/careercompass /code/app

RUN hatch env create

CMD ["hatch", "run", "start-app"]
