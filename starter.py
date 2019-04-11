import os
import numpy as np
from driver import *
from flask import Flask, render_template

app =Flask(__name__)

@app.route('/')
def index():
    inputs = initial()
    os.system('python driver.py bfs '+inputs)
    file = open('output.txt', 'r')
    moves = np.array(file.read())
    
    return render_template("index.html",initial=inputs,moves=moves)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,debug=True)