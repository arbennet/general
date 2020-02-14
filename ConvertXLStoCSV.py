import pandas as pd
import csv
import os
from configparser import ConfigParser

# get config file values
config = ConfigParser()
config_file = os.path.join(
    os.path.dirname(__file__), 'ConvertXLStoCSV.ini')
config.read(config_file)

path = config.get('main', 'path')
sheet_name = config.get('main', 'sheetname')

# get files in directory
files = os.listdir(path)


def truncate_file(path):
    """
    This will take an existing file and truncate it
    """
    with open(path, 'w') as fh:
        pass


def get_csv_extension(path):
    """
	Strips file extension and returns a '.csv' extension
    """
    filename, extension = os.path.splitext(path)

    return f"{filename}.csv"


def csv_from_excel(path):
	"""
	Truncate existing csv, write xls data
	"""
	csv_path = get_csv_extension(path)
	
	df = pd.read_excel(path, sheetname=sheet_name)
	
	# truncate **only** files you're writing to
	truncate_file(csv_path)
	
	# write to file
	df.to_csv(csv_path, index=False, quotechar= '"', quoting=csv.QUOTE_ALL)
	
	return


for file in files:
	if file.endswith('.xls'):
		xls_path = os.path.join(path, file)
		csv_from_excel(xls_path)
	else:
		pass