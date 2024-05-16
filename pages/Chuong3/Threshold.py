import streamlit as st
import numpy as np
from PIL import Image
import cv2

def Threshold(imgin):
    temp = cv2.blur(imgin, (15, 15))
    retval, imgout = cv2.threshold(temp, 64, 255, cv2.THRESH_BINARY)
    return imgout

def app():
    st.title('Ứng dụng Phân ngưỡng ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Áp dụng Phân ngưỡng'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = Threshold(frame)
            st.image(result_image, caption='Kết quả sau khi áp dụng Phân ngưỡng', use_column_width=True)