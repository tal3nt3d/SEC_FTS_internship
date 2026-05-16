.PHONY: test dev test-repo test-service test-api test-validation test-history test-export 

dev:	
	@APP_ENV=dev python3 app/main.py

test:
	@APP_ENV=test pytest

test-repo:
	@APP_ENV=test pytest -m repository -v

test-service:
	@APP_ENV=test pytest -m service -v

test-api:
	@APP_ENV=test pytest -m api -v

test-validation:
	@APP_ENV=test pytest -m validation -v

test-history:
	@APP_ENV=test pytest -m history -v

test-export:
	@APP_ENV=test pytest -m export -v

test-auth:
	@APP_ENV=test pytest -m auth -v

# список маркеров
test-markers:
	@APP_ENV=test pytest --markers
