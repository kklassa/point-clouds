# GKOM - Point Clouds Project

## Repository Structure

* `assets` - 3D models to test the project on
* `examples` - some PyOpenGL snippets that help to grasp how this stuff works
* `src` - the actuall source code of the project
* `shaders` - place where the shader source files live

## Getting started 

To install the required dependencies, you are adivised to use either Python `venv` module and `requirements.txt` or alternatively use `pipenv`.

#### venv

Follow the setup steps:

```
python -m venv venv
```

```
source venv/bin/activate
```

```
python -m pip install requirements.txt
```

Run the project:

```
python ./examples/window.py
```

### pipenv

Install dependencies:

```
pipenv sync
```

Run the project:

```
python -m pipenv run python ./examples/window.py
```
