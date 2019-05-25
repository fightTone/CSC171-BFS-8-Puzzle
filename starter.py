import os
import numpy as np
import driver as d
from flask import Flask, render_template,redirect
import random
import time

app =Flask(__name__)

def bfs(inputs):
    print inputs
    d.bfs(inputs)
    moves = d.backtrace()
    return moves

def ast(inputs):
	print inputs
	d.bfs(inputs)
	moves = d.backtrace()
	return moves

@app.route('/')
def index():
    inputs = d.initial_state
    init = str(d.initial_state).replace('[','').replace(']','')

    startBFS = time.time()
    moves = bfs(inputs)
    endBFS = time.time()
    bfsRun = endBFS - startBFS

    startAST = time.time()
    movesAST = ast(inputs)
    endAST = time.time()
    astRun = endAST - startAST

    return render_template("index.html",initial=init,moves=moves, bfsRun=bfsRun, astRun=astRun, movesAST=movesAST)


@app.route('/shuffle', methods=['GET'])
def shuffler():
    d.initial_state = d.initial()
    return redirect('/')
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,debug=True)