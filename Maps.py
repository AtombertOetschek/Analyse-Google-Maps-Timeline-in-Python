import json
import pandas as pd
from matplotlib import pyplot as plt
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
import numpy as np


year=['2018','2019','2020','2021']

for y in year:
    #add the path of the maps json files in datadir, leave the path after Maps/ intact
    datadir=r'Yourpath/Maps/takeout-20220123T151749Z-001/Takeout/Location History/Semantic Location History/'+y+'/'

    file = [f for f in listdir(datadir) if isfile(join(datadir, f))]
    filelist=[]
    for i in range(0,len(file)):
        fp_2020 = str(datadir)+'/'+str(file[i])
        filelist.append(fp_2020)


    data_list = []
    for file in (filelist):
        json_path = file
        json_data = pd.read_json(json_path)
        data_list.append(json_data)


    act=['IN_PASSENGER_VEHICLE','WALKING', 'IN_BUS', 'IN_TRAIN', 'CYCLING', 'IN_TRAM', 'MOTORCYCLING', 'IN_VEHICLE','SKIING']
    
    for x in act:
        try:
            type=[]
            distance=[]
            time=[]
            for l in range(0,len(filelist)):
                with open (filelist[l], encoding="utf8") as f:
                    data = json.load(f)  
                    df = pd.DataFrame(data)
                    for i in range(0,len(df)):
                        try:   
                            if (df.timelineObjects[i]['activitySegment']['distance'])>0 and (df.timelineObjects[i]['activitySegment']['activityType']) == x:    
                                if (df.timelineObjects[i]['activitySegment']['confidence']) == 'HIGH':  
                                    ty = df.timelineObjects[i]['activitySegment']['activityType']
                                    type.append(ty)
                                    t = df.timelineObjects[i]['activitySegment']['duration']['startTimestamp']
                                    time.append(t)
                                    d = (df.timelineObjects[i]['activitySegment']['distance'])/1000
                                    distance.append(d)
                        except:
                            pass
            month=[]
            for i in range(0,len(time)):
                m = time[i][0:10]
                month.append(m)    
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthdt=pd.to_datetime(pd.Series(month), format='%Y-%m-%d')
            values=list(zip(type,distance))
            maps=pd.DataFrame(values, columns=['Type','Distance'], index=monthdt)
            dissum=maps.Distance.resample('Y').sum()
            maps_rs = maps.resample('M').sum()
            fig, ax = plt.subplots(figsize=(8, 6))            
            maps_rs.plot.bar()
            plt.legend(['Sum = '+str(dissum.values)+' km'])
            plt.ylabel('Distance in km')
            plt.title('Distance traveled '+x+' '+y+'')
            plt.xticks(np.linspace(0,11,12), months)
            plt.savefig(r"C:/Users/bpges/Desktop/scripts/Plots/"+'Distance'+y+' '+x+'.png',dpi=300)        
        except:
            print(x+' was not performed')