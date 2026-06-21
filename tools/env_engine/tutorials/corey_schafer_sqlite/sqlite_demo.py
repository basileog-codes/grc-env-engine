import sqlite3
from employee import Employee

conn = sqlite3.connect ('employee.db')

c = conn.cursor ()

# c.execute ("""CREATE TABLE employees (
#            first text,
#            last text,
#            pay integer
#            )""" )

emp_1 = Employee ('Paul', 'McCartney', 6500)
emp_2 = Employee ('John', 'Lennon', 9000)

# print (emp_1.first)
# print (emp_1.last)
# print (emp_1.pay)

# c.execute ("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))

# conn.commit ()

# c.execute ("SELECT rowid, * FROM employees WHERE last = 'McCartney'")
# print (c.fetchall())

c.execute ("DELETE FROM employees WHERE rowid = :id_to_remove", {'id_to_remove': 4})

# c.execute ("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay})

# c.execute ("INSERT INTO employees VALUES ('Jean-Marie', 'Grégoire', 6000)")

# conn.commit()

# c.execute ("SELECT * FROM employees WHERE last = 'McCartney'") 

# print (c.fetchall ())

conn.commit ()

conn.close ()
