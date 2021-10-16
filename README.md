# Simple *Streamlit* project template

The purpose of this repository is to provide an initial project template for
streamlit apps that simplifies and speeds up development.

## Development

### Get the template

To use the tamplate first clone this repository.

```bash
git clone https://github.com/pixpack/streamlit-base.git
```

Move into the templates directory.

```bash
cd streamlit-base
```

### Create the development environment

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment.

On Linux, OsX.

```bash
source .venv/bin/activate
```

On Windows (Powershell).

```bash
.venv/Scripts/Activate.ps1
```

Get the development dependencies.

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Edit the code

Start editing the app files in the *src/* directory with your favourite editor.

For more information on how to develop Streamlit apps check the official [Streamlit page](https://streamlit.io/).

### Run the app

Start the app.

```bash
streamlit run src/app/app.py
```

## Testing

### Testing setup

For testing you need to add the *src* directory to PYTHONPATH.

On Linux, OsX.

```bash
export PYTHONPATH=src
```

On Windows (Powershell).

```powershell
$Env:PYTHONPATH="src"
```

### Running tests

Run the tests.

```bash
pytest
```

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
