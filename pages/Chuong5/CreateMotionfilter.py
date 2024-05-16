import streamlit as st
import numpy as np
from PIL import Image
import cv2
L = 256

def CreateMotionNoise(imgin, a=0.1, b=0.1, T=1):
    M, N = imgin.shape
    f = imgin.astype(float)  
    F = np.fft.fft2(f)
    F = np.fft.fftshift(F)
    H = CreateMotionfilter(M, N, a, b, T)
    G = F*H
    G = np.fft.ifftshift(G)
    g = np.fft.ifft2(G)
    g = g.real
    g = np.clip(g, 0, L-1)
    g = g.astype(np.uint8)
    return g

def CreateMotionfilter(M, N, a, b, T):
    H = np.zeros((M,N), complex)  
    for u in range(0, M):
        for v in range(0, N):
            phi = np.pi*((u-M//2)*a + (v-N//2)*b)
            if np.abs(phi) < 1.0e-6:
                RE = T*np.cos(phi)
                IM = -T*np.sin(phi)
            else:
                RE = T*np.sin(phi)/phi*np.cos(phi)
                IM = -T*np.sin(phi)/phi*np.sin(phi)
            H.real[u,v] = RE
            H.imag[u,v] = IM
    return H

def app():
    st.title('Ứng dụng Tạo Nhiễu Chuyển Động')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image.convert('L'))  

        a = st.slider('Chọn hệ số a', 0.0, 1.0, 0.1)
        b = st.slider('Chọn hệ số b', 0.0, 1.0, 0.1)
        T = st.slider('Chọn thời gian phơi sáng T', 0.1, 10.0, 1.0)

        if st.button('Áp dụng Nhiễu Chuyển Động'):
            noisy_image = CreateMotionNoise(frame, a, b, T)
            st.image(noisy_image, caption='Kết quả sau khi áp dụng Nhiễu Chuyển Động', use_column_width=True)
