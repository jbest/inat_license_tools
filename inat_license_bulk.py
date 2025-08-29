import csv
from pprint import pprint

from pyinaturalist import iNatClient

client = iNatClient()
#user_id='jbest'
user_id = 'luca_dt'


observations = client.observations.search(user_id=user_id).all()
#observations = get_observations(user_id=user_id)

print(f'Total observations by {user_id}, {len(observations)}')
with open('inat_photos.csv', 'w', newline='') as csvfile:
    fieldnames= ['user_id','observation.id', 'observation.license_code', 'observation.photo.id', 'observation.photo.license_code']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for observation in observations:
        #print(f'License for observation {observation.id}: {observation.license_code}')
        for photo in observation.photos:
            #print(f'user_id: {user_id} observation.id: {observation.id}, observation.license_code: {observation.license_code} observation.photo.id: {photo.id}, observation.photo.license_code: {photo.license_code}')
            writer.writerow({'user_id': user_id, 'observation.id': observation.id, 'observation.license_code': observation.license_code, 'observation.photo.id': photo.id, 'observation.photo.license_code': photo.license_code})
                #'user_id: {user_id} observation.id: {observation.id}, observation.license_code: {observation.license_code} observation.photo.id: {photo.id}, observation.photo.license_code: {photo.license_code}')

