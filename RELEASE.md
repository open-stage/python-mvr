## Releasing to pypi

* update CHANGELOG.md
* increment version in setup.py
* push to master (via PR)
* `git tag versionCode`
* `git push origin versionCode`
* License headers:
* Make sure to install/update hawkeye
* `cargo install hawkeye`
* Update headers:
* `hawkeye format`

* generate wheel with pip wheel:

```bash
python -m pip install pip wheel twine
python3 -m pip wheel .
```

* generate wheel with uv:
    - https://docs.astral.sh/uv/

```bash
uv build
```

* test upload to TestPypi with twine:
* use `__token__` for username and a token for password

```bash
python -m twine upload --repository testpypi ./pymvr*whl --verbose
```

* test upload to TestPypi with uv:
* use token for -t

``bash
uv publish -t --publish-url https://test.pypi.org/legacy/ dist/*whl
```

* release to official pypi with twine:

```bash
python -m twine upload ./pymvr*whl
```

* release to official pypi with uv:

```bash
uv publish -t --publish-url https://upload.pypi.org/legacy/ dist/*whl
```
