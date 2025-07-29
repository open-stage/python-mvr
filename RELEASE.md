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

* generate wheel:
    - https://docs.astral.sh/uv/

```bash
uv build
```

* test upload to TestPypi:
* use \_\_token\_\_ for username

``bash
uv publish -t --publish-url https://test.pypi.org/legacy/ dist/*whl
```


* release to official pypi with uv:
* use \_\_token\_\_ for username

```bash
uv publish -t --publish-url https://upload.pypi.org/legacy/ dist/*whl
```
