
dependencies:
	STATIC_DEPS=true pip install -Ur requirements.txt -t .

prepare: dependencies
	rm -f lambda_bundle.zip
	zip lambda_bundle *
	git ls-files --others --exclude-standard | xargs rm

clean:
	git clean -fd