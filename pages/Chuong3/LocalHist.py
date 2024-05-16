import streamlit as st
import numpy as np
from PIL import Image
import cv2

def LocalHist(imgin, kernel_size=3):
    M, N = imgin.shape[:2]
    imgout = np.zeros_like(imgin)
    border = kernel_size // 2

    padded_img = cv2.copyMakeBorder(imgin, border, border, border, border, cv2.BORDER_REFLECT)

    for x in range(border, M + border):
        for y in range(border, N + border):
            local_region = padded_img[x - border:x + border + 1, y - border:y + border + 1]
            equalized_region = cv2.equalizeHist(local_region)
            imgout[x - border, y - border] = equalized_region[border, border]
    return imgout

def app():
    st.title('Ứng dụng Local Histogram ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Áp dụng Local Histogram'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = LocalHist(frame)
            result_image = cv2.resize(result_image, (frame.shape[1], frame.shape[0]))
            st.image(result_image, caption='Kết quả sau khi áp dụng Local Histogram', use_column_width=True)