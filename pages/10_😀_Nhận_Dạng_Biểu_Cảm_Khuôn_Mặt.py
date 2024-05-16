import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
from keras.models import model_from_json
import numpy as np

json_file = open("model/facialemotionmodel.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("model/facialemotionmodel.h5")

haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

labels = {
    0: 'tuc gian',
    1: 'ghe tom',
    2: 'so hai',
    3: 'hanh phuc',
    4: 'binh thuong',
    5: 'buon',
    6: 'ngac nhien'
}


def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

class EmotionVideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            resized_img = cv2.resize(face_img, (48, 48))
            img_pixels = extract_features(resized_img)
            predictions = model.predict(img_pixels)
            max_index = np.argmax(predictions[0])
            predicted_emotion = labels[max_index]
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, predicted_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return img

st.title('Ứng dụng nhận diện biểu cảm khuôn mặt qua camera')
st.sidebar.title("Nhóm sinh viên thực hiện:")
st.sidebar.write("""
                - 1. **Hành Phúc Công - 21110817**
                - 2. **Võ Hữu Tài - 21110294**
                """)

webrtc_streamer(key="emotion-recognition", video_transformer_factory=EmotionVideoTransformer)
