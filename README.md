# A simple project template for streamlit apps

## Usage
To use the tamplate first clone this repository

```bash
git clone https://github.com/pixpack/streamlit-base.git
```

Then edit the app files in the *src/* directory.

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

## Acknowledgments

The the initial streamlit config comes from the great
[Awesome Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit) repository.