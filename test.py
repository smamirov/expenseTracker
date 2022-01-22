from datetime import datetime
from tokenize import Name
import sqlite3
'''
date = '01/17/2022'
dateObj = datetime.strptime(date, '%m/%d/%Y')
print(date, dateObj)
newdateObj = dateObj.strftime('%A %b %d, %Y')
print(date, newdateObj)'''

'''date = 'Monday Jan 17, 2022'
try: 
    dateObj = datetime.strptime(date, '%m/%d/%Y')
    formatted = dateObj.strftime('%A %b %d, %Y')
except NameError:
    formatted = date
except:
    dateObj = datetime.strptime(date, '%A %b %d, %Y')
    formatted = dateObj.strftime('%A %b %d, %Y')


print(formatted)


date = '01/17/2022'
dateObj = datetime.strptime(date, '%m/%d/%Y')
print('First', date, dateObj)
newdateObj = dateObj.strftime('%m/%d/%Y')
print('Here', date, newdateObj)'''

'''date = 'Monday Jan 17, 2022'
dateObj = datetime.strptime(date, '%A %b %d, %Y')
formatted = dateObj.strftime('%m/%d/%Y')
print(formatted)'''

'''# Create or connect to a database=
conn = sqlite3.connect('expenseTracker.db')
# Create a cursor
cursor = conn.cursor()
cursor.execute("""SELECT SUM(amount) FROM expenseTracker WHERE category LIKE 'Food/Eating Out%' """)
fTotal = cursor.fetchone()[0]
print(fTotal)'''

'''conn = sqlite3.connect('expenseTracker.db')
# Create a cursor
cursor = conn.cursor()

currentYear = datetime.now().year
values =  []
for i in range(1,10):
    cursor.execute(""" select sum(amount) from expenseTracker where date like ? or date like ? and date like ?""", ['0'+str(i)+'%', str(i)+'%','%' + str(currentYear)])
    monthlyTotals = cursor.fetchall()[0][0]
    if monthlyTotals is None:
        monthlyTotals = 0
    values.append(monthlyTotals)

print(values)

conn.commit()    
conn.close()
'''