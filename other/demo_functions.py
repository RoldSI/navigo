import numpy as np
import streamlit as st

def main():
    st.title("Msg Hackathon Demo")
    c1, c2, c3 = st.columns([1,2,1])
    c1.write("Demo")
    c2.write("Code")
    c3.write("Here")

    
if __name__ == "__main__":
    main()