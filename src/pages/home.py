import streamlit as st
from PIL import Image
import os

def write():

    with st.spinner("Loding..."):

        image_logo = Image.open(os.path.abspath("images/logo_ufrpe.jpg"))
        image_bsi = Image.open(os.path.abspath("images/bsi.jpg"))

        st.image(image_logo, caption='UFRPE', width=200)
        st.image(image_bsi, caption='UFRPE', width=200)

        st.write(
            """
            # Despesas Orçamentárias - Home
            """
        )

        