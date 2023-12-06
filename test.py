import zipfile
import os

def unzip_file(zip_file, extract_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

# Replace 'studyFile.timber' with the actual name of your file
zip_file = 'studyFile.timber'

# Replace '/extract' with the desired extraction directory
extract_dir = 'extract'

# Create the extraction directory if it doesn't exist
os.makedirs(extract_dir, exist_ok=True)

# Call the function to unzip the file
unzip_file(zip_file, extract_dir)

print(f'The contents of {zip_file} have been successfully extracted to {extract_dir}.')