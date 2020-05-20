'''
Program: FinalProject-Manjunath-0.py
Author: Manjunath Jayam
Purpose:Program to generate grouped bar chart using commodity data and user inputs.  
Revisions:Not yet
'''
#Step-1 importing the required modules
import csv
from datetime import datetime as dt
import plotly.offline as py
import plotly.graph_objs as go

#Step2-Reading the data from file and filtering the data
print(f'{"="*26}')
print(f'Analysis of Commodity Data')
print(f'{"="*26}')

data = []
date_list=[]
csvfile = open('produce_csv.csv','r') #open the data file to read
reader = csv.reader(csvfile)
for row in reader:  ###! main loop reads one row at a time
    if reader.line_num == 1: ###! get the location names from row 1
        locations = row[2:]  ###! slice to remove commodity and date
    else:
        for location,value in zip(locations,row[2:]):  ###! iterate through locations and values
            row_num = len(data)     ###! index for the data row 
            data.append(row[:1])    ###! new data row: commodity and date
            date_list.append(row[1])
            data[row_num].append(dt.strptime(row[1],'%m/%d/%Y'))###! append formatted date
            data[row_num].append(location)  ###! append location
            data[row_num].append(float(value.replace('$','')))     ###! append value
csvfile.close()

#Step3- Fetching the unique commodities/locations/dates 
# list named uComList which contains all the unique commodities in the data file
uComList=sorted(list(set([a[0] for a in data])))
# list named uDateList which contains all the unique dates in the data file
uDateList=sorted(list(set([a[1] for a in data])))
# list named uLocationList which contains all the unique locations in the data file
uLocationList=sorted(list(set([a[2] for a in data])))

#Step4- Diaplaying the available commodities/locations/dates and taking userinputs 
print(f'\nSELECT PRODUCTS BY NUMBER...')
#printing the available products, so that it will help user to select
for i,item in enumerate(uComList):
    print(f'<{str(i)}> {item}')
 
#taking inputs from user for the products
input_products=input("Enter product numbers separated by spaces:")
#adding the user selected products into a list
input_products_list=[uComList[int(i)] for i in input_products.split(' ')]

#printing the products which are selected by the user
print(f'Selected products:',end=' ')
for i in input_products_list:
    print(f'{i}',end=' ')
    
print(f'\n\nSELECT DATE RANGE BY NUMBER ...')
#printing the available dates so that user can select from the printed list
for i,item in enumerate(uDateList):
    print('<'+str(i)+'>',item.strftime('%Y-%m-%d'),end=' ')
   
#defining the start date and end date
start_date=uDateList[0].strftime('%Y-%m-%d')
end_date=uDateList[-1].strftime('%Y-%m-%d')

#printing the start date and end date
print(f'\nEarliest available date is:{start_date}')
print(f'Latest available date is:{end_date}')
#taking the dates input from the user
input_dates=input("Enter start/end Date numbers separated by a space:")
input_dates=[int(i) for i in input_dates.split(' ')]

#since dates input will be start date  and end date
#assigning the dates  inputs to the variables
date1=uDateList[input_dates[0]].strftime('%Y-%m-%d')
date2=uDateList[input_dates[1]].strftime('%Y-%m-%d')
#printing the start date and end date entered by user
print(f'Dates from {date1} to {date2}')

print(f'\nSELECT LOCATIONS BY NUMBER ...')
#printing the available locations to user
for i,item in enumerate(uLocationList):
    print(f'<{str(i)}> {item}')
 
#taking the location inputs from user
input_locations=input("Enter location numbers separated by spaces:")
input_locations_list=[uLocationList[int(i)] for i in input_locations.split(' ')]
  
print(f'Selected locations:',end=' ')
#printing the user selected locations
for i in input_locations_list:
    print(f'{i}',end=' ')

#Step5- selecting the data records based on the user given inputs
#selecting thelist of records which satisfies under user given inputs
select=list(filter(lambda x:x[0] in input_products_list and
(uDateList[input_dates[0]] <= x[1] <= uDateList[input_dates[1]])
and x[2] in input_locations_list,data)) 
print(f'\n{len(select)} records have been selected.')

#we can un-comment the below code if you want to display 
#the records which have been selected by user inputs
'''
print(f'\nRECORDS SELECTED ...')
for i,item in enumerate(select):
    print(f'<{i}> {item}')   
'''
#Step6-Creating the dictionary with the selected data
#for each product which are given by user inputs creating an empty dictionary
d1={each:{} for each in input_products_list}

for product in d1:
    for location in input_locations_list:
        #for each product in each location which are given by userinputs empty list is 
        #being added, so that it will be used to hold the multiple prices over the period
        d1[product].update({location:[]})

for item in select:
    #for each product in a particular location, the different prices over period are being added
    d1[item[0]][item[2]].append(item[3])
   

#Step7- Fetching the X-values and Y-values for the graph
print(f'\nTHE GROUPED BAR CHART IS DISPLAYED IN A BROWSER TAB …') 
#Empty list which will holds the data required to draw a grouped bar chart  
data1=[]
x_value=list(d1.keys()) #since x values are commodities which are keys of dictionaries

for loc in input_locations_list: #for each location in the user asked location
#since commodities(x-values are fixed, only y values are changing so in the beginning
#of each iteration we are defining an empty list to hold y values)
    y_value1=[] 
    for com in x_value: # for each commodity in the user input commodities
        #some locations doesnt have records of some commodities so its length is zero
        if(sum(d1[com][loc])!=0): # this condition avoids '/ divided by zero'
            y_value1.append(round((sum(d1[com][loc])/len(d1[com][loc])),2)) #Calculating the average and rounding it to 2 decimals
        else:
            y_value1.append(sum(d1[com][loc])) 
    #Each Trace variable holds x,y values of a particular location
    trace1=go.Bar(x=x_value,y=y_value1,name=loc) 
    data1.append(trace1) #appending the trace1 to the data1 which is of type list

#Step8-Plotting grouped Bar chart using the dictionary and other user given inputs
#defining the layout mode
layout=go.Layout(barmode='group')
#feeding the data to figure
fig=go.Figure(data=data1,layout=layout)
#Title for the GROUPED BAR CHART
title1=f'Product Price from {date1} through {date2}'
#defining the layout of the chart and title names and alignment 
fig.update_layout(
    title={
        'text': title1,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title = "Product", #X-axis title
    yaxis_title = "Average Price", #y-axis title
    )
fig.update_layout(yaxis_tickformat='$.2f') #FORMATTING THE Y-AXIS
#PLOTTING THE CHART IN BROWSER
#'grouped-bar.html' is the file name of the grouped bar chart
py.plot(fig,filename='grouped-bar.html') 

