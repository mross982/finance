from yahoo_finance import Share
import csv
from pprint import pprint
import sys
import os
import datetime
from dateutil.relativedelta import relativedelta
from pprint import pprint

def find_files(abs_file_path):
	if len(sys.argv) == 1:
		for file in os.listdir(abs_file_path):
			filename = file
			read_symbols(filename)
	else: 
		filename = sys.argv[1]
		read_symbols(filename)

def read_symbols(s_symbols_file):
    '''Read a list of symbols'''
    print s_symbols_file
    s_symbols_file = os.path.abspath("Fund_data\\" + s_symbols_file)
    ls_symbols = []
    ffile = open(s_symbols_file, 'r')
    for line in ffile.readlines():
        str_line = str(line)
        if str_line.strip(): 
            ls_symbols.append(str_line.strip())
    ffile.close()
    return ls_symbols 

def daily_update(account, start_date, end_date):

	updates = []
	for sec in account:
		try:
			security = Share(sec)
			tick = [
			security.get_historical(str(start_date), str(end_date))
			]
			updates.append(tick)
		except:
			print 'No data for ' + tick
			pass

	writedata(updates)


def writedata(updates):

	for items in updates:
		for thing in items:
			# for security in thing:
			keys = thing[0].keys()
			ticker_symbol = thing[0]
			print ticker_symbol
			ticker_symbol = ticker_symbol['Symbol']
			print ticker_symbol
			path = 'C:\Users\Michael\Anaconda3\envs\QSTK\Lib\site-packages\QSTK\QSData\Yahoo'
		
			with open(path + '\\' + ticker_symbol + '.csv', 'wb') as csv_file:
				dict_writer = csv.DictWriter(csv_file, fieldnames = keys, restval = 'NAN', extrasaction='ignore')
				dict_writer.writeheader()
				dict_writer.writerows(thing)


			# try:
			# 	os.makedirs(path)
			# except:
			# 	if not os.path.isdir(path):
			# 		raise


# gives the opening price of the previous trading day
# print yahoo.get_open()
# gives the last price of the previous trading day
# yahoo.refresh()
# print yahoo.get_price()
# print yahoo.get_trade_datetime()

if __name__ == '__main__':

	script_dir = os.path.dirname(__file__)
	rel_path = "Fund_data\\" 
	abs_file_path = os.path.join(script_dir, rel_path)

	ls_symbols = find_files(abs_file_path)

	end_date = datetime.date.today()
	start_date = end_date - relativedelta(years=1)

	daily_update(ls_symbols, start_date, end_date)
