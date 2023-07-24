import src.pages.home 
import src.pages.db_tradicional
import src.pages.dw
import src.pages.about

import src.sidebar.sidebar as sidebar

import streamlit as st

PAGES = {
    "Home": src.pages.home,
    "Banco tradicional": src.pages.db_tradicional,
    "Data Warehouse": src.pages.dw,
    "About": src.pages.about,
}
def main():

    page = sidebar.write(PAGES)
    st.write(page.write())

if __name__ == "__main__":
    main()
