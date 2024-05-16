import streamlit as st
import numpy as np
from PIL import Image
import cv2

def BoxFilter(imgin, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
    imgout = cv2.filter2D(imgin, -1, kernel)
    return imgout

def app():
    st.title('Ứng dụng Lọc Box ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Áp dụng Lọc Box'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                B, G, R = cv2.split(frame)
                B_filtered = BoxFilter(B)
                G_filtered = BoxFilter(G)
                R_filtered = BoxFilter(R)
                frame_filtered = cv2.merge((B_filtered, G_filtered, R_filtered))
                frame_filtered = cv2.cvtColor(frame_filtered, cv2.COLOR_BGR2RGB)
            else:
                frame_filtered = BoxFilter(frame)
            st.image(frame_filtered, caption='Kết quả sau khi áp dụng Lọc Box', use_column_width=True)