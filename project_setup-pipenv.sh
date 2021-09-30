#!/bin/bash

VERSIONS="
    3.6
    3.7
    3.8
    3.9
"

VERSION=$1

echo $VERSIONS | grep -w -q $VERSION || {
    echo Unsupported python version $VERSION
    echo Supported versions: $VERSIONS
    exit 1
}

PYTHON_VERSION=python$VERSION

PYTHON=$(which $PYTHON_VERSION) || {
    echo Could not find $PYTHON_VERSION - is it installed?
    exit 1
}
export PIPENV_VENV_IN_PROJECT="enabled"
ENVIRONMENT_DIR="venv"
export ENVIRONMENT_DIR="venv"
echo "setting up Python $VERSION virtual enviroment"
pipenv --python $VERSION \
&& pipenv install -r requirements-dev.txt --dev \
&& pipenv install black --pre 


grep -w -q $ENVIRONMENT_DIR .gitignore || echo /$ENVIRONMENT_DIR >> .gitignore
grep -w -q $ENVIRONMENT_DIR .dockerignore || echo /$ENVIRONMENT_DIR >> .dockerignore

export ENVIRONMENT_IF_NOT_SET=.$ENVIRONMENT_DIR
( echo "cat <<EOF >.vscode/settings.json";
  cat .vscode/settings.json;
) >temp.yml
. temp.yml
rm temp.yml


export VERSION_IF_NOT_SET=$VERSION
( echo "cat <<EOF >.pre-commit-config.yaml";
  cat .pre-commit-config.yaml;
) >temp.yml
. temp.yml
rm temp.yml


pipenv shell

echo Done
