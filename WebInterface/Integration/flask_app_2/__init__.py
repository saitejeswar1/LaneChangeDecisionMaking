from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON,Sequence
import json
import numpy as np
from tensorflow import keras
from werkzeug.utils import redirect


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lane_change.db"
db = SQLAlchemy(app)

class lanechange(db.Model):
    __tablename__ = "Weights database"
    id = db.Column(db.Integer, Sequence("item_id_seq"), primary_key = True, nullable = False)
    weights = db.Column(JSON, nullable = True)

    def __repr__(self):
        return "Weight added" + str(self.id)
    

@app.route('/', methods = ['GET'])
def index():
    return render_template('base.html')  

@app.route('/results', methods = ['GET','POST'])
def result():
    if request.method == "POST":
        
        form_data = request.form
        ip = []
        
        for value in form_data.values():
            ip.append(int(value))
        print(ip)
        model = keras.models.load_model(r"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_2\weights_matrix_updated.h5")
        y_predict = model.predict([[ip]])
        y_predict = np.round(y_predict,0)
        op = y_predict[0]
        message = ["Steer Right","Do not Steer","Steer Left"]
        
        for i in range(len(op)):
            if op[i] == 1 :
              return render_template('results.html',output=message[i],input=ip)  

    else:
        redirect('/')


if __name__ == "__main__":
    app.run(debug=True)