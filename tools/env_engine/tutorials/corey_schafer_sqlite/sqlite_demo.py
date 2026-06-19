import sqlite3

conn = sqlite3.connect ('employee.db')

c = conn.cursor ()

# c.execute ("""CREATE TABLE employees (
#            first text,
#            last text,
#            pay integer
#            )""" )

c.execute ("INSERT INTO employees VALUES ('Jean-Marie', 'Grégoire', 6000)")

conn.commit()

c.execute ("SELECT * FROM employees WHERE last = 'Grégoire'") 

print (c.fetchall ())

conn.commit ()

conn.close ()
