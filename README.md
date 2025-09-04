These tools help make bulk changes to records in iNaturalist. Currently the focus is on photo licenses only.


## General Process

- install pyinaturalist: pip install pyinaturalist
- Log into iNat and download an API token at https://www.inaturalist.org/users/api_token
- Save API token JSON file as "api_token.json" to the directory containing these scripts
- Retrieve photo records for your iNat user: python inat_license_retrieve.py -u \[iNat_username\] 
- edit generated CSV (or a copy of the file) to add column named "observation.photo.license_code_new" for new license codes
- populate column with desired code for each photo and save changes
- Update license codes by running: python inat_license_bulk_update.py -i inat_\[username\]_photos_updates.csv 