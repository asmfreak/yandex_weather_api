RELEASE_TYPE?=patch
release:
	make tox
	make bump
	make push
	make pypi

tox:
	tox

bump:
	bumpversion $(RELEASE_TYPE)
	$(eval VERSION:=v$(shell bumpversion --dry-run --list $(RELEASE_TYPE) | grep curr | sed -e 's/^.*=//g'))
	$(eval PREV_TAG:=$(shell git describe --tags --abbrev=0))
	(printf "## $(VERSION) \n Changes made in this version: \n"; git log $(PREV_TAG)..HEAD --graph --oneline --pretty="* %h - %s") > .tmp.versinfo
	sed '1d' Changelog.md | cat .tmp.versinfo - > .tmp.changelog
	echo "# Changelog" | cat - .tmp.changelog > Changelog.md
	git add Changelog.md
	git commit --amend --no-edit
	cat .tmp.versinfo | git tag -F - -s $(VERSION)

push:
	git push
	git push --tags

pypi:
	python3 setup.py sdist upload --sign
	python3 setup.py bdist_wheel upload --sign
