import datetime
import sqlite3 as f
connection=f.connect("Sales.db")                                                                                                                                                                               
cursor=connection.cursor()
cursor.execute("create table if not exists sales( Date datetime ,ProductID int,ProductName varchar(20),quantity int,Productprise int,Totalcost int,status varchar(20))")
connection.commit()
cursor.execute("create table if not exists admin( ProductID int,ProductName varchar(20),ProductType varchar(20),Productprice int,quantity int)")
connection.commit()
def createInventory():
  Run="yes"
  while Run=="yes":
   pid=int(input("enter the product ID----    "))
   pname=input("enter the product name---   Please Enter First letter in capital")
   ptype=input("enter the product type - {Grocery , dairy , cosmetics}---   ")
   price=int(input("enter the product price---- "))
   quantity=int(input("enter the product quantity----  "))
   cursor.execute("insert into admin(ProductID,ProductName,ProductType,Productprice,quantity)values({},'{}','{}',{},{})".format(pid,pname,ptype,price,quantity))
   connection.commit()
   Run=input("yes or not---     ")
                                                                                                                                                
def displayInventory():
  print("id-Name-Type-price-quantity")
  cursor.execute("select * from admin")
  display=cursor.fetchall()
  for row in display:
   print(row)                                                                                                                               
def modifyInventory():
  pid = int(input("enter the ID of the product"))
  cursor.execute('select ProductID from admin')
  listtt=[]
  new=cursor.fetchall()
  for i in new:
    for j in i:
      listtt.append(j)
  if pid not in listtt:
    print("no such  id")
  else:
    parameter=input("which parameter you wish to modify ? \n 1)productid \n 2)productname \n 3)producttype \n 4)productquantity \n 5)productprice\n please choose the option------   ")
    modifiedvalue = input("enter the updated value")
    if parameter=="productid":
      modifiedvalue=int(modifiedvalue)
      cursor.execute("update admin set ProductID = {} where ProductID = {}".format(modifiedvalue,pid))
      connection.commit()
    elif parameter=="productname":
      cursor.execute("update admin set ProductName = '{}' where ProductID = {}".format(modifiedvalue,pid) )
      connection.commit()
    elif parameter=="producttype":
      cursor.execute("update admin set ProductType = '{}' where ProductID = {}".format(modifiedvalue,pid) )
      connection.commit()
    elif parameter=="productquantity":
      modifiedvalue=int(modifiedvalue)
      cursor.execute("update admin set quantity = {} where ProductID = {}".format(modifiedvalue,pid))
      connection.commit()
    elif parameter=="productprice":
      modifiedvalue=int(modifiedvalue)
      cursor.execute("update admin set ProductPrice= {} where ProductID = {}".format(modifiedvalue,pid)  )
      connection.commit()
def deleteInventory():
  cursor.execute("select * from admin")
  display=cursor.fetchall()
  for row in display:
   print(row) 
  pid = int(input("enter the ID of the product to be deleted"))
  cursor.execute('select ProductID from admin')
  listtt=[]
  new=cursor.fetchall()
  for i in new:
    for j in i:
      listtt.append(j)
  if pid not in listtt:
    print("no such  id")
  else:
    cursor.execute("delete from admin where ProductID = {}".format(pid)    )
    connection.commit()
def searchInventory():
  pid = int(input("enter the product ID"))
  cursor.execute('select ProductID from admin')
  listtt=[]
  new=cursor.fetchall()
  for i in new:
    for j in i:
      listtt.append(j)
  if pid not in listtt:
    print("no such  id")
  else:
    cursor.execute("select * from admin where ProductID = {}".format(pid))
    display=cursor.fetchall()
    for row in display:
      print(row)
