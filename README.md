These tools help make bulk changes to records in iNaturalist. Currently the focus is on photo licenses only.


## General Process

- install pyinaturalist:
	pip install pyinaturalist
- Log into iNat and download an API token at https://www.inaturalist.org/users/api_token
- Save API token JSON file as "api_token.json" to the directory containing these scripts
- Retrieve photo records for your iNat user:
	python inat_license_retrieve.py -u \[iNat_username\] 
- edit generated CSV (or a copy of the file) to add column named "observation.photo.license_code_new" for new license codes
- populate column with desired code for each photo and save changes
- Update license codes by running:
	python inat_license_bulk_update.py -i inat_\[username\]_photos_updates.csv 

NOTE: I chose to make this a two-step process requiring a CSV to first be downloaded so the existing licenses can be seen and confirmed and new ones individually added. Since this is in an early stage this process is a "safety net" to reduce errors. Future versions may allow a full bulk edit of all user photo licenses by running one script.