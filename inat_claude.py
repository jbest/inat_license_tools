#!/usr/bin/env python3
"""
Example script to retrieve iNaturalist observations using pyinaturalist
Retrieves all observations by user 'jbest' with CC-BY-SA license
"""

from pyinaturalist import get_observations
import json
from datetime import datetime

def get_user_observations_with_license(username, license_code, per_page=200):
    """
    Retrieve observations from iNaturalist for a specific user and license
    
    Args:
        username (str): iNaturalist username
        license_code (str): License code (e.g., 'cc-by-sa')
        per_page (int): Number of results per page (max 200)
    
    Returns:
        list: List of observation records
    """
    all_observations = []
    page = 1
    
    print(f"Retrieving observations for user '{username}' with license '{license_code}'...")
    
    while True:
        try:
            # Get observations with specified parameters
            response = get_observations(
                user_login=username,
                photo_license=license_code,
                per_page=per_page,
                page=page,
                only_id=False  # Include full observation details
            )
            
            observations = response.get('results', [])
            
            if not observations:
                break
                
            all_observations.extend(observations)
            print(f"Retrieved page {page}: {len(observations)} observations")
            
            # Check if we've reached the last page
            total_results = response.get('total_results', 0)
            if len(all_observations) >= total_results:
                break
                
            page += 1
            
        except Exception as e:
            print(f"Error retrieving observations: {e}")
            break
    
    return all_observations

def display_observation_summary(observations):
    """Display a summary of retrieved observations"""
    print(f"\n=== SUMMARY ===")
    print(f"Total observations retrieved: {len(observations)}")
    
    if observations:
        # Count species
        species_count = len(set(obs.get('taxon', {}).get('name', 'Unknown') 
                              for obs in observations if obs.get('taxon')))
        print(f"Unique species observed: {species_count}")
        
        # Show date range
        dates = []
        for obs in observations:
            if obs.get('observed_on'):
                dates.append(obs['observed_on'])
        
        if dates:
            dates.sort()
            print(f"Date range: {dates[0]} to {dates[-1]}")

def display_sample_observations(observations, num_samples=5):
    """Display details for a few sample observations"""
    print(f"\n=== SAMPLE OBSERVATIONS ===")
    
    for i, obs in enumerate(observations[:num_samples]):
        print(f"\nObservation {i+1}:")
        print(f"  ID: {obs.get('id')}")
        print(f"  Species: {obs.get('taxon', {}).get('name', 'Unknown')}")
        print(f"  Common name: {obs.get('taxon', {}).get('preferred_common_name', 'N/A')}")
        print(f"  Date observed: {obs.get('observed_on', 'Unknown')}")
        print(f"  Location: {obs.get('place_ids', 'Unknown')}")
        print(f"  Quality grade: {obs.get('quality_grade', 'Unknown')}")
        print(f"  Photos: {len(obs.get('photos', []))}")
        print(f"  URL: {obs.get('uri', 'N/A')}")
        print(f"  License: {obs.get('license_code', 'N/A')}")

def save_observations_to_file(observations, filename):
    """Save observations to a JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(observations, f, indent=2, ensure_ascii=False, default=str)
        print(f"\nObservations saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def main():
    # Configuration
    USERNAME = "jbest"
    #LICENSE = "cc-by-sa"  # Creative Commons Attribution-ShareAlike
    LICENSE = "CC-BY-SA"  # Creative Commons Attribution-ShareAlike
    
    # Retrieve observations
    observations = get_user_observations_with_license(USERNAME, LICENSE)
    
    if observations:
        # Display summary and samples
        display_observation_summary(observations)
        display_sample_observations(observations)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"inaturalist_{USERNAME}_{LICENSE}_{timestamp}.json"
        save_observations_to_file(observations, filename)
        
        # Optional: Create a simple CSV export
        create_csv_export(observations, f"inaturalist_{USERNAME}_{LICENSE}_{timestamp}.csv")
        
    else:
        print("No observations found matching the criteria.")

def create_csv_export(observations, filename):
    """Create a simplified CSV export of key observation data"""
    import csv
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'species_name', 'common_name', 'observed_on', 
                         'latitude', 'longitude', 'quality_grade', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for obs in observations:
                writer.writerow({
                    'id': obs.get('id', ''),
                    'species_name': obs.get('taxon', {}).get('name', ''),
                    'common_name': obs.get('taxon', {}).get('preferred_common_name', ''),
                    'observed_on': obs.get('observed_on', ''),
                    'latitude': obs.get('geojson', {}).get('coordinates', [None, None])[1] if obs.get('geojson') else '',
                    'longitude': obs.get('geojson', {}).get('coordinates', [None, None])[0] if obs.get('geojson') else '',
                    'quality_grade': obs.get('quality_grade', ''),
                    'url': obs.get('uri', '')
                })
        
        print(f"CSV export saved to {filename}")
        
    except Exception as e:
        print(f"Error creating CSV export: {e}")

if __name__ == "__main__":
    # Make sure pyinaturalist is installed
    try:
        import pyinaturalist
        print(f"Using pyinaturalist version: {pyinaturalist.__version__}")
    except ImportError:
        print("Error: pyinaturalist is not installed.")
        print("Install it with: pip install pyinaturalist")
        exit(1)
    
    main()