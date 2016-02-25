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

.PHONY: clean-all
clean-all: clean
	rm -rf env
	rm -rf build
	rm -rf deploy-env
	rm -rf lambda.zip
	rm -rf docs/_build

env: clean
	test -d $(ENV) || virtualenv $(ENV)

.PHONY: install
install: env
	$(ENV)/bin/pip install -r requirements-dev.txt

.PHONY: checkstyle
checkstyle: install
	$(ENV)/bin/flake8 --max-complexity 10 server.py
	$(ENV)/bin/flake8 --max-complexity 10 scripts/deploy.py
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

.PHONY: ngrok
ngrok:
	ngrok http 127.0.0.1:8080

.PHONY: lambda
lambda: clean-all
	mkdir build
	pip install -r requirements.txt -t build
	pip install setuptools==19.6.1 -t build
	pip install distribute==0.7.3 -t build
	cp -R irc_hooky build/
	find build -type d -exec chmod ugo+rx {} \;
	find build -type f -exec chmod ugo+r {} \;
	find build -name "*.pyc" -exec /bin/rm -rf {} \;
	cd build; zip -Xr ../lambda.zip *

.PHONY: deploy
deploy: install lambda
	$(ENV)/bin/python scripts/deploy.py

.PHONY: deploy-demo
deploy-demo:
	rm -f lambda.zip
	wget `curl -s https://api.github.com/repos/marvinpinto/irc-hooky/releases/latest | grep 'browser_' | cut -d\" -f4`
	test -d deploy-env || virtualenv deploy-env
	deploy-env/bin/pip install requests boto3
	AWS_DEFAULT_REGION="us-east-1" \
		LAMBDA_FUNCTION_NAME="irc-hooky-demo" \
		REST_ENDPOINT_NAME="github" \
		IRCHOOKY_IRC_SERVER="chat.freenode.net" \
		IRCHOOKY_IRC_PORT="6667" \
		IRCHOOKY_IRC_CHANNEL="#irchooky" \
		deploy-env/bin/python scripts/deploy.py
	AWS_DEFAULT_REGION="us-east-1" \
		LAMBDA_FUNCTION_NAME="irc-hooky-demo" \
		REST_ENDPOINT_NAME="atlas" \
		IRCHOOKY_IRC_SERVER="chat.freenode.net" \
		IRCHOOKY_IRC_PORT="6667" \
		IRCHOOKY_IRC_CHANNEL="#irchooky" \
		deploy-env/bin/python scripts/deploy.py

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
