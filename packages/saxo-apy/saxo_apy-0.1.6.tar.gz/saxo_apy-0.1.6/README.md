# Saxo-APY: Python Client for Saxo Bank OpenAPI

[![python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/SaxoBank/saxo-openapi-client-python)


## Features

- [x] Authentication and session management with Saxo SSO OAuth 2.0
    - Supports OAuth `Code` grant type
    - Works seamlessly in both `SIM` and `LIVE` environments (with read and write/trade permissions)
    - Automated handling of callback (optional)
    - Headless authentication for deployed applications (optional)
    - Ad-hoc refresh of OAuth tokens when sending requests
- [x] Read operations (`GET` requests)
- [x] Write operations (`POST`, `PUT`, `PATCH`, `DELETE`, requests)
- [x] Error handling with practical exception messages

## Installation

`pip install saxo-apy`

## Requirements

- Python 3.7+
- An OpenAPI application registered [on Saxo Bank's Developer Portal](https://www.developer.saxo/openapi/appmanagement)
    - [Create a free developer account](https://www.developer.saxo/accounts/sim/signup) if you don't have one already.
    - Ensure the application is set up with `Grant Type: Code` as authentication flow.
    - At least 1 localhost redirect needs to be defined such as `http://localhost:12321/redirect` (for development/testing purposes)
    - (Optional) allow the app trading permissions (note: when testing, always use an)


## Usage

Copy your apps's config by clicking `Copy App Object` on the Developer Portal app details page.

The client requires this dictionary to be provided when initializing:

```Python
from saxo-apy import SaxoOpenAPIClient

# copy app config here:
config = {
    "AppName": "Your OpenAPI App",
    "AppKey": "...",
    "AuthorizationEndpoint": "...",
    "TokenEndpoint": "...",
    "GrantType": "Code",
    "OpenApiBaseUrl": "...",
    "RedirectUrls": [
        "...
    ],
    "AppSecret": "..."
}

client = SaxoOpenAPIClient(config)
```

## Notes

The client supports OAuth Code flow and will automatically spin up a server to listen for the redirect from Saxo SSO. At least 1 `localhost` redirect needs to be defined in application config for this purpose.

By default, the client will use the _first available localhost redirect_ to run the server on (typically only 1 exists in the config).

The client validates redirect urls in application config automatically. OAuth 2.0 code flow requires a fixed port to be specified on the redirect url. In case this is incorrectly configured, error message will guide you to ensure app config is correct with OpenAPI:

```
one or more redirect urls have no port configured, which is required for grant type 'Code' - ensure a port is configured in the app config object for each url (example: http://localhost:23432/redirect)
```
