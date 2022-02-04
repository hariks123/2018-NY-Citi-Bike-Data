import requests
from zipfile import ZipFile
import os,glob

# URL for CitiBike Trip Data
base_url = 'https://s3.amazonaws.com/tripdata/'
#Years for which we are analyzing data
years = [2018,2019,2020,2021]
source = './zipfiles/' #Folder for zipfiles
target = './BikeData/' #Folder for CSV Files

#delete zip files in source folder
delfilespath = source + '*.zip'
delfiles = glob.glob(delfilespath)
for file in delfiles:
    print(f"Deleting file {delfilespath+'/'+file}")
    os.remove(file)

for yr in years: # For each Year
    for m in range(1,13): # For each Month
        if m < 10: #create File name prefix as YYYYMM
            prefix = str(yr) +str(0) + str(m)
        else:
            prefix = str(yr) + str(m)
        file_name = prefix + '-citibike-tripdata.csv.zip'  #Create File name
        url = base_url + file_name #Cretae URL to be used for downloading
        print(f"Downloading {url}")
        req=requests.get(url) #Get response from URL
        file_path = source + file_name #Specify the folder where zip file is to  be downloaded
        with open(file_path,'wb') as out_file:
            out_file.write(req.content) #write content to zipfile
        print(f'{file_path},File downloaded')

#delete csv files in target
delfilespath = target + '*.csv'
delfiles = glob.glob(delfilespath)
for file in delfiles:
    print(f"Deleting file {delfilespath+'/'+file}")
    os.remove(file)

for f in os.listdir(source): #Read all files in the zip folder
    if f.endswith('.zip'):
        filename = source + f
        print(f"Unzipping {filename}")
        zip_ref = ZipFile(filename)
        zip_ref.extractall(target) #Extract zip file to target file name


