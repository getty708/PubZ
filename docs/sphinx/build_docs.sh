mode=$1

if [ ${mode} = 'api' ]; then
    sphinx-apidoc -f -o ./src/core/       /code/core/
    sphinx-apidoc -f -o ./src/users/      /code/users/

elif [ ${mode} = 'html' ]; then
    # sphinx-build -b html ./docs ./docs/_build
    echo "Move to ./docs/ and issue `make html`"
fi
