from datetime import datetime
import time
import pandas as pd
import datetime
import threading as th
from utils import get_random_cp
import xlsxwriter

last_time = None
global_instruments_set = set()
excel_sheet = "./candles_formed.xlsx"
triggering_instruments_list = []

def set_tp_sl(instruments):
	global triggering_instruments_list
	for instrument in instruments:		
		if(len(triggering_instruments_list)==0):
			print("stock details = ",instrument)
			res = input("interested in this instrument?(Y/N) = ")
			if res == "Y":
				sl = int(input("enter sl = "))
				tp = int(input("enter target = "))
				triggering_instruments_list.append((instrument,sl,tp))
		else:
			for updated_instrument in triggering_instruments_list:
				if(instrument!=updated_instrument[0]):
					print("stock details = ",instrument)
					res = input("interested in this instrument?(Y/N) = ")
					if res == "Y":
						sl = int(input("enter sl = "))
						tp = int(input("enter target = "))
						triggering_instruments_list.append((instrument,sl,tp))
	print("done")

def get_instruments_from_excel():
	global excel_sheet
	instruments = []
	global temp
	temp=[]
	temp.append("stock name")
	df = pd.read_excel(excel_sheet)
	for j in df["stock name"]:
		instruments.append(j)
		temp.append(j)
	return instruments

# * Will get the instruments ordered by phone also
def get_instruments_from_all_orders():
	return ["9th stock"]

# * Merges the instruments in excel and by phone also
def get_instruments():
	instruments = set(get_instruments_from_all_orders() + get_instruments_from_excel())
	return instruments

# * only gives the updated list of instruments if the time interval is 15 minutes
def get_instruments_for_15_minutes():
	global last_time
	global global_instruments_set
	time_delta = 0
	if last_time is not None:
		time_delta = (datetime.datetime.now() - last_time).seconds
	if time_delta >= 120 or time_delta == 0:
		print(datetime.datetime.now())
		last_time = datetime.datetime.now()
		global_instruments_set = get_instruments()
		t1 = th.Thread(target=set_tp_sl,args=[global_instruments_set])
		t1.start()
	return global_instruments_set

def get_current_price():
	instruments = get_instruments_for_15_minutes()
	#TODO get current price
	instruments_with_cp = get_random_cp(instruments)
	return instruments_with_cp


def buy(instrument):
	pass
	#TODO buy the particular trade

def sell(instrument):
	pass
	#TODO sell the particular trade

def execute(operation,instrument,msg):
	print(instrument,"executing",msg)
	if operation == "BUY":
		buy(instrument)
	else:
		sell(instrument)

def check_target_and_sl():
	instruments_wt_cp = get_current_price()
	global triggering_instruments_list
	triggered_instruments = []
	for trigger_instrument in triggering_instruments_list:
		for i in instruments_wt_cp:
			if trigger_instrument[0] == i[0]:
				if trigger_instrument[1] >= i[1]:
					execute("BUY",trigger_instrument[0],"sl reached")
					triggered_instruments.append(trigger_instrument[0])
				elif trigger_instrument[2] <= i[1]:
					execute("BUY",trigger_instrument[0],"target reached")
					triggered_instruments.append(trigger_instrument[0])
	row=0
	for i in triggered_instruments:
		for j in triggering_instruments_list:
			if j[0] == i:
				triggering_instruments_list.remove(j)
				temp.remove(i)
				workbook = xlsxwriter.Workbook('candles_formed.xlsx')
				worksheet = workbook.add_worksheet()
				for item in temp:
					worksheet.write(row,0, item)
					row += 1    
				workbook.close()
				break

while True:
	time.sleep(1)
	check_target_and_sl()

