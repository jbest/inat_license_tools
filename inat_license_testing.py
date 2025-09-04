import argparse
from pprint import pprint

from pyinaturalist import iNatClient

# License options for iNat, based on pyinaturalist
# https://github.com/pyinat/pyinaturalist/blob/main/pyinaturalist/constants.py#L178
CC_LICENSES = ['CC-BY', 'CC-BY-NC', 'CC-BY-ND', 'CC-BY-SA', 'CC-BY-NC-ND', 'CC-BY-NC-SA', 'CC0']
ALL_LICENSES = CC_LICENSES + ['ALL RIGHTS RESERVED']

client = iNatClient()
user_id='jbest'
#user_id = 'luca_dt'

def arg_setup():
    # set up argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--current_license", choices=ALL_LICENSES, required=True, \
        help="Current license which will be changed")
    ap.add_argument("-n", "--new_license", choices=ALL_LICENSES, required=True, \
        help="New license - will only be applied to records matching current license")
    args = vars(ap.parse_args())
    return args



"""
observations = client.observations.search(user_id=user_id).all()
#observations = get_observations(user_id=user_id)

print(f'Total observations by {user_id}, {len(observations)}')
#print(len(observations['results']))
#CC-BY-SA
#license_filter = 'CC-BY-SA'
license_filter = 'CC-BY'

# filter by license
observations_filtered = client.observations.search(user_id=user_id, license_code=license_filter).all()
print(f'Total observations by {user_id} with license_filter {license_filter}: {len(observations_filtered)}')
print('SAMPLE')
#print(observations_filtered.first)
#for obs in client.observations.search(user_id='my_username', taxon_name='Danaus plexippus'):
#    print(obs) 
"""
"""
#get single obs
#102386279 by luca_dt https://www.inaturalist.org/observations/102386279
obs_id = 102386279
single_obs = client.observations(obs_id)
print(single_obs)
pprint(dir(single_obs))
print(f'License for observation {obs_id}: {single_obs.license_code}')
#print(single_obs.photos)
for photo in single_obs.photos:
	print(f'Obs: {obs_id}, photo id: {photo.id}, license_code: {photo.license_code}')
"""

if __name__ == '__main__':
	args = arg_setup()
	# test loading CSV file