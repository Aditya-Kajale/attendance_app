class Faculty:

  # Constructor
    def __init__(self, id, name, subject):
        self.id = id
        self.name = name
        self.subject  = subject
 
    # Function to create and append new student
    def accept(self, id, Name, Subject):
        ob = Faculty(id, Name, Subject)
        ls.append(ob)
 
    # Function to display student details
    def display(self, ob):
        print("ID : ", ob.id)
        print("Name : ", ob.name)
        print("Subject : ", ob.subject)
 
    # Search Function
    def search(self, rn):
        for i in range(ls.__len__()):
            if(ls[i].id == rn):
                return i
 
    # Delete Function
    def delete(self, rn):
        i = obj.search(rn)
        del ls[i]
 
    # Update Function
    def update(self, rn, No):
        i = obj.search(rn)
        roll = No
        ls[i].id = roll

    def getSubject(self,rn):
        i = obj.search(rn)
        return ls[i].subject

ls = []
obj = Faculty(0,'', [])


obj.accept(1,"A", ['1','2'])
obj.accept(2,"B", ['3','4'])
obj.accept(3,"C", ['4','6'])

# for i in ls:
#     obj.display(i)

print(len(ls))




 

