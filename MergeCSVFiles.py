import os,glob
import pandas as pd
import geopy.distance
import warnings
warnings.filterwarnings("ignore")

#Function to calculate distance between 2 geo coordinates
def dist(startlat,startlong,endlat,endlong):
    latdist=[]
    for slat,slong,elat,elong in zip(startlat,startlong,endlat,endlong):
        #Start lat and long
        cord_1=(slat,slong)
        #End Lat and long
        cord_2=(elat,elong)
        #cacluate distance between cordinates and append to a list to return
        latdist.append(round(geopy.distance.distance(cord_1,cord_2).miles,2))
    return(latdist)

source = './BikeData/' #Folder for CSV Files
csvfilespath = source + '2018*.csv' # Data for 2018 only
csvfiles = glob.glob(csvfilespath) #List of all files for 2018
firstfile = 0
totalrows = 0
# For each month file of 2018
for file in csvfiles:
    filename = file.split("\\")[-1]
    filemonth = filename.split('-')[0]
    print(f"Reading file {filename} for month {filemonth}")
    df = pd.read_csv(file)
    print(f"Total rows in {filename} is {len(df)}")
    df['tripduration']=df['tripduration']/60 #Convert trip duration to minutes
    # Trip duration is atleast a minimum of a minute and maximum of 30 min,as 30 mins is the general ridetime per rules
    df = df[(df['tripduration']<=30)&(df['tripduration']>=1)]
    print(f"Total rows after tripduration filter is {len(df)}")
    df['month'] = filemonth
    df['distance']=dist(df['start station latitude'],df['start station longitude'],df['end station latitude'],df['end station longitude'])
    df=df[(df['distance']>=0.49)] #Remove rides less than half miles
    print(f"Total rows after distance filter is {len(df)}")
    filerows = len(df)
    if (firstfile) == 0:
        df.to_csv('2018.csv',index=False)
        firstfile += 1
    else:
        df.to_csv('2018.csv',mode='a',header=False,index=False)
    totalrows += filerows
print(f"Total rows in 2018 file are {totalrows}")
