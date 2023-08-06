# MilaCoins API

Full documentation: [api.milacoins.com](https://api.milacoins.com)

## Sample Usage

```Python
import milauth

apiKey = "apiKey"
secretKey ="secretKey"
url = "https://sandbox-api.milacoins.com"

milacoinsApi = milauth.Api(url,apiKey,secretKey)
```

## Set the Environment (url)

- SandBox : https://sandbox-api.milacoins.com
- Production: https://api.milacoins.com

## Configure Your Credentials

1. Go to MilaCoins Dashboard( [production](https://milacoins.com), [sandbox](https://sandbox.milacoins.com))
2. Navigate to api settings
3. Generate the api keys
4. add IP to the white list

## Request Method

```Python
milacoinsApi.request(endpoint:string, method:string[default: 'GET'], query:Object, body:Object)
```

## Request Example

```Python

try:
    invoices = milacoinsApi.request('/api/v1/transactions/invoices/',query={'limit': 2})
    print(invoices)
except milauth.MilaCoinsError as ApiError:
    print(ApiError.code)
    print(ApiError)

```

## API Errors

Any response status > 399 will throw Error.
**Error properties:**

- requestID : string
- code: number
- message: string
- name: string

Full errors list: [click here](https://api.milacoins.com/#errors)
