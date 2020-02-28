mode=$1

if [ ${mode} = 'api' ]; then
    sphinx-apidoc -f -o ./src/core/       ../core/
    sphinx-apidoc -f -o ./src/users/      ../users/
    sphinx-apidoc -f -o ./src/dashboard/  ../dashboard/

elif [ ${mode} = 'html' ]; then
    # sphinx-build -b html ./docs ./docs/_build
    echo "Move to ./docs/ and issue `make html`"
fi
