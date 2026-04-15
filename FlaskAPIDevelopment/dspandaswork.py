import pandas as pd
import numpy as np
import json, requests

url = "https://companysubdomain.bamboohr.com/api/v1/time_off/whos_out"
API_KEY = "1234"


emp_list = pd.read_csv("FlaskAPIDevleopment/Employees.csv")
# print(emp_list.columns.tolist())

def employee_status():
    d = emp_list.groupby("Employment Status")[["First Name", "Last Name", "Employment Status"]]
    # d_dic =  {"emp" : d}
    result = {}
    for status, group in d:
  ##tolist to convert o string . columns/values
    #or
       
        result[status] = group.to_dict("records")
        # print(status)
        # print(group)
        # print("\n" + "-"*60 + "\n")
    return result
def fulltime():
    j = emp_list[emp_list["Employment Status"] == "Employee - FT"][["First Name", "Last Name"]]
    return j.to_dict("records")


def emp_by_status(user_status, methods = ["post"]):
    k = emp_list[emp_list["Employment Status"] == user_status][["First Name", "Last Name"]]
    return k.to_dict("records")

def timeoff():
    
    headers = {"accept": "application/json"}
#jdo v koi api doosre tool vli connect krni a a, get response in url. requests.get
    response = requests.get(url, auth=(API_KEY, "x"), headers=headers)
    data = response.json()        
    timeoff_list = pd.DataFrame(data)  
    return timeoff_list.to_dict("records")


###WE just need dctonaries to convert to jsonify

# response.json() — converts text to dictionary
# pd.DataFrame() — converts dictionary to DataFrame
# .to_dict() — converts DataFrame to dictionary
# jsonify() — converts dictionary to JSON

# request = someone knocking on YOUR door
# requests = YOU knocking on BAMBOOHR's door