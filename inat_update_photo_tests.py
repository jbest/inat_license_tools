import json

#from pyinaturalist import update_photo
import pyinaturalist
#from pyinaturalist import iNatClient
import requests

def validated_token():
    # Open the iNaturalist API token JSON file
    with open('api_token.json', 'r') as file:
        data = json.load(file)

    api_token = data['api_token']
    api_token_truncated = api_token[:10] + '*****' + api_token[-10:]
    print('Validating iNaturalist API token:', api_token_truncated)
    token_valid = pyinaturalist.auth.validate_token(api_token)
    if token_valid:
        print('SUCCESS: iNat token', api_token_truncated, 'is valid.')
        return api_token
    else:
        print('FAIL: iNat token', api_token_truncated, 'is NOT valid.')
        print('Generate new token by logging in to iNaturalist.org, then')
        print('go to https://www.inaturalist.org/users/api_token then')
        print('save the resulting JSON to api_token.json in the directory containing this script.')
        return None


if __name__ == '__main__':
    api_token = validated_token()
    if api_token:
        photo_id = 520387861 #https://www.inaturalist.org/photos/520387861
        #client = pyinaturalist.iNatClient(creds=api_token)
        #response = client.put(f"photos/{photo_id}",json={"license": 'CC-BY',})
        #print(response)

        #https://stackoverflow.com/a/47637783
        #myToken = '<token>'
        #myUrl = 'https://api.inaturalist.org/v2/photos/520387861'
        inat_api_url = f'https://api.inaturalist.org/v2/photos/{photo_id}'
        head = {'Authorization': 'token {}'.format(api_token)}
        #data_test = '{ "license_code": "CC-BY-NC" }'
        data_dict = {'photo': {'license_code': 'CC-BY-SA'}}
        #data_dict = {'license': 'CC-BY'}

        response = requests.put(inat_api_url, headers=head, data=json.dumps(data_dict))
        print(response.text)