def createSales():
  now = datetime.datetime.now()
  Sqldateform=now.strftime('%Y-%m-%d %H:%M:%S.%f')
  name=input("enter the product name")
  pname=name.title()
  cursor.execute("select ProductName from admin")
  checking=cursor.fetchall()
  totalnames=[]
  for w in checking:
    for q in w:
      totalnames.append(q)
  if pname not in totalnames:
    print("sorry product does not excist")
    print(totalnames)
  else:
    cursor.execute("select ProductID,Productprice from admin where ProductName = '{}'".format(pname))
    row=cursor.fetchall()
    listt=[]
    for i in row:
      for j in i:
        listt.append(j)
    SalesProductID=listt[0]
    salesProductprice=listt[1]
    cursor.execute("select quantity from admin where ProductName = '{}'".format(pname))
    Salesquantity=int(input("enter the quantity so as to check Where the Quantity is available or not "))
    quantityrow=cursor.fetchall()
    Availablequantity=0
    for x in quantityrow:
      for m in x:
        Availablequantity+=m
    if (Salesquantity > int(Availablequantity)):
      print("understock ! request limited quantity")
    else:
      totalcost=salesProductprice*Availablequantity
      cursor.execute("insert into sales values('%s' , %s , '%s' , %s ,%s , %s,'%s')"%(Sqldateform,SalesProductID,pname,Availablequantity,salesProductprice,totalcost,'INITIAL'))
      connection.commit()
      cursor.execute("update admin set quantity = 0 where ProductName ='{}'".format(pname))
      connection.commit()
def displaySales():
  cursor.execute('select * from sales')
  display=cursor.fetchall()
  for i in display:
    print(i)
def sellproduct():
  pid=int(input("enter the productid u want to buy"))
  cursor.execute('select ProductID from sales')
  listtt=[]
  new=cursor.fetchall()
  for i in new:
    for j in i:
      listtt.append(j)
  if pid not in listtt:
    print("no such  id")
  else:
    cursor.execute("select quantity,ProductName,Productprise from sales where ProductID = {} and status = 'INITIAL'".format(pid))
    listt=[]
    row=cursor.fetchall()
    for i in row:
      for j in i:
        listt.append(j)
    sumsum=listt[0]
    pname=listt[1]
    salesProductprice=listt[2]
    soldquantity=int(input(("available quantity is",sumsum,"how much you want")))
    unsoldquantity=sumsum-soldquantity
    totalcost=unsoldquantity*salesProductprice
    now = datetime.datetime.now()
    Sqldateform=now.strftime('%Y-%m-%d %H:%M:%S.%f')
    cursor.execute("insert into sales values('%s' , %s , '%s' , %s ,%s , %s,'%s')"%(Sqldateform,pid,pname,unsoldquantity,salesProductprice,totalcost,'unsold'))
    connection.commit()
    cursor.execute("insert into sales values('%s' , %s , '%s' , %s ,%s , %s,'%s')"%(Sqldateform,pid,pname,soldquantity,salesProductprice,soldquantity*salesProductprice,'SOLD'))
    connection.commit()
def Again_sell_The_same_Product():
  pid=int(input("enter The product id u want to buy again"))
  cursor.execute("select quantity , Productprise from sales where ProductID = {} and status = 'INITIAL'".format(pid))
  listt=[]
  row=cursor.fetchall()
  for i in row:
    for j in i:
      listt.append(j)
  Totalquantity=listt[0]
  ProductPrice=listt[1]
  cursor.execute("select quantity from sales where ProductID = {} and status = 'unsold'".format(pid))
  listtt=[]
  row2=cursor.fetchall()
  for n in row2:
    for m in n:
      listtt.append(m)
  Availablequantity=listtt[0]
  print(Availablequantity,"the available quantity is")
  soldquantityplus=int(input("enter the quantity"))
  cursor.execute("update sales set quantity=quantity + {} where ProductID = {} and status = 'SOLD'".format(soldquantityplus,pid))
  connection.commit()
  cursor.execute("select quantity from sales where ProductID = {} and status = 'SOLD'".format(pid))
  listttt=[]
  row3=cursor.fetchall()
  for k in row3:
    for l in k:
      listttt.append(l)
  soldquantity=listttt[0]
  cursor.execute("update sales set Totalcost = {} where ProductID = {} and status = 'SOLD'".format(soldquantity*ProductPrice,pid))
  connection.commit()
  unsoldquantity=Totalquantity-soldquantity
  print(unsoldquantity)
  cursor.execute("update sales set quantity = {} where ProductID = {} and status = 'unsold'".format(unsoldquantity,pid))
  connection.commit()
  cursor.execute("update sales set Totalcost = {} where ProductID = {} and status = 'unsold'".format(unsoldquantity*ProductPrice,pid))
  connection.commit()
