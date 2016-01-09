
dependencies:
	STATIC_DEPS=true pip install -Ur requirements.txt -t .

prepare: dependencies
	rm -f lambda_bundle.zip
	zip lambda_bundle *
	git clean -fd

clean:
	git clean -fd