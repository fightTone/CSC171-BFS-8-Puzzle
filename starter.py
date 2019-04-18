import os
import numpy as np
import driver as d
from flask import Flask, render_template,redirect
import random

app =Flask(__name__)



@app.route('/')
def index():
    inputs = d.initial_state
    init = str(d.initial_state).replace('[','').replace(']','')
    d.bfs(inputs)
    moves = d.backtrace()
    return render_template("index.html",initial=init,moves=moves)


@app.route('/shuffle', methods=['GET'])
def shuffler():
    d.initial_state = d.initial()
    return redirect('/')
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,debug=True)