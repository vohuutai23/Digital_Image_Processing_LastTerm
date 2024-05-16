import streamlit as st
import numpy as np
from PIL import Image
import cv2

def Histogram(imgin):
    L = 256
    M, N = imgin.shape[:2]
    h = np.zeros(L, np.int32)
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            h[r] += 1
    p = h / (M * N)
    scale = M / np.max(p)  
    imgout = np.zeros((M, N), np.uint8) + 255
    for r in range(L):
        cv2.line(imgout, (r, M - 1), (r, M - 1 - int(scale * p[r])), (0, 0, 0))
    return imgout

def app():
    st.title('Ứng dụng Histogram ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Tính Histogram'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = Histogram(frame)
            result_image = cv2.resize(result_image, (frame.shape[1], frame.shape[0]))
            st.image(result_image, caption='Histogram của ảnh', use_column_width=True)