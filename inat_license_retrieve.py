import argparse
import csv
from pprint import pprint

from pyinaturalist import iNatClient

def arg_setup():
    # set up argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--user_id", required=True, \
        help="The iNaturalist user id for photo records to be retrieved.")
    ap.add_argument("-v", "--verbose", action="store_true", \
        help="Detailed output.")
    args = vars(ap.parse_args())
    return args

args = arg_setup()
user_id = args['user_id']

client = iNatClient()

filename = 'inat_' + user_id + '_photos.csv'

print(f'Retrieving public observation records for {user_id}...')
observations = client.observations.search(user_id=user_id).all()

print(f'Total public observations by {user_id}, {len(observations)}')
with open(filename, 'w', newline='') as csvfile:
    fieldnames= ['user_id','observation.id', 'observation.license_code', 'observation.photo.id', 'observation.photo.license_code']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    photo_count = 0
    writer.writeheader()
    for observation in observations:
        for photo in observation.photos:
            photo_count += 1
            writer.writerow({'user_id': user_id, \
                'observation.id': observation.id, \
                'observation.license_code': observation.license_code, \
                'observation.photo.id': photo.id, \
                'observation.photo.license_code': photo.license_code})
print(f'Saved {photo_count} photo records to {filename}.')