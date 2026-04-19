# import json

# class Database:
    
#     def insert (self,name, email, password):
#         with open("users.json", "r") as rf :
#             users = json.load(rf)
#             if email in users:
#                return 0
#             else:
#                 users[email] = [name, password]
        
#         with open("users.json", "w") as wf :
#             json.dump(users,wf, indent=4)
#             return 1








import json
import os

class Database:

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

    def insert(self, name, email, password):

        # create file if not exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as wf:
                json.dump({}, wf)

        # read file safely
        try:
            with open(self.file_path, "r") as rf:
                users = json.load(rf)
        except:
            users = {}

        if email in users:
            return 0
        else:
            users[email] = [name, password]

        with open(self.file_path, "w") as wf:
            json.dump(users, wf)

        return 1
    

    def search(self, email, password):
        with open (self.file_path, "r") as rf :
            users = json.load(rf)
            if email in users:
                if users[email][1] == password:  ############>>> very important to learn, it is list so, see how value is fetch
                    return 1                         ## if it would be dict, then dic name an dkey name aa jana c, ex, database[email["password"]]
                else :
                    return 0
                
            else:
                return 0