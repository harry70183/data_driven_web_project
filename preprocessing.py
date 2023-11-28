# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 21:53:58 2023

@author: USER
"""

import pandas as pd
import numpy as np
import json

data = pd.read_csv("../data/spotify-2023.csv", encoding='latin-1')
data = data[(data["released_year"] == 2023) & (data["artist_count"]==2)].reset_index(drop=True)
feat = {"nodes":[], "edges":[]}    
final = {"artist":[],"feat":[], "track_name":[], "streams":[], "bpm":[], "valence_%":[],
         "energy_%":[], "danceability_%":[], "speechiness_%":[], "acousticness_%":[]}

all_artisit = []
for a in data["artist(s)_name"]:
    artist = a.split(',')
    artist = [a.strip() for a in artist]
    all_artisit += artist

cnt = 0
index = {}
for aa in list(set(all_artisit)):
    index[aa] = cnt
    cnt+=1
        
for i in range(len(data)):
    artist = data.loc[i, "artist(s)_name"].split(',')
    artist = [a.strip() for a in artist]
    final["artist"] += artist
    artist.reverse()
    final["feat"] += artist
    final["track_name"] += [data.loc[i, "track_name"]]*2
    final["streams"] += [int(data.loc[i, "streams"])]*2
    final["bpm"] += [data.loc[i, "bpm"]]*2
    final["valence_%"] += [data.loc[i, "valence_%"]]*2
    final["energy_%"] += [data.loc[i, "energy_%"]]*2
    final["danceability_%"] += [data.loc[i, "danceability_%"]]*2
    final["speechiness_%"] += [data.loc[i, "speechiness_%"]]*2
    final["acousticness_%"] += [data.loc[i, "acousticness_%"]]*2
    feat["edges"].append({"source":artist[0],
                          "target":artist[1],
                          "stream":int(data.loc[i, "streams"]),
                          "sourceIndex":index[artist[0]],
                          "targetIndex":index[artist[1]]})

final_data = pd.DataFrame(final)        
for artist in list(set(all_artisit)):
    total_streams = final_data[final_data['artist']==artist].streams.sum()
    feat["nodes"].append({"name":artist, 
                          "total_streams":total_streams})

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)    
    
final_data.to_csv("../data/spotify.csv",index=False)
with open("../data/feat.json", "w", encoding='utf8') as outfile:
    json.dump(feat, outfile, cls=NpEncoder, indent=2, ensure_ascii=False)

    

