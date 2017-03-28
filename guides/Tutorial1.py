#! C:\Python27\python.exe

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def getdata(dt_start, dt_end, ls_symbols):
	"""
	start date, end date, stock symbols and returns price and volume arrays.
	"""
	dt_timeofday = dt.timedelta(hours=16)
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
	c_dataobj = da.DataAccess('Yahoo')
	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))
	na_price = d_data['close'].values
	na_volume = d_data['volume'].values
	return ldt_timestamps, na_price, na_volume

def normalize(na_price):
	"""
	divides each field by the first value in each field. Thus you get the 
	difference between start price and end price and normalize the data.
	"""
	na_normalized_price = na_price / na_price[0, :]
	return na_normalized_price


def risk(na_price):
	""" 
	Calculates the standard deviation of each column
	"""
	stdev = np.std(na_price)
	return stdev


def dailyReturns(na_price):
	"""
	takes price data and returns the normalized daily returns.
	"""
	na_rets = tsu.daily(na_price)
	return na_rets


def sharpeRatio(na_dailyReturns):
	"""
	takes daily returns data and returns the sharp ratio for each security
	"""
	sharpe_ratio = tsu.get_sharpe_ratio(na_dailyReturns)
	return sharpe_ratio


def cumulativeSum(na_dailyReturns):
	"""
	takes the daily returns array and returns the cumulative sum of each field.
	"""
	sum = np.sum(na_dailyReturns)
	return sum


def graph(ldt_timestamps, ls_symbols, na_rets, st_label, st_filename):
	"""
	takes the timestamps, symbols, and array of daily returns then creates 
	a line graph of the array.
	"""

	plt.clf()
	plt.plot(ldt_timestamps, na_rets)
	plt.legend(ls_symbols)
	plt.ylabel(st_label)
	plt.xlabel('Date')
	plt.savefig(st_filename, format='pdf')


def scatterplot(na_rets, ls_symbols, index1, index2, st_filename='scatterplot.pdf'):
	plt.clf()
	plt.scatter(na_rets[:, index1], na_rets[:, index2], c='blue')
	plt.ylabel(ls_symbols[0])
	plt.xlabel(ls_symbols[1])
	plt.savefig(st_filename, format='pdf')


if __name__ == '__main__':

	# Adjusted Close Graph
	startdate = dt.datetime(2010, 1, 1)
	enddate = dt.datetime(2010, 5, 31)
	symbols = ['GOOG','AAPL','GLD','XOM']
	timestamp, price, volume = getdata(startdate, enddate, symbols)
	normal_price = normalize(price)	
	
	label = 'Adjusted Close'
	filename = 'adjustedclose.pdf'
	graph(timestamp, symbols, normal_price, label, filename)

	# Daily Return Graph
	dR_enddate = dt.datetime(2010, 1, 31)
	dR_symbols = ['GOOG', 'AAPL']
	dR_timestamp, dR_price, dR_volume = getdata(startdate, enddate, dR_symbols)
	dR_normal_price = normalize(dR_price)
	daily_return = dailyReturns(dR_normal_price)
	label = 'Daily Returns'
	filename = 'dailyreturns.pdf'
	graph(timestamp, dR_symbols, daily_return, label, filename)

	#Scatter Plot
	index1 = 0
	index2 = 1
	scatterplot(daily_return, dR_symbols, index1, index2)
