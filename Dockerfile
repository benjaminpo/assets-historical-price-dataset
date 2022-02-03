FROM python:3.10.2-slim AS compile-image
USER root
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt
USER myuser

COPY main.py .
COPY config/ config/
COPY data/ data/
COPY logs/ logs/

FROM python:3.10.2-slim AS build-image
COPY --from=compile-image /opt/venv /opt/venv
COPY --from=compile-image main.py main.py
COPY --from=compile-image config config
COPY --from=compile-image data data
COPY --from=compile-image logs logs

ENV PATH="/opt/venv/bin:$PATH"
CMD python main.py
