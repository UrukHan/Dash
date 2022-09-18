#%%
import psycopg2
import pandas as pd


# %%


conn = psycopg2.connect(dbname='parser', user='postgres', password='8nNcZVs', host='51.250.84.80', port=32345)



# %%

cursor = conn.cursor()


# %%

cursor.execute('SELECT posted_timestamp, link, description, source, title, cat_old FROM news LIMIT ' + str(5000))


# %%

data = {'posted_timestamp': [], 'link': [], 'description': [], 'source': [], 'title': [], 'cat_old': []}
for row in cursor:
    data['posted_timestamp'].append(row[0])
    data['link'].append(row[1])
    data['description'].append(row[2])
    data['source'].append(row[3])
    data['title'].append(row[4])
    data['cat_old'].append(row[5])
df = pd.DataFrame(data)
df
# %%
