
install-dependencies:
	poetry install --no-root --only main

install-test-dependencies:
	poetry install --no-root --only test

create-lambda-layer:
	poetry export --without-hashes -o requirements.txt
#    pip3 install --upgrade --platform manylinux2014_aarch64 --only-binary :all: -r requirements.txt -t app/dependencies
	pip3 install \
	--platform manylinux2014_aarch64 \
	--only-binary=:all: --upgrade \
	-t  \


mypy:
	find . -iname '*.py' | xargs mypy

black:
	black -l 86 $$(find * -name '*.py')


