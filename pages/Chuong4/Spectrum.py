import streamlit as st
import numpy as np
from PIL import Image
import cv2

def Spectrum(imgin):
    L = 256
    M, N = imgin.shape
    P = cv2.getOptimalDFTSize(M)
    Q = cv2.getOptimalDFTSize(N)
    
    fp = np.zeros((P, Q), np.float32)
    fp[:M, :N] = imgin
    fp = fp / (L - 1)

    for x in range(M):
        for y in range(N):
            if (x + y) % 2 == 1:
                fp[x, y] = -fp[x, y]

    F = cv2.dft(fp, flags=cv2.DFT_COMPLEX_OUTPUT)

    S = np.sqrt(F[:, :, 0]**2 + F[:, :, 1]**2)
    S = np.clip(S, 0, L - 1)
    S = S.astype(np.uint8)
    return S

def app():
    st.title('Ứng dụng Phổ Fourier của ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Tính Phổ Fourier'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            spectrum_image = Spectrum(frame)
            st.image(spectrum_image, caption='Phổ Fourier của ảnh', use_column_width=True)