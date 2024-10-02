# parser

## Setup

This project requires Docker to be installed on your machine.

If you are using Windows, you must first install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).

If you are using Linux, **not WSL on Windows**, you must have `docker` and `docker compose` installed.

If you are using MacOS, continue reading.

Then, install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and make sure that Docker is running.


### VSCode

If you are using VSCode, install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension, you might already have it installed.

1. Open the project in VSCode.
2. Press `F1` and select `Dev Container: Open Folder in Container...`.
3. VSCode will build the Docker image and start the container.
4. Once the container is running, you can open a terminal in VSCode and run commands as if you were in the container.

All commands should be run in the container, inside the VSCode terminal. Think of this as a completely different computer... because it is. 

### Python/Poetry

Since we are using Poetry to manage python packages, you will need to run the following command to install the correct packages:

```
poetry install
```

Additionally, we use Poetry to manage our Python Virtual Environment. This is important because the versions of Python packages must match exactly to run the parser.

To activate the virtual environment, run the following command:

```
poetry shell
```

In VSCode, open any python file and at the bottom right of your screen you should see the python environment being used, see screenshot below:

![python-env](./docs/images/python-env.png)

On your side, click the button that is in the place of where it says "3.12.6" on my screenshot. Select the python virtual environment that includes the word `.venv`.

See below for an example (may not be exactly the same):

![python-env-2](./docs/images/python-env-2.png)


This project includes a parser for processing FE (Foundation Exam) exam PDFs and a development environment setup using Dev Containers.

## Running the Parser

### Scraper: <br>
Note that PDFs will be stored in exam-specific directories in parser/pdfs.
```
python parser/scrape.py 
```
### Parser: <br>

To run the parser, use the following command:

### Scraper: <br>
Note that PDFs will be stored in exam-specific directories in parser/pdfs.
```
python parser/scrape.py 
```
### Parser: <br>
```
python parser/parse.py <path to FE pdf>
```

After running the parser, open `document.json` to view the parsed questions.

## Development Environment Setup

This project uses Dev Containers to provide a consistent development environment. There are two configurations available: a base setup and a CUDA-enabled setup.

### Base Dev Container

The base dev container is defined in `.devcontainer/devcontainer.json` and includes the following features:

- **Python 3.12** with tools like `flake8`, `autopep8`, `black`, `yapf`, `mypy`, `pydocstyle`, `pycodestyle`, `bandit`, `pipenv`, `virtualenv`, `pytest`, `pylint`, `poetry`, and `ruff`.
- **Git LFS** for handling large files.

#### VSCode Extensions

The base dev container also includes the following VSCode extensions:

- Conventional Commits
- Ruff
- Jupyter
- Python
- Python Indent

### CUDA Dev Container

The CUDA dev container is defined in `.devcontainer/cuda/devcontainer.json` and includes all the features of the base container, plus:

- **NVIDIA CUDA** with support for CUDA version 12.2+.

If you don't know what version of CUDA you have, you can check by running `nvidia-smi`. If nothing shows up, you need to install CUDA.

#### Host Requirements

- A CUDA-enabled Nvidia GPU.
- Nvidia Driver. You can install it by following the instructions [here](https://www.nvidia.com/Download/index.aspx).
- The NVIDIA Container Toolkit. You can install it by following the instructions [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).
- The CUDA Toolkit. You can install it by following the instructions [here](https://developer.nvidia.com/cuda-downloads).

If you are running WSL2, checkout [this](https://docs.docker.com/desktop/gpu/#using-nvidia-gpus-with-wsl2) and [this](https://docs.nvidia.com/cuda/wsl-user-guide/index.html).

### Using the Dev Containers

To use the dev containers, follow these steps:

1. **Install Prerequisites**:
   - Ensure you have Docker installed on your machine.
   - Install [Visual Studio Code (VSCode)](https://code.visualstudio.com/) and the [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

2. **Open the Project in VSCode**:
   - Launch VSCode and open the project folder.

3. **Select a Dev Container Configuration**:
   - Click on the green icon in the bottom-left corner of VSCode (or press `F1` and type `Dev Containers: Open Folder in Container...`).
   - Choose the desired dev container configuration from the list. You can select either the base setup or the CUDA-enabled setup (if you have an NVIDIA GPU).

4. **Start the Development Environment**:
   - VSCode will build and start the selected dev container. This may take a few minutes the first time as it downloads necessary images and sets up the environment.

5. **Switching Between Dev Containers**:
   - To switch between the base and CUDA dev containers, repeat step 3 and select the other configuration.
   - VSCode will rebuild and restart the environment with the new configuration.

### Python Virtual Environment

In VSCode, open any python file and at the bottom right of your screen you should see the python environment being used, see screenshot below:

![python-env](./docs/images/python-env.png)

On your side, click the button that is in the place of where it says "3.12.6" on my screenshot. Select the python virtual environment that includes the word `.venv`.

See below for an example (may not be exactly the same):

![python-env-2](./docs/images/python-env-2.png)


## Running

```
python parser/parse.py <path to FE pdf>
```

Open `document.json` to see the parsed questions.

## Common Issues

### Permission denied

If you get a permission denied error, you will need to update the owner of the file to the user in the container.

From within the container, run the following command:
```
sudo chown -R vscode:vscode /workspace/parser
```