from flask import Flask,render_template, request, get_flashed_messages, flash, redirect, url_for, flash
from model import model_graph
from kpi import kpi_graph
from alert import click, message
from audit import gmes




app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.form.get('action1') == 'Service & Sales Status Report':
        kpi_graph()
        return render_template('kpi.html')
    elif request.form.get('action2') == 'New Model Service Report':
        model_graph()
        return render_template('model.html')
    elif request.form.get('action3') == 'Line Audit Result':
        gmes()
        return render_template('audit.html')
    return render_template('index.html')
