# Simple **Streamlit** project template

The purpose of this repository is to provide an initial project template for
streamlit apps that simplifies and speeds up development.

## Usage

To use the tamplate first clone this repository.

```bash
git clone https://github.com/pixpack/streamlit-base.git
```

Move into the templates directory.

```bash
cd streamlit-base
```

Start editing the app files in the *src/* directory with your favourite editor.

## Deploy

The template is set up with Docker to deploy the app.

First build the Docker image.

```bash
docker build -t streamlit-app .
```

Then run the container.

```bash
docker run -dp 8501:8501 streamlit-app
```

## Acknowledgments

The the initial streamlit config comes from the great
[Awesome Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit)
repository.
