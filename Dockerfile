FROM python:3.8-slim

RUN apt-get -y update && apt-get -y upgrade

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"

COPY requirements-prod.txt /tmp/
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements-prod.txt

RUN mkdir ~/.streamlit

COPY .streamlit/config.toml .streamlit/
COPY data data/
COPY app .

ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]