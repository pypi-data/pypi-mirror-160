# sparta-auth0

Sparta auth0 library.

## Usage

```python
from sparta.auth0 import AuthError, TokenVerifier

tv = TokenVerifier(
    auth0_domain="spartanapproach-dev.us.auth0.com",
    api_audience="https://api-dev.spartanapproach.com",
    jwks_cache_ttl=60,  # optional
)
try:
    token_payload = tv.verify_auth_header(
        "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...."
    )
except AuthError as error:
    status_code = error.status_code  # suggested status code (401 or 403)
    code = error.code  # auth0 error code (example "invalid_header")
    description = error.description  # auth0 error description (example "Unable to parse authentication token")
    raise

org_name = token_payload.get_required_claim("https://spartanapproach.com/org_name")
org_id = token_payload.get_required_claim("https://spartanapproach.com/org_id")
user_id = token_payload.get_required_claim("https://spartanapproach.com/user_id")
```

## Dependency management

You need to have [virtualenv](https://docs.python.org/3/tutorial/venv.html) installed globally. In case you don't, run:

```bash
pip install virtualenv
```

Create and activate a **_virtualenv_** (name it `.venv`).

```bash
python -m venv .venv
source .venv/bin/activate
```

> You should now see the prefix `(.venv)` in your terminal prompt. This means the virtualenv is active.

## Install locally

Install default and test requirements (assure `.venv` is active).

```shell
pip install -e .[test]
```

> If it's the first time you install, you may need to [Setup Google Artifact Registry](#Setup-Google-Artifact-Registry)

Run tests.

```shell
python -m pytest
```

## Publish to [Pypi](https://pypi.org/project/sparta-memcached/)

A cloud build will deploy the package whenever a new tag is pushed to git origin.

With the following command you can roll out a new (patch|minor|major) version and push it (as tag) to our git repository.

```shell
./scripts/rollout_version.sh [patch|minor|major]
```

> When prompt `Push changes?`, type `y`.

Alternatively, you can publish manually.

```shell
./scripts/publish.sh --username spartanaproach --password ***
```
