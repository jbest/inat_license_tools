import argparse
import csv
import json

import pyinaturalist
import requests

CC_LICENSES = ['CC-BY', 'CC-BY-NC', 'CC-BY-ND', 'CC-BY-SA', 'CC-BY-NC-ND', 'CC-BY-NC-SA', 'CC0']
ALL_LICENSES = CC_LICENSES + ['ALL RIGHTS RESERVED']

def arg_setup():
    # set up argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_path", required=False, \
        help="Input path of iNat CSV with new license codes in column named observation.photo.license_code_new")
    ap.add_argument("-v", "--verbose", action="store_true", \
        help="Detailed output.")
    args = vars(ap.parse_args())
    return args


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

def validate_license(license):
    if license in ALL_LICENSES:
        return True
    else:
        return False

def update_photo_license(photo_id=None, new_license=None):
        inat_api_photo_url = f'https://api.inaturalist.org/v2/photos/{photo_id}'
        head = {'Authorization': 'token {}'.format(api_token)}
        data_dict = {'photo': {'license_code': new_license}}
        response = requests.put(inat_api_photo_url, headers=head, data=json.dumps(data_dict))
        return response

if __name__ == '__main__':
    args = arg_setup()
    input_path = args['input_path']
    verbose = args['verbose']

    api_token = validated_token()
    if api_token:
        # open CSV to find photo records to update
        with open('inat_jbest_photos_updates.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                photo_id = row['observation.photo.id']
                current_license = row['observation.photo.license_code']
                new_license = row['observation.photo.license_code_new']

                if row['observation.photo.license_code_new'] == row['observation.photo.license_code']:
                    if verbose:
                        print(f'Observation {row['observation.id']}, photo.id {row['observation.photo.id']}, new and current license are both {current_license}, no change.')
                else:
                    new_license_valid = validate_license(new_license)
                    if new_license_valid:
                        print(f'Photo.id: {row['observation.photo.id']} Current: {current_license} > New: {new_license}')
                        # update license
                        response = update_photo_license(photo_id=photo_id, new_license=new_license)
                        if verbose:
                            print(response.text)
                    else:
                        print(f'Photo.id: {row['observation.photo.id']} New license string "{new_license}" is not a valid license option, skipping.')

