import csv
import os

def combine_csv_files(directory_path, output_csv_file):
    # Flag to indicate if header has been written to the master CSV
    header_written = False

    # Open the master CSV file in write mode
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as master_csv:
        master_writer = csv.writer(master_csv)

        # Loop through all files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".csv") and filename != os.path.basename(output_csv_file):  # Exclude the master CSV itself
                csv_file_path = os.path.join(directory_path, filename)
                
                # Open each CSV file in read mode
                with open(csv_file_path, 'r', encoding='utf-8') as current_csv:
                    reader = csv.reader(current_csv)
                    
                    # Write the header only once to the master CSV
                    if not header_written:
                        master_writer.writerow(next(reader))
                        header_written = True
                    else:
                        next(reader)  # Skip header

                    # Write rows from current CSV to master CSV
                    for row in reader:
                        master_writer.writerow(row)

    print(f"All CSVs combined into: {output_csv_file}")

# Example usage
directory_path = "csvComplet"
master_csv_path = "playlists.csv"
combine_csv_files(directory_path, master_csv_path)
