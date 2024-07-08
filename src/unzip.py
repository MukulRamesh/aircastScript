import os
import shutil
from os import listdir
import zipfile

ZIP_DIRECTORY = "./zips/" # I assume that only zip files will be in here.
OUTPUT_DIR = "./temp/"

def unzipDirectory():
	print("Starting utility...")
	for entry in listdir(ZIP_DIRECTORY):
		print("Unzipping " + entry)

		inputPath = ZIP_DIRECTORY + entry 

		with zipfile.ZipFile(inputPath, 'r') as zip_ref:
			zip_ref.extractall(OUTPUT_DIR)

def unzipList(list):
	print("Starting utility...")
	for entry in list:
		print("Unzipping " + entry)

		with zipfile.ZipFile(entry, 'r') as zip_ref:
			zip_ref.extractall(OUTPUT_DIR)

def deleteTempFiles():
	print("Deleting temp files...")
	for filename in os.listdir(OUTPUT_DIR):
		file_path = os.path.join(OUTPUT_DIR, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))