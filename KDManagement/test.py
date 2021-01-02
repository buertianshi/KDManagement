import pymssql
import pyodbc
#conn = pymssql.connect("127.0.0.1:8553", "sqltest", "999620", "homework")
#conn = pymssql.connect(host='localhost', port='8553', user='sqltest01', password='19990620', database='homework')
"""

print('1')
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
print('2')
cursor=conn.cursor()
sql = "select isnull((select top(1) 1 from userAndPassword where username='yuelei'), 0)"
print('3')
cursor.execute(sql)
row=cursor.fetchone()
row=list(row)[0]
conn.close()
print(row)
"""

if not (True or  False):
    print("a")