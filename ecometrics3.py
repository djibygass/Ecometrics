import streamlit as st
from PIL import Image
import boto3
import io
from credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from streamlit_extras.let_it_rain import rain
import streamlit_theme as stt
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_theme import set_theme
import streamlit.components.v1 as components
import base64
import streamlit as st


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def main():

    st.set_page_config(layout="wide", initial_sidebar_state="expanded")

    add_bg_from_local('images/gradient1.jpg')

    col1, col2 = st.columns([1, 14])
    with col1:
        st.image("images/logo.PNG", width=80)
    with col2:
        st.title("Ecometrics")

    submitted = st.session_state.get('submitted', False)

    if not submitted:
        form = st.form(key='my_form')
        submit_button = False

        with form:
            # Display the image and form side by side
            col2, col1 = st.columns([1, 1])
            image = Image.open("images/photo1.png")
            with col1:
                st.image(image)
                
            with col2:
                st.title("Fill out the form")
                role = st.selectbox("Role", ["Employé", "Boss"])
                secteur = st.selectbox(
                    "Secteur d'activité", [
                        "Usine", "Hopital", "Bureaux", "Aéroport"])
                entreprise = st.text_input("Nom de l'entreprise")
                surface=st.text_input("Surface")
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

            st.session_state['submitted'] = True
            st.experimental_rerun()
            # Add custom CSS to style the submit button
        st.markdown("""
            <style>
                div.stButton > button:first-child {
                    background-color: #43949a;
                    color: white;
                    width: 20%;
                    margin: auto;
                    display: block;
                }
            </style>
        """, unsafe_allow_html=True)


    else:

        # Add links to other pages
        menu = {
            "Accueil": accueil,
            "A propos": a_propos,
            "Contact": contact,
            "Blog": blog
        }
        add_vertical_space(3)

        choice = st.sidebar.selectbox("Select a page", list(menu.keys()))
        menu[choice]()



def accueil():
    # Display the homepage
    add_vertical_space(3)
    col2, col1 = st.columns([2, 2])
    image = Image.open("images/photo1.png")
    with col1:
        st.image(image, width=650)
    with col2:
        st.markdown("<br><br><br><br><span style='font-size: 30px; line-height: 1.5;'>Ecometrics est une solution innovante pour améliorer la performance énergétique des bâtiments tout en réduisant l'impact environnemental. En utilisant notre application, les propriétaires et les gestionnaires de bâtiments peuvent réaliser des économies d'énergie significatives, prendre des décisions éclairées concernant leur consommation d'énergie et contribuer à un avenir plus durable.</span>", unsafe_allow_html=True)


def a_propos():
    st.title("A propos")
    st.write("This is the à propos page.")


def contact():
    st.title("Contact Us")
    st.write("This is the Contact page.")


def blog():
    st.title("My Blog")
    st.write("This is the Blog page.")


if __name__ == "__main__":
    main()
