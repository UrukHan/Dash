from tqdm import tqdm
import psycopg2
import pandas as pd
import torch
import os
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go

class DashModel():
    
    def __init__(self):

        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')

        self.conn = psycopg2.connect(dbname=os.environ['MY_BD'], user=os.environ['MY_USER'], password=os.environ['MY_PASS'], host=os.environ['MY_HOST'], port=os.environ['MY_PORT'])
        self.cursor = self.conn.cursor()
        self.MODEL_NAME = 'model/'
        self.model = SentenceTransformer(self.MODEL_NAME).to(self.device)


    def get_data(self, amount, month, year):
        self.cursor.execute('SELECT posted_timestamp, link, description, source, title, cat_old FROM news LIMIT ' + str(amount))
        data = {'posted_timestamp': [], 'link': [], 'description': [], 'source': [], 'title': [], 'cat_old': []}
        for row in self.cursor:
            data['posted_timestamp'].append(row[0])
            data['link'].append(row[1])
            data['description'].append(row[2])
            data['source'].append(row[3])
            data['title'].append(row[4])
            data['cat_old'].append(row[5])
        df = pd.DataFrame(data)
        data = df[df['description'].str.contains("<|Г|կ|©|╟|ò|ä|Ð|Р|Ѕ|ê|å|ա|&|None", regex=True, na=True)==False]
        data = data[data['posted_timestamp'] < 2000000000]
        data['posted_timestamp'] = pd.to_datetime(data['posted_timestamp'], unit='s')
        data.sort_values('posted_timestamp', inplace = True, ascending=True)
        data = data.loc[(data['posted_timestamp'].dt.month == month) & (data['posted_timestamp'].dt.year == year)]
        data['description'] == data['description'].to_string()
        data['cat_old'] = [len(x) for x in data['title'].values]
        data = data.loc[data.cat_old > 20]
        data.drop_duplicates(subset=['description'], inplace = True)
        data.reset_index(drop = True, inplace = True)
        return(data)


    def simlarFil(self, data, coef, min, max):
        simlars = {}
        id = 0
        activ = []
        embeding = self.model.encode(data['title'].values)

        for k in tqdm(range(data.shape[0])):
            cheker = embeding[k]
            other = [j for i, j in enumerate(embeding) if i != k]
            cos = cosine_similarity([cheker], other)[0] 

            ind = False
            tmp = {}
            for i in range(len(cos)):
                if cos[i]>coef and i+1 not in activ:
                    if ind == False:
                        tmp['id'] = [k]
                        tmp['title'] = [data['title'].values[k]]
                        tmp['description'] = [data['description'].values[k]]
                        tmp['dt'] = [data['posted_timestamp'].values[k]]
                        tmp['source'] = [data['source'].values[k]]
                        tmp['link'] = [data['link'].values[k]]
                        activ.append(k)
                        ind = True
                    tmp['id'].append(i+1)
                    tmp['title'].append(data['title'].values[i+1])
                    tmp['description'].append(data['description'].values[i+1])
                    tmp['dt'].append(data['posted_timestamp'].values[i+1])
                    tmp['source'].append(data['source'].values[i+1])
                    tmp['link'].append(data['link'].values[i+1])
                    activ.append(i+1)
            
            if ind == True and len(tmp['title']) >= min and len(tmp['title']) <= max:

                tmp = pd.DataFrame(tmp).sort_values('dt', ascending=True)

                simlars[id] = tmp.reset_index(drop = True)
                id += 1
        return simlars

    def ploting(self, data, summs):

        fig = go.Figure()

        for i in list(data.keys()):
            dt = pd.Series(data[i]['dt'])
            text = [data[i]['title'][j] + '  -  (' + data[i]['source'][j] + ')' for j in range(len(data[i]['title']))]
            label = [data[i]['source'][j] for j in range(len(data[i]['title']))]
            urls = data[i]['link'].values

            x = []
            y = []
            for j in range(len(dt)):
                x.append(dt[j])
                y.append(j)

            fig.add_trace(go.Scatter(x=x, y=y, customdata=urls, text=text, mode='lines+markers', name = str(label[0]), marker=dict(size = 15), showlegend=True))

        fig.update_layout(legend_title_text='Original source', legend=dict(orientation="v", traceorder='reversed', font_size=16, bgcolor='#585858', bordercolor = '#ff7b3e')) #, title_text = "News Evalution"
        fig.update_layout(legend_font=dict(color = '#ff7b3e'))
        fig.update_layout(paper_bgcolor='#585858', plot_bgcolor='#585858')
        fig.update_xaxes(showline=True, linewidth=2, linecolor="#999", gridcolor='#ff7b3e', color='#ff7b3e', zerolinecolor='#ff7b3e')
        fig.update_yaxes(showline=True, linewidth=2, linecolor="#999", gridcolor='#ff7b3e', color='#ff7b3e', zerolinecolor='#ff7b3e')
        return fig