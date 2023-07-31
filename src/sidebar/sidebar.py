import streamlit as st


def write(PAGES: list)  -> any:
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Lucas Gabriel and was built in `Python` using the `streamlit` library. 
        The purpose of this app is to show the use of a Data Warehouse to store and analyze data.
        Access the source code at:
        https://github.com/lucas-sales/md
"""
    )
    
    return PAGES[selection]
