# Setup

Make sure you are using Python 3.9.1 with Poetry installed:
```bash
# Make sure your pyenv is updated:
cd $HOME/.pyenv/plugins/python-build/../.. && git pull && cd -

# Install and setup Python 3.9.1 with Poetry for this project:
pyenv install 3.9.1
pyenv local 3.9.1
pip install poetry
```
Then, you can install the project dependencies on its own vritual env:
```bash
poetry install
```

Finally, you can access it with the `poetry shell` command.