def deleteentries():
  pid = int(input("enter the ID of the product to be deleted"))
  cursor.execute('select ProductID from sales')
  listtt=[]
  new=cursor.fetchall()
  for i in new:
    for j in i:
      listtt.append(j)
  if pid not in listtt:
    print("no such  id")
  else:
    cursor.execute("delete from sales where ProductID = {}".format(pid)    )
    connection.commit()
  
def checkstock():
  pid=int(input("enter the product id to check the stock"))
  cursor.execute("select Productprice*quantity as totalcost , quantity from admin group by ProductID Having ProductID = {}".format(pid))
  row=cursor.fetchall()
  listt=[]
  for i in row:
    for j in i:
      listt.append(j)
  stockquantity=listt[1]
  stocktotalprice=listt[0]
  cursor.execute("select totalcost , quantity from sales where ProductID = {} and status = 'unsold' ".format(pid))
  row2=cursor.fetchall()
  listt2=[]
  for k in row2:
    for l in k:
      listt2.append(l)
  unsoldquantity=listt2[1]
  unsoldotalprice=listt2[0]
  cursor.execute("select totalcost , quantity from sales where ProductID = {} and status = 'SOLD' ".format(pid))
  row3=cursor.fetchall()
  listt3=[]
  for m in row3:
    for n in m:
      listt3.append(n)
  soldquantity=listt3[1]
  soldotalprice=listt3[0]
  print(soldquantity,"-------sold quantity of individual given product")
  print(unsoldquantity,"------unsold quantity of individual given product")
  print (stockquantity,"-----total stock quantity of individual given product")
def salesinventorycheck():
  cursor.execute('select sum(totalcost) from sales where status = "INITIAL" ')
  row=cursor.fetchall()
  totalcost=0
  listt=[]
  for i in row:
    for j in i:
      totalcost=totalcost+j
  cursor.execute("select sum(totalcost) from sales where status = 'SOLD'")
  row3=cursor.fetchall()
  soldtotalcost=0
  for m in row3:
    for n in m:
      soldtotalcost=soldtotalcost+n
  print(totalcost,"total cost in sales module")
  print(soldtotalcost,"Sum of the prices of individual product sold")
def inventory():
    print("welcome administrator")
    while(True):
        print("choose the operation to perform\n 1)create product\n 2)modify product \n 3)Display product \n 4)delete product \n 5)search product\n 6)Switch to sales \n  7)Exit\n 8) choose a product in sales \n   10) delete entries in sales \n please choose---------    ")
        choice = input()
        if(choice=='7'):
            break
        elif(choice=='1'):
            createInventory()
        elif(choice=='2'):
            modifyInventory()
        elif(choice=='3'):
            displayInventory()
        elif(choice=='4'):
            deleteInventory()
        elif(choice=='5'):
            searchInventory()
        elif(choice=='6'):
            sales()
        elif (choice=='8'):
            createSales()
        elif(choice=='10'):
          deleteentries()
def sales():
    print("Welcome salesperson !!")
    while(True):
        print("you can \n 1) choose a product \n   3)Display \n 4)sell products\n 10) Again sell a same product \n 5)Check stock \n 6)Stock-sales tally \n 7)quit )8 delete entries\n please choose------------     ")
        num=input("choose one")
        if(num=='7'):
            break
        elif (num=='1'):
            createSales()
        elif(num=='3'):
            displaySales()
        elif(num=='4'):
            sellproduct()
        elif(num=='10'):
            Again_sell_The_same_Product()
        elif(num=='5'):
            checkstock()
        elif(num=='6'):
            salesinventorycheck()
        elif(num=='8'):
          deleteentries()
            

print("**************************************************************\n")
print("WELCOME TO ABC SUPERMARKET !!!")
print("WELCOME ADMINISTRATOR ! \n You can access inventory and sales module \n")
print("**************************************************************\n")
num = int(input("enter 1 to continue \n--------      "))
if(num==1):
    inventory()
