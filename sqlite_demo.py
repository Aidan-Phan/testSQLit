import sqlite3
from employee import Employee



conn = sqlite3.connect('employee.db')

c = conn.cursor()

#c.execute("""CREATE TABLE employees (
#          first text,
#          last text,
#          pay integer
#          )""")

# emp_1 = Employee('Aidan', 'Phan', 456)
# emp_2 = Employee('Aaron', 'Phan', 654)
# emp_3 = Employee('Aidan', 'Phan', 456)

def insertEmp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

def getEmpByName(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchall()

def updatePay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                     WHERE first = :first AND last = :last""",
                     {'first': emp.first, 'last': emp.last, 'pay': pay})
    
#c.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))

#conn.commit()

#c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay})

#conn.commit()
#c.execute("INSERT INTO employees VALUES (first, last, pay)")

emps = getEmpByName('Phan')
print(emps)

# update = updatePay()




# c.execute("SELECT * FROM employees WHERE last=?", ('Schafer',))

# print(c.fetchall())

# c.execute("SELECT * FROM employees WHERE last=:last", {'last': 'Phan'})

# print(c.fetchall())

# conn.commit()

conn.close()