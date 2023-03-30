from flask import Flask, render_template
import pandas as pd
import requests
import os 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html", title="Home")


@app.route('/chart1')
def chart1():
    url = 'https://dev157572.service-now.com/api/now/table/incident?sysparm_display_value=all&sysparm_fields=sys_class_name%2Ccategory%2Cseverity%2Ccorrelation_display%2Cclose_code'

# Eg. User name="admin", Password="admin" for this code sample.
    user = os.getenv("USER")
    pwd = os.getenv("PASSWORD")

# Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )
    #print(response.status_code)
# Check for HTTP codes other than 200
    try:

# Decode the JSON response into a dictionary and use the data
        data = response.json()
    
        severity = []
        category=[]
        index1 = 0
    #This graph shows the categories that have severe incidents
    
        high_cat= []
        high_value = []
        low_cat=[]
  
        for severe in data['result']:
            severity.append(data['result'][index1]['severity']['value'])
            category.append(data['result'][index1]['category']['value'].upper())
            if severity[index1] == '1':
                high_cat.append(category[index1])
                high_value.append(severity[index1])
            else:
                low_cat.append(category[index1].upper())
            index1 +=1
        cat= []
        values = []
        for i in high_cat: 
            if i not in cat: 
                cat.append(i)
        for i in cat:
            count = pd.Series(high_cat).value_counts()
            values.append(count[i])

        return render_template("index.html", title="Graph 1", cat=cat, values=values)

    except:
        return render_template("hibernate.html")



@app.route('/chart2')
def chart2():
    url = 'https://dev157572.service-now.com/api/now/table/incident?sysparm_display_value=all&sysparm_fields=sys_class_name%2Ccategory%2Cseverity%2Ccorrelation_display%2Cclose_code'

# Eg. User name="admin", Password="admin" for this code sample.
    user = os.environ.get("USER")
    pwd = os.environ.get("PASSWORD")
    print(user," ", pwd)
# Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )

# Check for HTTP codes other than 200
   

# Decode the JSON response into a dictionary and use the data
    try:

        data = response.json()
        print(data)
        severity = []
        category=[]
        index1 = 0
    #This graph shows the categories that have severe incidents
    
        high_cat= []
        high_value = []
        low_cat=[]
  
        for severe in data['result']:
            severity.append(data['result'][index1]['severity']['value'])
            category.append(data['result'][index1]['category']['value'].upper())
            if severity[index1] == '1':
                high_cat.append(category[index1])
                high_value.append(severity[index1])
            else:
                low_cat.append(category[index1].upper())
            index1 +=1
        cat= []
        values = []
    #get categories without repetitions
        for i in low_cat: 
            if i not in cat: 
                cat.append(i)
            #get values
        for i in cat:
            count = pd.Series(low_cat).value_counts()
            values.append(count[i])
        #no empty categories
        for i in cat:
            if i == '':
                j = cat.index(i)
                cat[j] = 'UNKNOWN'

        return render_template("chart2.html", title="Graph 2", cat=cat, values=values)

    except:

                return render_template("hibernate.html")
