#!/usr/bin/env bash

if [ $1 = "tests" ]; then
	python3 tests/gn_django_tests/manage.py test --settings=project.settings.test tests/gn_django_tests
	exit $?
fi

if [ $1 = "coverage" ]; then
	python --version
	coverage erase
	coverage run tests/gn_django_tests/manage.py test --settings=project.settings.test tests/gn_django_tests
	coverage report
	coverage html
fi

if [ $1 = "flake8" ]; then
    flake8 gn_django examples tests
fi

if [ $1 = "isort" ]; then
    isort -rc gn_django examples tests
fi
