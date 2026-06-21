import sqlite3
from employee import Employee

conn = sqlite3.connect ('employee.db')

c = conn.cursor ()

# c.execute ("""CREATE TABLE employees (
#            first text,
#            last text,
#            pay integer
#            )""" )

def insert_emp (emp):
    with conn:
        c.execute ("INSERT INTO employees VALUES (:first, :last, :pay)",
                   {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name (lastname):
    c.execute ("SELECT * FROM employees WHERE last = :last", {'last': lastname})
    return c.fetchall ()

def update_pay (emp, pay):
    with conn:
        c.execute ("""UPDATE employees SET pay = :pay
                   WHERE first = :first AND last = :last""",
                   {'first': emp.first, 'last': emp.last, 'pay': pay})

def remove_emp (emp):
    with conn:
        c.execute ("""DELETE from employees WHERE first = :first AND last = :last""",
                   {'first': emp.first, 'last': emp.last})


emp_1 = Employee ('Jean-Louis', 'Grégoire', 6500)
emp_2 = Employee ('Jean-Pierre', 'Grégoire', 9000)

insert_emp (emp_1)
insert_emp (emp_2)

emps = get_emps_by_name ('Grégoire')
print (emps)

update_pay (emp_2, 11000)
remove_emp (emp_1)

emps = get_emps_by_name ('Grégoire')
print (emps)

# print (emp_1.first)
# print (emp_1.last)
# print (emp_1.pay)

# c.execute ("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))

# conn.commit ()

# - DATA DUPLICATE DELETION - START
# c.execute ("SELECT rowid, * FROM employees WHERE last = 'McCartney'")
# print (c.fetchall())

# c.execute ("DELETE FROM employees WHERE rowid = :id_to_remove", {'id_to_remove': 4})
# - DATA DUPLICATION DELETION - END

# c.execute ("INSERT INTO employees VALUES (:first, :last, :pay)",
#            {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay})

# conn.commit ()

# c.execute ("INSERT INTO employees VALUES ('Jean-Marie', 'Grégoire', 6000)")

# conn.commit() 

# conn.commit ()

conn.close ()
