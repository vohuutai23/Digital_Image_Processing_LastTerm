import streamlit as st
import numpy as np
from PIL import Image
import cv2

def FrequencyFilter(imgin):
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    
    fp = np.zeros((P, Q), np.float32)
    fp[:M, :N] = imgin

    for x in range(M):
        for y in range(N):
            if (x + y) % 2 == 1:
                fp[x, y] = -fp[x, y]

    F = cv2.dft(fp, flags=cv2.DFT_COMPLEX_OUTPUT)

    H = np.zeros((P, Q), np.float32)
    D0 = 60
    n = 2
    for u in range(P):
        for v in range(Q):
            Duv = np.sqrt((u - P // 2)**2 + (v - Q // 2)**2)
            if Duv > 0:
                H[u, v] = 1.0 / (1.0 + np.power(D0 / Duv, 2 * n))

    G = F.copy()
    for u in range(P):
        for v in range(Q):
            G[u, v, 0] = F[u, v, 0] * H[u, v]
            G[u, v, 1] = F[u, v, 1] * H[u, v]

    g = cv2.idft(G, flags=cv2.DFT_SCALE)
    gp = g[:, :, 0]

    for x in range(P):
        for y in range(Q):
            if (x + y) % 2 == 1:
                gp[x, y] = -gp[x, y]

    imgout = gp[0:M, 0:N]
    imgout = np.clip(imgout, 0, 255)
    imgout = imgout.astype(np.uint8)
    return imgout

def app():
    st.title('Ứng dụng Lọc High Pass trong miền tần số')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Áp dụng Lọc High Pass'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            filtered_image = FrequencyFilter(frame)
            st.image(filtered_image, caption='Kết quả sau khi áp dụng Lọc High Pass', use_column_width=True)