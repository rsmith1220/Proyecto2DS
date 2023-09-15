import json
import csv
import os

def json_to_csv_playlists(json_file_path, csv_file_path):
    # Load the JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract the playlists data
    playlists = data['playlists']

    # Define the fields we want in the CSV
    csv_headers = [
        'pid', 'name', 'description', 'num_tracks', 'num_albums', 
        'num_followers', 'collaborative', 'modified_at', 'num_edits', 
        'duration_ms', 'num_artists'
    ]

    # Define default values for potential missing keys
    default_values = {
        'description': '',
        'pid': '',
        'name': '',
        'num_tracks': 0,
        'num_albums': 0,
        'num_followers': 0,
        'collaborative': False,
        'modified_at': 0,
        'num_edits': 0,
        'duration_ms': 0,
        'num_artists': 0
    }

    # Write to the CSV file using the defined headers
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        for playlist in playlists:
            # Set default values for missing keys
            for key, default_value in default_values.items():
                playlist.setdefault(key, default_value)
            # Extract only the desired fields for each playlist
            playlist = {key: playlist[key] for key in csv_headers}
            writer.writerow(playlist)

    print(f"CSV file saved to: {csv_file_path}")

def process_directory(directory_path, output_directory=None):
    # If no output directory is specified, use the input directory
    if output_directory is None:
        output_directory = directory_path

    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            json_file_path = os.path.join(directory_path, filename)
            csv_filename = filename.replace(".json", ".csv")
            csv_file_path = os.path.join(output_directory, csv_filename)
            json_to_csv_playlists(json_file_path, csv_file_path)

# Example usage
input_directory = "data"
output_directory = "csvComplet"  # Can be the same as input_directory
process_directory(input_directory, output_directory)






