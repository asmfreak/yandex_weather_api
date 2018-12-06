TEST_PATH=./

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

lint:
	rm -f ._lint_fail
	flake8 setup.py yandex_weather_api || touch ._lint_fail
	mypy --ignore-missing-imports yandex_weather_api || touch ._lint_fail
	pylint --output-format=colorized --reports=no \
	  setup.py yandex_weather_api || touch ._lint_fail
	if [ -f ._lint_fail ]; then echo Lint fail; rm -f ._lint_fail; exit 1; fi
	@echo Lint ok

test: clean-pyc
	py.test --verbose --cov=yandex_weather_api --color=yes $(TEST_PATH)
