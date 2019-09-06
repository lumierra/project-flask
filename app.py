from flask import Flask, render_template, redirect, abort, request, flash, Markup
from flask_paginate import Pagination, get_page_parameter
from IPython.core.display import display, HTML
from pymongo import MongoClient
from spacy import displacy
from random import shuffle
import id_beritagar
import datetime
import json



app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))
client = MongoClient("mongodb://localhost:27017")
db = client.iData
dbAdmin = client.iStorage

#datetime Now
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

nlp = id_beritagar.load()

class Database(object):
    def __init__(self):
        self

    def find_data(self, keyword=None, start_date=None, end_date=None, kategori=None, sumber=None):

        if kategori == 'semua_kategori':
            if sumber == 'semua_sumber':
                query = db.test.find({
                    'title': {
                        '$regex': '{}'.format(keyword),
                        '$options': 'i'
                    },
                    'content': {
                        '$regex': '{}'.format(keyword),
                        '$options': 'i'
                    },
                    'publishedAt': {
                        '$gte': '{}'.format(start_date),
                        '$lte': '{}'.format(end_date)
                    }
                })
            else:
                query = db.test.find({
                    'title': {
                        '$regex': '{}'.format(keyword),
                        '$options': 'i'
                    },
                    'content': {
                        '$regex': '{}'.format(keyword),
                        '$options': 'i'
                    },
                    'publishedAt': {
                        '$gte': '{}'.format(start_date),
                        '$lte': '{}'.format(end_date)
                    }
                })
        else:
            if sumber == 'semua_sumber':
                query = db.test.find({
                    'title': {
                        '$regex': '{}'.format(keyword),
                        '$options': 'i'
                    },
                    'content': {
                        '$regex': '{}'.format(keyword),
                        '$options': 'i'
                    },
                    'publishedAt': {
                        '$gte': '{}'.format(start_date),
                        '$lte': '{}'.format(end_date)
                    }
                })
            else:
                query = db.test.find({
                    'title': {
                        '$regex': '{}'.format(keyword),
                        '$options': 'i'
                    },
                    'content': {
                        '$regex': '{}'.format(keyword),
                        '$options': 'i'
                    },
                    'publishedAt': {
                        '$gte': '{}'.format(start_date),
                        '$lte': '{}'.format(end_date)
                    }
                })

        return  query

dbMongo = Database()

@app.route('/')
def main():

    # query = db.test.find({"publishedAt" : "{}-0{}-{}".format(day, month, year)})
    query = db.test.find({"publishedAt" : "02-09-2019"})

    data_now = []
    for q in query:
        data_now.append(q)

    # query top entity
    queryTE = db.topEntity.find({"publishedAt" : "2-9-2019"})
    temp, topEntity = [], []
    for qe in queryTE:
        temp.append(qe)
    for i in range(len(temp)):
        for t in temp[i]['top_ner']:
            topEntity.append(t[0])

    news, bisnis, entertainment, sports, tekno, otomotif, health = [],[],[],[],[],[],[]
    for d in data_now:
        if d['category'] == 'news':
            news.append(d)
        elif d['category'] == 'bisnis':
            bisnis.append(d)
        elif d['category'] == 'entertainment':
            entertainment.append(d)
        elif d['category'] == 'sports':
            sports.append(d)
        elif d['category'] == 'tekno':
            tekno.append(d)
        elif d['category'] == 'otomotif':
            otomotif.append(d)
        elif d['category'] == 'health':
            health.append(d)

    len_liputan, len_kompas, len_tempo = [],[], []
    for d in data_now:
        if d['source'] == 'liputan6.com':
            len_liputan.append(d)
        elif d['source'] == 'kompas.com':
            len_kompas.append(d)
        elif d['source'] == 'tempo.co':
            len_tempo.append(d)

    len_news = len(news)
    len_bisnis = len(bisnis)
    len_entertainment = len(entertainment)
    len_sports = len(sports)
    len_tekno = len(tekno)
    len_otomotif = len(otomotif)
    len_health = len(health)
    len_data = len(data_now)
    len_liputan = len(len_liputan)
    len_kompas = len(len_kompas)
    len_tempo = len(len_tempo)

    shuffle(data_now)

    return render_template('full-header.html',topEntity=topEntity, data=data_now, len_data=len_data, len_news=len_news,
                           len_bisnis=len_bisnis, len_entertainment=len_entertainment,
                           len_sports=len_sports, len_tekno=len_tekno, len_otomotif=len_otomotif, len_health=len_health,
                           len_liputan=len_liputan, len_kompas=len_kompas, len_tempo=len_tempo)

@app.route('/data')
def data():

    len_news = 0
    len_bisnis = 0
    len_entertainment = 0
    len_sports = 0
    len_tekno = 0
    len_otomotif = 0
    len_data = 0
    len_liputan = 0
    len_kompas = 0
    len_tempo = 0

    return  render_template('data.html', len_data=len_data, len_tempo=len_tempo, len_kompas=len_kompas, len_liputan=len_liputan,
                            len_news=len_news, len_bisnis=len_bisnis, len_entertainment=len_entertainment,
                            len_sports=len_sports, len_tekno=len_tekno, len_otomotif=len_otomotif)


