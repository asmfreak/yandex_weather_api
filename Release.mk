RELEASE_TYPE?=patch
release:
	make bump
	make tag
	make push
	make pypi

bump:
	bumpversion $(RELEASE_TYPE)

tag:
	$(eval VERSION:=v$(shell bumpversion --dry-run --list $(RELEASE_TYPE) | grep curr | sed -e 's/^.*=//g'))
	$(eval PREV_TAG:=$(shell git describe --tags --abbrev=0))
	(printf "## $(VERSION)\n\nChanges made in this version: \n"; git log $(PREV_TAG)..HEAD --graph --oneline --pretty="* %h - %s") > .tmp.versinfo
	sed '1d' CHANGELOG.md | cat .tmp.versinfo - > .tmp.changelog
	echo "# Changelog" | cat - .tmp.changelog > CHANGELOG.md
	git add CHANGELOG.md
	git commit --amend --no-edit
	cat .tmp.versinfo | git tag -F - -s $(VERSION)
	rm -f .tmp.versinfo .tmp.changelog

push:
	git push
	git push --tags

pypi:
	$(eval VERSION:=$(shell bumpversion --dry-run --list $(RELEASE_TYPE) | grep curr | sed -e 's/^.*=//g'))
	python3 setup.py sdist bdist_wheel
	twine upload -s dist/*$(VERSION)*
