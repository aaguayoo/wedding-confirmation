"""{{cookiecutter.project_name.title()}} Streamlit Demo App."""
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def main() -> None:
    """Main fucntion."""
    st.set_page_config(page_title="My Streamlit app.", layout="wide")

    st.sidebar.title("Menú")
    opcion = st.sidebar.selectbox("Select one option:", ["Start", "Graph", "About"])

    if opcion == "Start":
        st.title("Welcome to my Streamlit app.")
        st.write("This is an example app using Streamlit.")

    elif opcion == "Graph":
        st.title("Example graph")
        fig, ax = plt.subplots()
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y)
        st.pyplot(fig)

    elif opcion == "About":
        st.title("About")
        st.write("This is a small Streamlit app template.")


if __name__ == "__main__":
    main()
