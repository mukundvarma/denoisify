"""Main module for the streamlit template app"""
import streamlit as st
import pandas as pd

def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Page 1", "Page 2"])

    st.sidebar.title("About")
    st.sidebar.info("""This app is a project template for streamplit apps.""")

    st.title("Template streamlit app")
    st.write("Some **markdown** placeholder *text*.")

    prices = pd.read_csv("data/prices.csv")
    st.write("Some price data:")
    st.write(prices)

if __name__ == "__main__":
    main()
