from flask import Flask, jsonify, render_template, request
import os
app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    print request.args
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print a + b
    return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5001'))
    app.run('0.0.0.0', port=port)