@app.route('/findata', methods=['POST', 'GET'])
def findata():

    if request.method == 'POST':
        keyword = request.form['keyword']
        start_date = request.form['start_date']
        start_date_name = datetime.datetime.strptime(start_date, "%d/%b/%Y").strftime("%e %B %Y")
        start_date = datetime.datetime.strptime(start_date, "%d/%b/%Y").strftime("%d-%m-%Y")
        end_date = request.form['end_date']
        end_date_name = datetime.datetime.strptime(end_date, "%d/%b/%Y").strftime("%e %B %Y")
        end_date = datetime.datetime.strptime(end_date, "%d/%b/%Y").strftime("%d-%m-%Y")
        kategori = request.form.get('select_kategori')
        sumber = request.form.get('select_sumber')


        query = dbMongo.find_data(keyword, start_date, end_date, kategori, sumber)

        data_now = []
        for q in query:
            data_now.append(q)

        news, bisnis, entertainment, sports, tekno, otomotif = [], [], [], [], [], []
        for d in data_now:
            if d['category'] == 'news':
                news.append(d)
            elif d['category'] == 'bisnis':
                bisnis.append(d)
            elif d['category'] == 'entertainment':
                entertainment.append(d)
            elif d['category'] == 'sports':
                sports.append(d)
            elif d['category'] == 'tekno':
                tekno.append(d)
            elif d['category'] == 'otomotif':
                otomotif.append(d)

        len_liputan, len_kompas, len_tempo = [], [], []
        for d in data_now:
            if d['source'] == 'liputan6.com':
                len_liputan.append(d)
            elif d['source'] == 'kompas.com':
                len_kompas.append(d)
            elif d['source'] == 'tempo.co':
                len_tempo.append(d)

        len_news = len(news)
        len_bisnis = len(bisnis)
        len_entertainment = len(entertainment)
        len_sports = len(sports)
        len_tekno = len(tekno)
        len_otomotif = len(otomotif)
        len_data = len(data_now)
        len_liputan = len(len_liputan)
        len_kompas = len(len_kompas)
        len_tempo = len(len_tempo)

    else:
        return "error"

    shuffle(data_now)

    return render_template('findata.html', data=data_now, len_data=len_data, len_news=len_news,
                           len_bisnis=len_bisnis, len_entertainment=len_entertainment,
                           len_sports=len_sports, len_tekno=len_tekno, len_otomotif=len_otomotif,
                           len_liputan=len_liputan, len_kompas=len_kompas, len_tempo=len_tempo,
                           start_date=start_date_name, end_date=end_date_name)

@app.route('/admin')
def admin():

    # query = db.test.find({"publishedAt" : "{}-0{}-{}".format(day, month, year)})
    query = dbAdmin.iData.find({})

    data_now = []
    for q in query:
        data_now.append(q)

    news, bisnis, entertainment, sports, tekno, otomotif, health = [],[],[],[],[],[],[]
    for d in data_now:
        if d['category'] == 'news':
            news.append(d)
        elif d['category'] == 'bisnis':
            bisnis.append(d)
        elif d['category'] == 'entertainment':
            entertainment.append(d)
        elif d['category'] == 'sports':
            sports.append(d)
        elif d['category'] == 'tekno':
            tekno.append(d)
        elif d['category'] == 'otomotif':
            otomotif.append(d)
        elif d['category'] == 'health':
            health.append(d)

    len_liputan, len_kompas, len_tempo = [],[], []
    for d in data_now:
        if d['source'] == 'liputan6.com':
            len_liputan.append(d)
        elif d['source'] == 'kompas.com':
            len_kompas.append(d)
        elif d['source'] == 'tempo.co':
            len_tempo.append(d)

    len_news = len(news)
    len_bisnis = len(bisnis)
    len_entertainment = len(entertainment)
    len_sports = len(sports)
    len_tekno = len(tekno)
    len_otomotif = len(otomotif)
    len_health = len(health)
    len_data = len(data_now)
    len_liputan = len(len_liputan)
    len_kompas = len(len_kompas)
    len_tempo = len(len_tempo)

    shuffle(data_now)

    return render_template('admin.html', data=data_now, len_data=len_data, len_news=len_news,
                           len_bisnis=len_bisnis, len_entertainment=len_entertainment,
                           len_sports=len_sports, len_tekno=len_tekno, len_otomotif=len_otomotif, len_health=len_health,
                           len_liputan=len_liputan, len_kompas=len_kompas, len_tempo=len_tempo)


@app.route('/test', methods=['POST', 'GET'])
def test():
    # query = db.test2.find({})
    #
    # data_now = []
    # for q in query:
    #     data_now.append(q)

    # if request.method == 'POST':
    #     nama = request.form['keyword']
    #     start_date = request.form['start_date']
    #     start_date = datetime.datetime.strptime(start_date, "%d/%b/%Y").strftime("%d-%m-%Y")
    #     end_date = request.form['end_date']
    #     end_date = datetime.datetime.strptime(end_date, "%d/%b/%Y").strftime("%d-%m-%Y")
    #     kategori = request.form.get('select_kategori')

    # else:
    #     return "error"
    kategori = 'test'

    # query top entity
    query = db.topEntity.find({"publishedAt" : "2-9-2019"})
    temp, topEntity = [], []
    for qe in query:
        temp.append(qe)
    for i in range(len(temp)):
        for t in temp[i]['top_ner']:
            topEntity.append(t[0])

    asd = len(topEntity)

    return render_template('test.html', kategori=kategori, topEntity=topEntity, asd=asd)

if __name__ == '__main__':
    app.run(debug=True)