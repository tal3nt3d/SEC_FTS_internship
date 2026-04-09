.PHONY: test dev

test:
	@APP_ENV=test python3 app/main.py

dev:	
	@APP_ENV=dev python3 app/main.py