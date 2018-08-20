import sqlite3
import csv
import datetime

conn = sqlite3.connect('metersDB.db')
c = conn.cursor()


def create_table():
	''' creates a table if it does not exist'''

	exists = c.execute("""
			select name from sqlite_master where type='table' and name='meters'
		""").fetchall()

	if not (exists and exists[0] and exists[0][0]):
		c.execute("""
			CREATE TABLE meters
				(id varchar, meter varchar, date datetime, status varchar)
		""")

def import_insert():
	'''reads csv files and insert the data in the table'''

	csv_files = ["cl-1-50.csv", "cl-51-100.csv", "cl-101-150.csv", "cl-151-200.csv",
		"cl-201-250.csv", "cl-251-300.csv", "cl-301-322.csv"]

	for i in csv_files:
		with open(i, 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				c.execute("""
					INSERT INTO meters
						VALUES ('{0}', '{1}', '{2}', '{3}')
				""".format(row[0], row[1], row[2], row[3]))
	conn.commit()

def calculate_log():
	'''for each meter calculate un-connected days'''

	out = {}
	meter_data = {}
	meters = c.execute("select distinct meter from meters").fetchall()
	for meter in meters:
		if meter[0]=='Meter': continue
		data = c.execute("""select * from meters where meter='{0}' order by id asc"""
			.format(meter[0])).fetchall()

		for row in data:
			date = datetime.datetime.strptime(row[2], "%d-%m-%Y %H:%M").date()
			out[date] = row[3]

		sorted_dates = sorted(out)
		un_connected = []

		for d in range(len(sorted_dates)-1):
			diff = (sorted_dates[d+1] - sorted_dates[d]).days - 1
			if diff > 0 and out[sorted_dates[d]]=='Disconnected':
				for i in range(diff):
					un_connected.append(sorted_dates[d] + datetime.timedelta(i+1))

		if un_connected:
			meter_data[meter[0]] = un_connected

	for d in meter_data:
		print("------------------------------------------")
		print("Days when Meter {0} stayed disconnected...".format(d))

		for k in meter_data[d]:
			print(k.strftime('%d-%m-%y'))

create_table()
import_insert()
calculate_log()

conn.close()