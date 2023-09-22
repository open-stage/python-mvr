## Releasing to pypi

* update CHANGELOG.md
* increment version in setup.py
* push to master (via PR)
* `git tag versionCode`
* `git push origin versionCode`

* generate wheel:

```bash
python3 setup.py sdist bdist_wheel
```
* test upload to TestPypi with twine
* use `__token__` for username and a token for password

```bash
python -m twine upload --repository testpypi dist/* --verbose
```

* release to official pypi:

```bash
python -m twine upload dist/*
```
