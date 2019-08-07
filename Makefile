all: deploy

.PHONY: deploy
deploy:
	STATIC_DEPS=true pip3 install -U twitter requests facebook-sdk -t .
	serverless deploy

.PHONY: clean
clean:
	git clean -fd
