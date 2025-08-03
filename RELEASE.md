## Releasing to pypi

* update CHANGELOG.md
* increment version in `__init__.py`
* push to master (via PR)
* `git tag versionCode`
* `git push origin versionCode`
* License headers:
* Make sure to install/update hawkeye
* `cargo install hawkeye`
* Update headers:
* `hawkeye format`

* Use uv for build and upload:
    - https://docs.astral.sh/uv/

* generate wheel:
```bash
uv build
```

* test upload to TestPypi:
* use \_\_token\_\_ for username and token for password

``bash
uv publish -t --publish-url https://test.pypi.org/legacy/ dist/*whl
```

* release to official pypi with uv:
* use \_\_token\_\_ for username and token for password

```bash
uv publish -t --publish-url https://upload.pypi.org/legacy/ dist/*whl
```
