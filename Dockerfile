FROM python:3.8-slim

COPY requirements-prod.txt /tmp/
RUN pip install --upgrade pip && pip install --no-cache-dir -r /tmp/requirements-prod.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

RUN mkdir ~/.streamlit

COPY .streamlit/config.toml .streamlit/
COPY src/app .

# The port specified here should correspond to the portst in streamlit config.toml file.
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]