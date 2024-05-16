import streamlit as st
import numpy as np
from PIL import Image
import cv2

def HistEqualColor(imgin):
    B, G, R = cv2.split(imgin)
    B_eq = cv2.equalizeHist(B)
    G_eq = cv2.equalizeHist(G)
    R_eq = cv2.equalizeHist(R)
    imgout = cv2.merge((B_eq, G_eq, R_eq))
    return imgout

def app():
    st.title('Ứng dụng Cân bằng Histogram cho ảnh màu')

    st.markdown('**Vui lòng tải lên hình ảnh màu:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Cân bằng Histogram cho ảnh màu'):
            result_image = HistEqualColor(frame)
            result_image = cv2.resize(result_image, (frame.shape[1], frame.shape[0]))
            st.image(result_image, caption='Kết quả sau khi cân bằng Histogram cho ảnh màu', use_column_width=True)
