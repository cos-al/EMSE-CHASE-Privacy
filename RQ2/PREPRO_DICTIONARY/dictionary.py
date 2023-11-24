import pandas as pd
import os
import spacy
import numpy as np
import pickle
import seaborn as sns

user_story = "As a site member, I want to access to the Facebook profiles of other members so that I can share my experiences with them."
print(user_story)

from liwc_class import Liwc

dictionary = Liwc('privacydictionary_TAWC.dic')

dataset = "active_pr_dict.csv"
df = pd.read_csv(dataset, low_memory=False)
print(len(df.index))
out_df = pd.DataFrame(columns=['user_id', 'body', 'login', 'SENSITIVE [C]', 'SENSITIVE [J]'])
debug_counter = 0
for index, row in df.iterrows():
    debug_counter = debug_counter + 1
    if (debug_counter % 1000 == 0):
        print(debug_counter)
    # print(row[0])
    # print(row['body'])
    # print(row['login'])

    if not type(row['body']) is float:
        c, k = dictionary.parse(row['body'].lower().split(' '))
        categories = [list(i) for i in c.items()]
        #terms = [list(i) for i in k.items()]
        if len(categories) > 0:
            try:
                resu = map(lambda x: x[0], categories)
                row['SENSITIVE [C]'] = " ".join(resu)
                row['SENSITIVE [J]'] = k
                out_df = out_df.append(row, ignore_index=True)
            except Exception as e:
                print(e)

out_df.to_csv('parsed.csv')


