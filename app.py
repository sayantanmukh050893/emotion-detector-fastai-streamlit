from __future__ import division
import cv2
import streamlit as st
from PIL import Image
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.models import model_from_json
import os
import numpy as np
import fastbook
from fastbook import *
from fastai.vision.widgets import *

# #loading the model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("weights.h5")

# loading fastai model
#path = Path()
#path.ls(file_exts='.pkl')
#print(os.getcwd())
filenames = next(os.walk(os.getcwd()), (None, None, []))[2]
print(filenames)
model_file_path = os.path.join(os.getcwd(),'model.pkl')
print(model_file_path)
model_inf = load_learner(model_file_path)

WIDTH = 48
HEIGHT = 48
x=None
y=None
#labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
labels = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']


st.set_page_config(layout="wide")
if "clicked" not in st.session_state:
    st.session_state["clicked"] = False

def onSearch():
    st.session_state["clicked"] = True

c = st.container()
st.title("Webcam Live Feed")

col1, col2 = st.columns(2)

with col1:
    image = Image.open('human_sentiments.jpg')
    st.image(image)
    run = st.checkbox('Enable Webcam')
    #st.button("Click to open Webcam", on_click= onSearch(),args= [])

with col2: 
    #run = st.checkbox('Enable Webcam')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
    #while st.session_state["clicked"]:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(128, 128)
        # ,
        # flags=cv2.CV_HAAR_SCALE_IMAGE
    )
        for (x, y, w, h) in faces:
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            #cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            #cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
            #cv2.rectangle(frame, (x, y), (x + w+2, y + h+2), (0, 255, 0), 2)
            cropped_img_pil = Image.fromarray(roi_gray)
            pred,pred_idx,probs = model_inf.predict(cropped_img_pil)
            cv2.putText(frame, pred, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            #yhat= loaded_model.predict(cropped_img)
            #cv2.putText(frame, labels[int(np.argmax(yhat))], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow('Video', frame)
        FRAME_WINDOW.image(frame)
    else:
        st.write('')