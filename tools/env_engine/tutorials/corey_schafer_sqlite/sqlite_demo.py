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

print (emp_1.first)
print (emp_1.last)
print (emp_1.pay)

# c.execute ("INSERT INTO employees VALUES ('Jean-Marie', 'Grégoire', 6000)")

# conn.commit()

# c.execute ("SELECT * FROM employees WHERE last = 'Grégoire'") 

# print (c.fetchall ())

conn.commit ()

conn.close ()
