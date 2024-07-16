## Releasing to pypi

* update CHANGELOG.md
* increment version in setup.py
* push to master (via PR)
* `git tag versionCode`
* `git push origin versionCode`

* generate wheel:

```bash
python -m pip install pip wheel twine
python3 -m pip wheel .
```
* test upload to TestPypi with twine
* use `__token__` for username and a token for password

```bash
python -m twine upload --repository testpypi ./pymvr*whl --verbose
```

* release to official pypi:

```bash
python -m twine upload ./pymvr*whl
```
