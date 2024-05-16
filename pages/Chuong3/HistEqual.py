import streamlit as st
import numpy as np
from PIL import Image
import cv2

def HistEqual(imgin):
    L = 256
    M, N = imgin.shape[:2]
    imgout = np.zeros((M, N), np.uint8)
    h = np.zeros(L, np.int32)
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            h[r] += 1
    p = h / (M * N)
    s = np.zeros(L, np.float64)
    for k in range(L):
        for j in range(k + 1):
            s[k] += p[j]
    s = (L - 1) * s
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            imgout[x, y] = np.uint8(s[r])
    return imgout

def app():
    st.title('Ứng dụng Cân bằng Histogram ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Cân bằng Histogram'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = HistEqual(frame)
            result_image = cv2.resize(result_image, (frame.shape[1], frame.shape[0]))
            st.image(result_image, caption='Kết quả sau khi cân bằng Histogram', use_column_width=True)