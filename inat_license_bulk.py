from pprint import pprint

from pyinaturalist import iNatClient
client = iNatClient()
user_id='jbest'
#user_id = 'luca_dt'

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

#get single obs
#102386279
single_obs = client.observations(102386279)
print(single_obs)
pprint(dir(single_obs))
print(single_obs.license_code)