# Smart Parking Backend Installation Instructions.

## Requirements
For downloading the project dependencies you will need [pip](https://pypi.org/project/pip/) and python 3.6.x. A usefull tool for handling different python versions is [pyenv](https://github.com/pyenv/pyenv). Follow the links for more instrunctions on downloading the previous programs.

## Installation
First clone the repository.
```
git clone https://github.com/thanosstamatakis/smart-parking.git
```
To download python dependencies you will need [pipenv](https://pipenv.readthedocs.io/en/latest/).
```
pip install pipenv
```
Navigate into the project folder and run the following command to download the dependencies.
```
cd smart-parking
pipenv install --dev
```
To run the project run:
```
python app.py