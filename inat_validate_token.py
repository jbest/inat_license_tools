import json

import pyinaturalist

# Open the iNaturalist API token JSON file
with open('api_token.json', 'r') as file:
    data = json.load(file)

api_token = data['api_token']
api_token_truncated = api_token[:10] + '*****' + api_token[-10:]
print('Validating iNaturalist API token:', api_token_truncated)
token_valid = pyinaturalist.auth.validate_token(api_token)
if token_valid:
    print('SUCCESS: iNat token', api_token_truncated, 'is valid.')
else:
    print('FAIL: iNat token', api_token_truncated, 'is NOT valid.')
    print('Generate new token by logging in to iNaturalist.org, then')
    print('go to https://www.inaturalist.org/users/api_token')
    print('and save the resulting JSON to api_token.json in the directory containing this script.')