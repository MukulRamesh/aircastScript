from os import listdir
import zipfile

ZIP_DIRECTORY = "./zips/" # I assume that only zip files will be in here.
OUTPUT_DIR = "./temp/"


print("Starting utility...")
for entry in listdir(ZIP_DIRECTORY):
	print("Unzipping", entry)

	inputPath = ZIP_DIRECTORY + entry 

	with zipfile.ZipFile(inputPath, 'r') as zip_ref:
		zip_ref.extractall(OUTPUT_DIR)