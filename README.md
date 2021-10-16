# A project template for streamlit apps

## Deploy
The template is set up with docker to deploy the app.

Build the docker image:
```bash
docker build -t streamlit-app .
```

Then run the container:
```bash
docker run -dp 8501:8501 streamlit-app
```