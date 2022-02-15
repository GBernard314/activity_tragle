import datetime
import json
import os
import time

year = 2021
activity_type = 'MOTORCYCLING'


def timing_activity(year: int, activity_type: str) -> dict:   
    tot = {}
    path_files = os.path.join('data', 'Semantic Location History', str(year))
    for filename in os.listdir(path_files):
        file_path = path_files + '/' + filename
        with open(file_path) as rec:
            tot[filename[:-5]] = {'total_km': 0, 'total_min': 0}
            activity = json.load(rec)
            for act in activity['timelineObjects']:
                if 'activitySegment' in act.keys(): # 2022-02-01T06:45:36.262Z
                    if act['activitySegment']['activityType'] == activity_type:
                        if '.' in act['activitySegment']['duration']['startTimestamp']:
                            start = datetime.datetime.strptime(act['activitySegment']['duration']['startTimestamp'], "%Y-%m-%dT%X.%fZ")
                        else:
                            start = datetime.datetime.strptime(act['activitySegment']['duration']['startTimestamp'], "%Y-%m-%dT%XZ")
                        if '.' in act['activitySegment']['duration']['endTimestamp']:
                            end = datetime.datetime.strptime(act['activitySegment']['duration']['endTimestamp'], "%Y-%m-%dT%X.%fZ")
                        else: 
                            end = datetime.datetime.strptime(act['activitySegment']['duration']['endTimestamp'], "%Y-%m-%dT%XZ")
                        minutes = round((end - start).seconds / 60)
                        tot[filename[:-5]]['total_km'] += act['activitySegment']['distance'] / 1000
                        tot[filename[:-5]]['total_min'] += minutes

    for month in tot.keys():
        if(month in tot.keys()):
            tot[month]['total_km'] = round(tot[month]['total_km'], 1)
            if tot[month].get('total_min', 0) >= 60:
                tot[month]['total_time'] = {}
                tot[month]['total_time']['hours'] = round(tot[month]['total_min'] / 60)
                tot[month]['total_time']['minutes'] = tot[month]['total_min'] % 60
                tot[month].pop('total_min')
    return tot

def timing_act_all(activity_type: str) -> dict:    
    years =  os.listdir(os.path.join('data', 'Semantic Location History'))
    tot = {}
    for y in years:
        tot[y] = []
        tot[y].append(timing_activity(y, activity_type))    
    return tot
        

# time_2022 = timing_activity(year, activity_type)
# print(json.dumps(time_2022, indent=2))

all_time = timing_act_all('MOTORCYCLING')
with open(os.path.join('data', 'all_time.json'), 'wt') as output:
    json.dump(all_time, output, indent=2)