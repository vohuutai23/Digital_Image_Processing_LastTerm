import streamlit as st
import numpy as np
from PIL import Image
import cv2

st.title('Nhận dạng trái cây')
st.sidebar.title("Nhóm sinh viên thực hiện:")
st.sidebar.write("""
                - 1. **Hành Phúc Công - 21110817**
                - 2. **Võ Hữu Tài - 21110294**
                """)

try:
    if st.session_state["LoadModel"]:
        st.write('Mô hình đã được tải.')
except KeyError:
    st.session_state["LoadModel"] = True
    st.session_state["Net"] = cv2.dnn.readNet("model/yolov8n_trai_cay.onnx")

filename_classes = 'model/object_detection_trai_cay_yolo.txt'
mywidth = 640
myheight = 640
postprocessing = 'yolov8'
background_label_id = -1
backend = 0
target = 0

classes = None
if filename_classes:
    with open(filename_classes, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

st.session_state["Net"].setPreferableBackend(0)
st.session_state["Net"].setPreferableTarget(0)
outNames = st.session_state["Net"].getUnconnectedOutLayersNames()

confThreshold = 0.5
nmsThreshold = 0.4
scale = 0.00392
mean = [0, 0, 0]

def drawPred(classId, conf, left, top, right, bottom, frame):
    box_thickness = 3
    font_scale = 0.75
    font_thickness = 2
    color = (0, 255, 0)  
    label = '%.2f' % conf
    if classes:
        assert(classId < len(classes))
        label = '%s: %s' % (classes[classId], label)

    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    top = max(top, labelSize[1])
    cv2.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness=font_thickness)

def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    def drawPred(classId, conf, left, top, right, bottom):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0))

        label = '%.2f' % conf

        if classes:
            assert(classId < len(classes))
            label = '%s: %s' % (classes[classId], label)

        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv2.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    layerNames = st.session_state["Net"].getLayerNames()
    lastLayerId = st.session_state["Net"].getLayerId(layerNames[-1])
    lastLayer = st.session_state["Net"].getLayer(lastLayerId)

    classIds = []
    confidences = []
    boxes = []
    if lastLayer.type == 'Region' or postprocessing == 'yolov8':

        if postprocessing == 'yolov8':
            box_scale_w = frameWidth / mywidth
            box_scale_h = frameHeight / myheight
        else:
            box_scale_w = frameWidth
            box_scale_h = frameHeight

        for out in outs:
            if postprocessing == 'yolov8':
                out = out[0].transpose(1, 0)

            for detection in out:
                scores = detection[4:]
                if background_label_id >= 0:
                    scores = np.delete(scores, background_label_id)
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThreshold:
                    center_x = int(detection[0] * box_scale_w)
                    center_y = int(detection[1] * box_scale_h)
                    width = int(detection[2] * box_scale_w)
                    height = int(detection[3] * box_scale_h)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
    else:
        print('Unknown output layer type: ' + lastLayer.type)
        exit()

    if len(outNames) > 1 or (lastLayer.type == 'Region' or postprocessing == 'yolov8') and 0 != cv2.dnn.DNN_BACKEND_OPENCV:
        indices = []
        classIds = np.array(classIds)
        boxes = np.array(boxes)
        confidences = np.array(confidences)
        unique_classes = set(classIds)
        for cl in unique_classes:
            class_indices = np.where(classIds == cl)[0]
            conf = confidences[class_indices]
            box  = boxes[class_indices].tolist()
            nms_indices = cv2.dnn.NMSBoxes(box, conf, confThreshold, nmsThreshold)
            indices.extend(class_indices[nms_indices])
    else:
        indices = np.arange(0, len(classIds))

    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
    return

st.markdown('**Vui lòng tải lên hình ảnh trái cây:**')
img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    frame = np.array(image)  
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

    if st.button('Nhận dạng'):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        inpWidth = mywidth if mywidth else frameWidth
        inpHeight = myheight if myheight else frameHeight
        blob = cv2.dnn.blobFromImage(frame, size=(inpWidth, inpHeight), swapRB=True, ddepth=cv2.CV_8U)

        st.session_state["Net"].setInput(blob, scalefactor=scale, mean=mean)
        if st.session_state["Net"].getLayer(0).outputNameToIndex('im_info') != -1:  
            frame = cv2.resize(frame, (inpWidth, inpHeight))
            st.session_state["Net"].setInput(np.array([[inpHeight, inpWidth, 1.6]], dtype=np.float32), 'im_info')

        outs = st.session_state["Net"].forward(outNames)
        postprocess(frame, outs)

        color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(color_coverted)
        st.image(pil_image)

st.markdown("""
    <style>
    .stFileUploader {
        border: 2px solid #f63366;
        border-radius: 5px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        color: white;
        background-color: #f63366;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
