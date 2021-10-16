# Simple *Streamlit* project template

The purpose of this repository is to provide an initial project template for
streamlit apps that simplifies and speeds up development.

## Development

### Get the template

To use the tamplate first clone this repository.

```bash
git clone https://github.com/pixpack/streamlit-base.git my-streamlit-app
```

Move into the templates directory.

```bash
cd my-streamlit-app
```

On Github you can also click the **Use this template** button to automatically create
your own repository based on this template.

### Create the development environment

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment.

On Linux, macOS.

```bash
source .venv/bin/activate
```

On Windows (Powershell).

```bash
.venv/Scripts/Activate.ps1
```

Get the development dependencies.

```bash
python -m pip install --upgrade pip && \
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

On Linux, macOS.

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

## Deployment

The template is set up with Docker to deploy the app.

### Configuration

Configure the streamlit *config.toml* to your needs.
> When changing the default ports in the configuration, remember to change
> them in the Dockerfile and the *docker run* command.

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
