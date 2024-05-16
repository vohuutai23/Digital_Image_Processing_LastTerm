import streamlit as st
import cv2 as cv
import numpy as np
import joblib
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title('Ứng dụng nhận diện khuôn mặt qua camera')
st.sidebar.title("Nhóm sinh viên thực hiện:")
st.sidebar.write("""
                - 1. **Hành Phúc Công - 21110817**
                - 2. **Võ Hữu Tài - 21110294**
                """)

def str2bool(v):
    return v.lower() in ('yes', 'true', 't', '1')

def load_model(model_path):
    return joblib.load(model_path)

face_detection_model = 'model/face_detection_yunet_2023mar.onnx'
face_recognition_model = 'model/face_recognition_sface_2021dec.onnx'
svc = load_model('model/svc.pkl')
mydict = ['An', 'Cong', 'Khoa', 'Tai', 'Trung']


color_map = {
    'An': (0, 255, 0),  
    'Cong': (0, 0, 255),  
    'Khoa': (255, 0, 255),   
    'Tai': (255, 255, 0), 
    'Trung': (0, 0, 0),
    'Unknown': (128, 0, 128)       
}

detector = cv.FaceDetectorYN.create(face_detection_model, "", (320, 320), 0.9, 0.3, 5000)
recognizer = cv.FaceRecognizerSF.create(face_recognition_model, "")

class RecognizedVideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        h, w, _ = img.shape
        img_resized = cv.resize(img, (320, 320))

        faces = detector.detect(img_resized)
        if faces[1] is not None:
            scale_factor_w = w / 320
            scale_factor_h = h / 320

            for i, face in enumerate(faces[1][:6]):
                face_align = recognizer.alignCrop(img_resized, face)
                face_feature = recognizer.feature(face_align)
                test_predict = svc.predict(face_feature)
                result = mydict[test_predict[0]]

                coords = face[:-1]
                coords[0] *= scale_factor_w
                coords[1] *= scale_factor_h
                coords[2] *= scale_factor_w
                coords[3] *= scale_factor_h
                color = color_map.get(result, color_map['Unknown']) 
                cv.rectangle(img, (int(coords[0]), int(coords[1])), (int(coords[0]+coords[2]), int(coords[1]+coords[3])), color, 2)
                cv.putText(img, result, (int(coords[0]), int(coords[1]) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        return img



webrtc_streamer(key="face-recognition", video_transformer_factory=RecognizedVideoTransformer)
