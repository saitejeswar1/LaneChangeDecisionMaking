import importlib
from flask_app_3.dynamicQuery import dq
import os
from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
import xlsxwriter
from werkzeug.utils import secure_filename
import numpy as np
import cv2
from scipy.misc import imresize
import pandas as pd
from keras.models import load_model
import shutil
from pixellib.instance import instance_segmentation
from flask_app_3.write2KB import write_to_ttl
import pathlib
from flask_app_3.training_nn import train_LC




app = Flask(__name__)

UPLOAD_FOLDER = r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///image.db"
db = SQLAlchemy(app)

class IMAGES(db.Model):
    ID = db.Column(db.Integer,primary_key=True)
    IMG = db.Column(db.Text,nullable=False)
    MSG = db.Column(db.Text,nullable=False)
    RESP = db.Column(db.Integer,nullable=True)


@app.route('/',methods = ["GET","POST"])
def index():
    return render_template("base.html")  

@app.route('/nn_train',methods=['GET','POST'])
def simpletrain():
    train_LC()
    return redirect('/home')  

@app.route('/home',methods = ["GET","POST"])
def go_home():
    return render_template('index.html')


@app.route("/upload",methods=["POST"])
def upload():
    pic = request.files["pic"]
    if not pic:
        return "No file uploaded"
    filename = secure_filename(pic.filename)
    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        

    class Lanes():
        def __init__(self):
            self.recent_fit = []
            self.avg_fit = []

    def road_lines(image):
        """ Takes in a road image, re-sizes for the model,
        predicts the lane to be drawn from the model in G color,
        recreates an RGB image of a lane and merges with the
        original road image.
        """

        # Get image ready for feeding into model
        small_img = imresize(image, (80, 160, 3))
        small_img = np.array(small_img)
        small_img = small_img[None,:,:,:]

        # Make prediction with neural network (un-normalize value by multiplying by 255)
        prediction = model.predict(small_img)[0] * 255

        
        # Add lane prediction to list for averaging
        lanes.recent_fit.append(prediction)
        # Only using last five for average
        if len(lanes.recent_fit) > 5:
            lanes.recent_fit = lanes.recent_fit[1:]

        # Calculate average detection
        lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis = 0)

        # Generate fake R & B color dimensions, stack with G
        blanks = np.ones_like(lanes.avg_fit).astype(np.uint8)
        lane_drawn = np.dstack((blanks, lanes.avg_fit, blanks))

        # Re-size to match the original image
        lane_image = imresize(lane_drawn, (image.shape[0], image.shape[1], 3))

        # Merge the lane drawing onto the original image
        result = cv2.addWeighted(image, 1, lane_image, 1, 0)

        return result

    
    # Load Keras model
    model = load_model(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\Lanes_CNN_model.h5')
    # Create lanes object
    lanes = Lanes()
    
    vidObj = cv2.VideoCapture(fr'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\UPLOAD_FOLDER\{filename}')
    
    if os.path.exists(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Input_Frames\{filename[:-4]}"):
        shutil.rmtree(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Input_Frames\{filename[:-4]}")

    if os.path.exists(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\lanes_frames\{filename[:-4]}"):
        shutil.rmtree(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\lanes_frames\{filename[:-4]}")
    
    if os.path.exists(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Output_Frames\{filename[:-4]}"):
        shutil.rmtree(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Output_Frames\{filename[:-4]}")

    success = 1
    count = 0
    os.mkdir(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Input_Frames\{filename[:-4]}")
    os.mkdir(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\lanes_frames\{filename[:-4]}")
    os.mkdir(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Output_Frames\{filename[:-4]}")
    seg = instance_segmentation()
    seg.load_model(r"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\mask_rcnn_coco.h5")
    target_classes = seg.select_target_classes(car=True,truck=True)
    row,col = 0,0
    
    inArgs = "seg_vals,count" #take input from ...
    outArgs = "msg"

    [module,func_name] = dq(inArgs,outArgs)
    module = 'flask_app_3.' + module
    mod = importlib.import_module(module)           #final_result
    inputs = np.empty((0,10),dtype=int)
    outputs = np.empty((0,1),dtype=int)
    while success:
            success, image = vidObj.read()
            if count%500 == 0:
                cv2.imwrite(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Input_Frames\{filename[:-4]}\frames{count}.jpg",image)
                cv2.imwrite(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\lanes_frames\{filename[:-4]}\frames{count}.jpg",road_lines(image))
                seg_vals = seg.segmentImage(fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Input_Frames\{filename[:-4]}\frames{count}.jpg", segment_target_classes= target_classes, show_bboxes=True,  output_image_name=fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Output_Frames\{filename[:-4]}\frames{count}.jpg")
                
                ip,msg,index = getattr(mod,func_name)(seg_vals,count,filename)
                
                inputs = np.append(inputs,np.array([ip]),axis = 0)
                outputs = np.append(outputs,np.array([[index]]),axis = 0)
                
                

                img = IMAGES(IMG = fr"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Input_Frames\{filename[:-4]}\frames{count}.jpg",MSG = msg)
                
                db.session.add(img)
            count = count + 1
    
    workbook = xlsxwriter.Workbook(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\log_file.xlsx')
    
    worksheet = workbook.add_worksheet("My sheet2")

    for i,j in zip(inputs,outputs):
        col = 0
        for k in i:
          worksheet.write(row, col, k)
          col += 1  
        worksheet.write(row, col+1, j) 
        row += 1
    workbook.close()
    db.session.commit()
    return redirect("/1")

@app.route("/<int:id>",methods=["GET","POST"])
def get_img(id):
    
    if request.method == "POST":
        form_data = request.form
        img = IMAGES.query.filter_by(ID = id - 1).first()
        print(form_data)
        if form_data["gridRadios1"] == 'option1':
            img.RESP = 1
            print('response written')
        else:
            img.RESP = 0
            print('response written')
        db.session.commit()
        img = IMAGES.query.filter_by(ID = id).first()
        if not img:
            return redirect("/excel")
        message = img.MSG 
        path = pathlib.PureWindowsPath(img.IMG)
        path = path.as_posix()
        path = path.partition('flask_app_3')[2]
        return render_template("results.html",out_path = message,path=path,id=id)

    else:
        img = IMAGES.query.filter_by(ID = id).first()
        print("in get")
        if not img:

            redirect("/excel")

        message = img.MSG

        path = pathlib.PureWindowsPath(img.IMG)

        path = path.as_posix()

        path = path.partition('flask_app_3')[2]

        return render_template("results.html",out_path = message,path=path,id=id)

@app.route("/excel",methods=["get"])
def write2excel():
    data = IMAGES.query.all()
    df = pd.read_excel (r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\log_file.xlsx', sheet_name='My sheet2',usecols="A:J")
    d = pd.read_excel (r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\log_file.xlsx', sheet_name='My sheet2',usecols="L")
    inputs = df.to_numpy()
    outputs = d.to_numpy()
    inputs = [[1,0,1,1,0,1,1,0,0,1]]
    outputs = [[1]]
    workbook = xlsxwriter.Workbook(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\log_file.xlsx')
    
    worksheet = workbook.add_worksheet("My sheet2")
    row = 1
    
    for i,j in zip(inputs,outputs):
        col = 0
        
        for k in i:
          worksheet.write(row, col, k)
          col += 1 
          
        worksheet.write(row, col+1, j[0])
        worksheet.write(row,col+3,data[row].RESP) 
        row += 1
    workbook.close()
    return redirect('/2kb')

@app.route("/2kb",methods=["GET","POST"])
def w2kb():
    write_to_ttl()
    return redirect('/')



    

if __name__ == "__main__":
    app.run(debug=True)
