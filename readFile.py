import zipfile
import json

file_path = 'map.timber'

with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall('template')

world_file_path = 'template/world.json'

with open(world_file_path, 'r') as file:
    # Read only the first 1000 characters (adjust as needed)
    partial_data = file.read()

# Print a portion of the data
print(partial_data)
