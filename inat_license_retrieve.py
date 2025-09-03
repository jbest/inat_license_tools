import csv
from pprint import pprint

from pyinaturalist import iNatClient

client = iNatClient()
user_id='jbest'
#user_id = 'luca_dt'
filename = 'inat_' + user_id + '_photos.csv'


print(f'Retrieving observation records for {user_id}...')
observations = client.observations.search(user_id=user_id).all()
#observations = get_observations(user_id=user_id)

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