from flask import Flask
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
bs = Bootstrap5(app)
from views import *

if __name__ == '__main__':
    app.run(debug=True)
     
    