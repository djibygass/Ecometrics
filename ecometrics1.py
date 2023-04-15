import streamlit as st
from PIL import Image
import boto3
import io
from credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from streamlit_extras.let_it_rain import rain
from streamlit_extras.add_vertical_space import add_vertical_space


def main():
    st.set_page_config(layout="wide")

    rain(
        emoji="🌿💰",
        font_size=25,
        falling_speed=5,
        animation_length="1",
    )

    col1, col2 = st.columns([1, 14])

    add_vertical_space(1)
    col3, col4, col5, col6 = st.columns([1, 1, 1, 1,])
    # col3,col4,col5,col6=st.columns([8,8,8,8])
    # add_vertical_space(3)

    with col1:
        st.image("logo.PNG", width=80)
    with col2:
        st.title("Ecometrics")
    with col3:
        accueil_button = st.button("Accueil")
    with col4:
        a_propos_button = st.button("à propos")
    with col5:
        contact_button = st.button("Contact")
    with col6:
        blog_button = st.button("Blog")

    # Keep track of the current page
    current_page = None

    if accueil_button:
        current_page = "accueil"
    elif a_propos_button:
        current_page = "a_propos"
    elif contact_button:
        current_page = "contact"
    elif blog_button:
        current_page = "blog"

    if current_page == "accueil":
        accueil()
    elif current_page == "a_propos":
        a_propos()
    elif current_page == "contact":
        contact()
    elif current_page == "blog":
        blog()

    st.markdown(
        '<p style="text-align:center">&copy; Ecometrics 2023</p>',
        unsafe_allow_html=True)


def accueil():
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
        if st.button("Submit"):
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


def a_propos():
    st.title("À propos")
    st.write("Welcome to Ecometrics!")


def contact():
    st.title("Contact")
    st.write("Welcome to Ecometrics!")


def blog():
    st.title("Blog")
    st.write("Welcome to Ecometrics!")


if __name__ == "__main__":
    main()
