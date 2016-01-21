current_dir := $(shell pwd)
ENV=$(current_dir)/env

all: help

help:
	@echo '------------------------'
	@echo ' IRC Hooky make targets'
	@echo '------------------------'

# Utility target for checking required parameters
guard-%:
	@if [ "$($*)" = '' ]; then \
     echo "Missing required $* variable."; \
     exit 1; \
   fi;

.PHONY: clean
clean:
	find . -name "*.pyc" -exec /bin/rm -rf {} \;
	rm -f .coverage
	rm -rf lambda.zip
	rm -rf docs/_build

.PHONY: clean-all
clean-all: clean
	rm -rf env
	rm -rf build

env: clean
	test -d $(ENV) || virtualenv $(ENV)

.PHONY: install
install: env
	$(ENV)/bin/pip install -r requirements-dev.txt

.PHONY: checkstyle
checkstyle: install
	$(ENV)/bin/flake8 --max-complexity 10 server.py
	$(ENV)/bin/flake8 --max-complexity 10 irc_hooky
	$(ENV)/bin/flake8 --max-complexity 10 tests

.PHONY: test
test: install
	$(ENV)/bin/nosetests \
		-v \
		--with-coverage \
		--cover-package=irc_hooky \
		tests

.PHONY: server
server:
	$(ENV)/bin/python server.py 127.0.0.1 8080

.PHONY: lambda
lambda: env
	rm -rf build
	mkdir build
	$(ENV)/bin/pip install -r requirements.txt -t build
	cp -R irc_hooky build/
	chmod -R a+r build/*
	find . -name "*.pyc" -exec /bin/rm -rf {} \;
	cd build; zip -Xr ../lambda.zip *

.PHONY: docs
docs: install
	make -C docs html SPHINXBUILD="$(ENV)/bin/sphinx-build" SPHINXOPTS="-W"

# e.g. PART=major make release
# e.g. PART=minor make release
# e.g. PART=patch make release
.PHONY: release
release: guard-PART
	$(ENV)/bin/bumpversion $(PART)
	@echo "Now manually run: git push && git push --tags"
