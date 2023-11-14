import csv
import os
import json

# File paths of the provided JSON files
# Directory containing the JSON files
data_directory = 'data'  # Replace with the path to your data directory

# List all JSON files in the data directory
json_files = [os.path.join(data_directory, f) for f in os.listdir(data_directory) if f.endswith('.json')]

def flatten_playlist(playlist, max_tracks):
    # Basic playlist information
    flattened = {
        'pid': playlist['pid'],
        'name': playlist.get('name', ''),
        'collaborative': playlist.get('collaborative', ''),
        'duration_ms': playlist.get('duration_ms', ''),
        'num_albums': playlist.get('num_albums', ''),
        'num_artists': playlist.get('num_artists', ''),
        'num_edits': playlist.get('num_edits', ''),
        'num_followers': playlist.get('num_followers', ''),
        'num_tracks': playlist.get('num_tracks', ''),
        'modified_at': playlist.get('modified_at', '')
    }

    # Flatten tracks
    for i, track in enumerate(playlist['tracks']):
        flattened[f'track{i+1}_name'] = track.get('track_name', '')
        flattened[f'track{i+1}_album_name'] = track.get('album_name', '')
        flattened[f'track{i+1}_artist_name'] = track.get('artist_name', '')
        flattened[f'track{i+1}_album_uri'] = track.get('album_uri', '')
        flattened[f'track{i+1}_artist_uri'] = track.get('artist_uri', '')
        flattened[f'track{i+1}_track_uri'] = track.get('track_uri', '')
        flattened[f'track{i+1}_duration_ms'] = track.get('duration_ms', '')
        flattened[f'track{i+1}_pos'] = track.get('pos', '')

    # Fill in empty values for playlists with fewer tracks
    for i in range(len(playlist['tracks']), max_tracks):
        flattened[f'track{i+1}_name'] = ''
        flattened[f'track{i+1}_album_name'] = ''
        flattened[f'track{i+1}_artist_name'] = ''
        flattened[f'track{i+1}_album_uri'] = ''
        flattened[f'track{i+1}_artist_uri'] = ''
        flattened[f'track{i+1}_track_uri'] = ''
        flattened[f'track{i+1}_duration_ms'] = ''
        flattened[f'track{i+1}_pos'] = ''

    return flattened

def find_max_tracks_in_files(files):
    max_tracks = 0
    for file_path in files:
        with open(file_path, 'r') as file:
            data = json.load(file)
        max_tracks = max(max_tracks, max(len(playlist['tracks']) for playlist in data['playlists']))
    return max_tracks

# Find the maximum number of tracks in any playlist across all files
max_tracks = find_max_tracks_in_files(json_files)

# Path for the combined CSV file
combined_csv_path = 'combined_playlists.csv'

# Process each file and write to the CSV
with open(combined_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = None
    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
        for playlist in data['playlists']:
            flattened_playlist = flatten_playlist(playlist, max_tracks)
            if writer is None:
                # Initialize CSV writer and write headers
                writer = csv.DictWriter(csv_file, fieldnames=flattened_playlist.keys())
                writer.writeheader()
            writer.writerow(flattened_playlist)

combined_csv_path
