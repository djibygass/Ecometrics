import streamlit as st
from PIL import Image
import boto3
import io
from credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from streamlit_extras.let_it_rain import rain
import streamlit_theme as stt
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_theme import set_theme


def main():

    # set_theme('.streamlit/config.toml')
    st.set_page_config(layout="wide")

    rain(
        emoji="🌿💰",
        font_size=25,
        falling_speed=5,
        animation_length="1",
    )  # 🔋🌿

    col1, col2 = st.columns([1, 14])
    with col1:
        st.image("logo.PNG", width=80)
    with col2:
        st.title("Ecometrics")

    form = st.form(key='my_form')
    submit_button = False

    with form:
        # Display the image and form side by side
        col1, col2 = st.columns([2, 2])
        image = Image.open("photo1.png")
        with col1:
            st.image(image)
        with col2:
            st.title("Fill out the form")
            role = st.selectbox("Role", ["Employé", "Boss"])
            secteur = st.selectbox(
                "Secteur d'activité", [
                    "Usine", "Pharmacie", "Bureaux"])
            entreprise = st.text_input("Nom de l'entreprise")
            surface = st.text_input("Surface")
            submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Create a CSV string from the form data
        csv_string = f"{role},{secteur},{entreprise},{surface}"

        # Upload the CSV string to S3
        BUCKET_NAME = "pa-csv"
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        csv_buffer = io.BytesIO(csv_string.encode('utf-8'))
        s3.upload_fileobj(csv_buffer, BUCKET_NAME, 'form_data.csv')
        st.success("CSV file uploaded successfully")

        # Redirect to the multipage webapp
        menu = {
            "Accueil": accueil,
            "à propos": a_propos,
            "Contact": contact,
            "Blog": blog
        }
        add_vertical_space(3)

        choice = st.sidebar.selectbox("Select a page", list(menu.keys()))
        menu[choice]()
    else:
        accueil()


def accueil():
    st.title("Welcome to Accueil")


def a_propos():
    menu = {
        "Accueil": accueil,
        "à propos": a_propos,
        "Contact": contact,
        "Blog": blog
    }
    st.title("About My Multi-Page App")
    st.write("This is the à propos page.")
    add_vertical_space(3)
    choice = st.sidebar.selectbox("Select a page", list(menu.keys()))
    menu[choice]()


def contact():

    menu = {
        "Accueil": accueil,
        "à propos": a_propos,
        "Contact": contact,
        "Blog": blog
    }
    st.title("About My Multi-Page App")
    st.write("This is the contact page.")
    add_vertical_space(3)
    choice = st.sidebar.selectbox("Select a page", list(menu.keys()))
    menu[choice]()


def blog():

    menu = {
        "Accueil": accueil,
        "à propos": a_propos,
        "Contact": contact,
        "Blog": blog
    }
    st.title("About My Multi-Page App")
    st.write("This is the à propos page.")
    add_vertical_space(3)
    choice = st.sidebar.selectbox("Select a page", list(menu.keys()))
    menu[choice]()


if __name__ == "__main__":
    main()
