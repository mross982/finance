from yahoo_finance import Share
import csv
from pprint import pprint
import sys
import os
import datetime
from dateutil.relativedelta import relativedelta
from pprint import pprint
import glob


def read_symbols(s_symbols_file):
    '''Read each line from a .txt file and return a list of symbols'''

    s_symbols_file = os.path.abspath(s_symbols_file)
    ls_symbols = []
    ffile = open(s_symbols_file, 'r')
    for line in ffile.readlines():
        str_line = str(line)
        if str_line.strip(): 
        	ls_symbols.append(str_line.strip())
    ffile.close()
  
    return ls_symbols 


def daily_update(ls_symbols, start_date, end_date):

	updates = []
	for symbol in ls_symbols:
		print symbol
		try:
			security = Share(symbol)
			print 'getting data from Yahoo...'
			tick = [
			security.get_historical(str(start_date), str(end_date))
			]
			for data in tick:
				updates.append(data)
		except:
			print 'Could not find data for ' + tick

	writedata(updates)


def writedata(updates):

	for items in updates:
		for thing in items:
			keys = thing[0].keys()
			print keys
			sys.exit(0)
			ticker_symbol = thing[0]['Symbol']
			path = 'C:\Python27\Lib\site-packages\QSTK\QSData\Yahoo'
		
			with open(path + '\\' + ticker_symbol + '.csv', 'wb') as csv_file:
				dict_writer = csv.DictWriter(csv_file, fieldnames = keys, restval = 'nan', extrasaction='ignore')
				dict_writer.writeheader()
				dict_writer.writerows(thing)

def makedir(path):
	try:
		os.makedirs(path)
	except:
		if not os.path.isdir(path):
			raise


# gives the opening price of the previous trading day
# print yahoo.get_open()
# gives the last price of the previous trading day
# yahoo.refresh()
# print yahoo.get_price()
# print yahoo.get_trade_datetime()

if __name__ == '__main__':

	end_date = datetime.date.today()
	start_date = end_date - relativedelta(years=1)

	script_dir = os.path.dirname(__file__)
	rel_path1 = "accounts\\*"
	rel_path2 = "accounts\\" 
	
	# print os.path.realpath(__file__) finds this script's path

	if len(sys.argv) == 1:
		for file in glob.glob(os.path.join(script_dir, rel_path1)):
			filename = file
			ls_symbols = read_symbols(filename)
			daily_update(ls_symbols, start_date, end_date)
	else: 
		filename = sys.argv[1]
		ls_symbols = read_symbols(os.path.join(script_dir, rel_path2, filename))
		daily_update(ls_symbols, start_date, end_date)