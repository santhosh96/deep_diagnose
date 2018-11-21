import os, time, datetime
from flask import Flask, render_template, request
import sys
import argparse
import numpy as np
import pandas as pd
import PIL.Image
import requests
from io import BytesIO
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pygal as pg
import tensorflow as tf

from keras.preprocessing import image
from keras.models import load_model
from keras.applications.inception_v3 import preprocess_input

app = Flask(__name__)
model = load_model("./models/17032018inception")
graph = tf.get_default_graph()

@app.route("/", methods=['GET'])
def server():
    return render_template('index.html')

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/home", methods=['GET'])
def ret():
    return render_template('index.html')

def predict(crop_img):
    x = image.img_to_array(crop_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    with graph.as_default():
        preds = model.predict(x)
    return preds[0]

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    name, ext = file.filename.split(".")
    name_r = name
    date, Time = time.strftime("%x %X", time.localtime()).split(" ")
    date = date.replace("/","-")
    name = name + "_" + date + "_" + Time
    file.filename = name + "." + ext
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)

    """Here on code for prediction is entered """

    path = "uploads" + "/" + file.filename
    img = image.load_img(path)

    half_the_width = img.size[0] / 2
    half_the_height = img.size[1] / 2
    cropped_image = img.crop(
        (
            half_the_width - 900,
            half_the_height - 900,
            half_the_width + 1000,
            half_the_height + 1000
        )
    )
    crop_img = cropped_image.resize((299,299))

    prediction = predict(crop_img)
    if prediction[0] > 0.5:
        pred_class = 'negative'
    if prediction[1] > 0.5:
        pred_class = 'positive'

    """Code for exporting data"""

    df = pd.read_excel('./data/stats.xlsx')
    df.loc[len(df.index)] = [name_r, date, Time, pred_class]
    df.to_excel('./data/stats.xlsx')

    if pred_class == 'positive':
        return render_template('Report.html', name=name_r, date=date, time=Time, result='Positive')

    else:
        return render_template('Report_neg.html', name=name_r, date=date, time=Time, result='Negative')

# @app.route('/plots')
@app.route("/table", methods=['GET'])
def plottings():

    df = pd.read_csv("./data/week.csv")
    df_m = pd.read_csv("./data/month.csv")
    df_y = pd.read_csv("./data/year.csv")

    df.index = df['timestamp']
    df.drop('timestamp', inplace=True, axis=1)

    df_m.index = df_m['timestamp']
    df_m.drop('timestamp', inplace=True, axis=1)

    df_y.index = df_y['timestamp']
    df_y.drop('timestamp', inplace=True, axis=1)

    bar_chart = pg.Bar()
    bar_chart.title = 'Past 6 weeks cases trend'
    bar_chart.x_labels = list(df.index.get_values()[-6:])
    bar_chart.add('Positive', list(df['positive'][-6:]))
    bar_chart.add('Negative', list(df['negative'][-6:]))

    pie_chart = pg.Pie()
    p = df['positive'][44:54].sum()
    n = df['negative'][44:54].sum()
    pie_chart.title = 'Past 6 weeks cases trend aggregated'
    pie_chart.add('Positive', p)
    pie_chart.add('Negative', n)

    bar_chart_m = pg.Bar()
    bar_chart_m.title = 'Past 6 months cases trend'
    bar_chart_m.x_labels = list(df_m.index.get_values()[-6:])
    bar_chart_m.add('Positive', list(df_m['positive'][-6:]))
    bar_chart_m.add('Negative', list(df_m['negative'][-6:]))

    pie_chart_m = pg.Pie()
    p_m = df['positive'][-6:].sum()
    n_m = df['negative'][-6:].sum()
    pie_chart_m.title = 'Past 6 months cases trend aggregated'
    pie_chart_m.add('Positive', p_m)
    pie_chart_m.add('Negative', n_m)

    bar_chart_y = pg.Bar()
    bar_chart_y.title = 'Past 6 months cases trend'
    bar_chart_y.x_labels = list(df_y.index.get_values())
    bar_chart_y.add('Positive', list(df_y['positive']))
    bar_chart_y.add('Negative', list(df_y['negative']))

    pie_chart_y = pg.Pie()
    p_y = df_y['positive'].sum()
    n_y = df_y['negative'].sum()
    pie_chart_y.title = 'Past year cases trend aggregated'
    pie_chart_y.add('Positive', p_y)
    pie_chart_y.add('Negative', n_y)

    graph_data_week_bar = bar_chart.render_data_uri()
    graph_data_week_pie = pie_chart.render_data_uri()
    graph_data_month_bar = bar_chart_m.render_data_uri()
    graph_data_month_pie = pie_chart_m.render_data_uri()
    graph_data_year_bar = bar_chart_y.render_data_uri()
    graph_data_year_pie = pie_chart_y.render_data_uri()

    return render_template('pie_chart.html', foo=graph_data_week_bar, bar=graph_data_week_pie, alpha=graph_data_month_bar, gamma=graph_data_month_pie, beta=graph_data_year_bar, theta=graph_data_year_pie)

if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
