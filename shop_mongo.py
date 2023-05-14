from pymongo import MongoClient
from bson.objectid import ObjectId

def get():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['shop']

db=get()
item_data=db["item"]
cus_data=db["Customer"]
order_data=db["order"]

def insert_item(name,cost,qty):
    ite={"name":name,"cost":cost,"qty":qty}
    item_data.insert_one(ite)

def insert_cus(name,phno,doorno,Street,city):
    cus={"name":name,"phno":phno,"address":{"doorno":doorno,"street":Street,"city":city}}
    cus_data.insert_one(cus)
def insert_order(item,cus,tot):
    dat={"item":item,"cus":cus,"tot":tot}
    order_data.insert_one(dat)

def get_item():
    return item_data.find()

def get_cus(cid):
    return cus_data.find_one(ObjectId(cid))

def update_item(id,new_qty):
    item_data.update_one({"_id":id},{"$set":{"qty":new_qty}})


if __name__ == "__main__":
    while(True):
        print("1)Admin")
        print("2)Customber")
        print("3)EXIT")
        ch0=int(input("Enter choice:"))
        if ch0==1:
            print()
            print("1) Add item")
            print("2) Update quantity")
            ch1=int(input("enter choice: "))
            if ch1==1:
                name=input("Enter name: ")
                cost=float(input("Enter cost: "))
                qty=int(input("Enter quantity: "))
                insert_item(name,cost,qty)
            if ch1==2:
                data=get_item()
                ldata=list(data)
                j=0
                for i in ldata:
                    print(j,"\t",i["_id"],"\t",i["name"],"\t\t",i["cost"],"\t",i["qty"])
                    j+=1
                ind=int(input("Enter product no: "))
                new_val=int(input("Enter new quantity"))
                update_item(ldata[ind]["_id"],new_val)
        elif ch0==2:
            print()
            print("1)Add customber")
            print("2)Bill")
            ch1=int(input("Enter choice: "))
            if ch1==1:
                name=input("Enter name: ")
                phno=int(input("Enter phone no: "))
                door=int(input("Enter door no: "))
                stre=input("Enter street: ")
                city=input("Enter city: ")
                insert_cus(name,phno,door,stre,city)
            elif ch1==2:
                cid=input("enter id: ")
                data=get_cus(cid)
                data1=get_item()
                ldata=list(data1)
                j=0
                for i in ldata:
                    print(j,"\t",i["_id"],"\t",i["name"],"\t\t",i["cost"],"\t",i["qty"])
                    j+=1
                lis=[]
                t=0
                while(True):
                    ind=int(input("Enter product no or '-1': "))
                    if ind==-1:
                        break
                    q=int(input("Enter quantity: "))
                    if ldata[ind]["qty"]>q:
                        update_item(ldata[ind]["_id"],ldata[ind]["qty"]-q)
                        lis.append({"item_id":ldata[ind]["_id"],"name":ldata[ind]["name"],"qty":q,"cost":ldata[ind]["cost"]*q})
                        t+=ldata[ind]["cost"]*q
                    else:
                        print("quantity is not possible")
                insert_order(lis,data,t)
                print("Thanks for order")

        elif ch0==3:
            break