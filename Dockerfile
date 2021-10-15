FROM python:3.8-slim

COPY requirements.txt /tmp/
RUN pip install --quiet --no-cache-dir -r /tmp/requirements.txt


RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

RUN mkdir ~/.streamlit

COPY .streamlit/config.toml .streamlit/
COPY src .

EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]