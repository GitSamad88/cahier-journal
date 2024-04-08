import requests
import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components
from streamlit_extras.app_logo import add_logo
from streamlit_signin_auth_ui.widgets import __login__
from bs4 import BeautifulSoup
from st_pages import Page, add_page_title, show_pages
import pathlib
import urllib.request
import shutil
import time

st.set_page_config(page_icon=r"C:\Users\hp\PycharmProjects\Streamlitt_App\Multipages_App\app-images\Moudkira_dark_v_100_100.png",
                   page_title="Page D'acceuil")




#add_logo(req_img.content,height=80)
add_logo(r"C:\Users\hp\PycharmProjects\Streamlitt_App\Multipages_App\app-images\Moudkira_dark_v_100_100.png",height=80)

st.image(r'C:/Users/hp/PycharmProjects/Streamlitt_App/Multipages_App/app-images/Moudakira_Banner_626x210.png')

# Inject google ads and analytics
GA_ID = "google_analytics"
ga_script = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2TE23YZQ28"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-2TE23YZQ28');
</script> """

false_ga_script = """<!-- Google tag (gtag.js) -->
<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-2TE23YZQ28"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-2TE23YZQ28');
</script>"""


def inject_ga():
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")

    if ("Google tag" not in str(soup)):
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)
        else:
            shutil.copy(index_path, bck_index)
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + ga_script)
        index_path.write_text(new_html)
    else:
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)
        else:
            shutil.copy(index_path, bck_index)
        html = str(soup)
        html = html.replace(false_ga_script, "")
        html = html.replace(ga_script, "")
        new_html = html.replace('<head>', '<head>\n' + ga_script)
        index_path.write_text(new_html)


inject_ga()

# link = "Made by [TAOUFIQ ABDESSAMAD](https://www.linkedin.com/in/abdessamad-taoufiq-082013209)"
# st.sidebar.write(" ")
# st.sidebar.markdown(link,unsafe_allow_html=True)

st.title("Moudakira.ma: Cahier De Leçons Journaliers ")
st.write("Bienvenue, "
         "Moudakira.ma est une application novatrice conçue spécialement pour simplifier la vie des enseignants du "
         "cycle primaire. "
         "Notre application vise à transformer l'expérience de la tenue de journal en une tâche simple, intuitive et "
         "efficace, "
         " offrant ainsi aux enseignants plus de temps pour se concentrer sur l'essentiel : l'éducation de leurs élèves")

col1, col2 = st.columns([0.4, 0.6])
col1.header("Fonctionnalités Clés :")

col1.write("1. ***Création Facile de Cahiers Journal :*** "
           "Avec Moudakira.ma, la création de cahier journal n'a jamais été aussi simple. "
           "Les enseignants peuvent enregister les matières, les durées, les éléments du cours, les nombres du séances,"
           "dans 5 minutes avec simples cliques."
           " le tout dans une interface conviviale.")



#col2.image(add_img("1s4_MBmKmY8KLgByiDpEdBe98CeiI6oTK"),output_format="png")
col2.image(r"C:\Users\hp\PycharmProjects\Streamlitt_App\Multipages_App\app-images\journal_presentation_d2.png")

col3, col4 = st.columns([0.6,0.4])
#col3.image(add_img("15T3pBagTfJuQIbNc1cWXf_t-lP19kJAP"),output_format="png")
col3.image(r"C:\Users\hp\PycharmProjects\Streamlitt_App\Multipages_App\app-images\emplois_presen_d3.png")
col4.write("2. ***Comment ça marche? :*** "
           "Vous créez d'abord un emploi du temps ou vous importez le votre si vous avez déjà créer "
           "un (en format CSV), puis vous créez votre cahier journal en choisissant: les niveaux scolaires ou les "
           "groupes, les manuels utilisés, "
           "l'unité et les horaires, vous enregistrez votre sélectionnes."
           "Enfin vous télécharger votre cahier journal en format Excel.")


col5,col6 =st.columns([0.4,0.6])
col5.subheader("Pourquoi Moudakira.ma ?")
col5.write("Moudakira.ma a été créé avec la conviction que la gestion du suivi des élèves "
           "devrait être aussi enrichissante que l'enseignement lui-même."
           " Notre application vise à simplifier le processus de création de cahier journal tout en offrant"
           " des outils puissants pour améliorer la communication et l'efficacité pédagogique.")

embed_video="""
<iframe src="https://drive.google.com/file/d/1Z6n3-Uyvu3UyZJkNHf864B0_Z2uLRTao/preview"
 width="420" height="280" allow="autoplay"></iframe> 
"""
col6.markdown(embed_video,unsafe_allow_html=True)


st.write("Téléchargez votre cahier journal dès aujourd'hui et découvrez "
           "comment notre application peut transformer"
           "la façon dont les enseignants du cycle primaire gèrent leurs cahiers de journal,"
           "libérant ainsi du temps précieux pour se concentrer sur"
           "l'enseignement et l'épanouissement de leurs élèves.")


def login():
    cred = pd.read_csv("https://docs.google.com/spreadsheets/d/1c0KODi57SYHz569TKxeHrCRsHs3FVE3POnPF06K_biU/gviz/tq?tqx=out:csv&sheet=cred")
    json_auth_ = cred.set_index(cred.columns[0]).to_dict()["0"]

    __login__obj = __login__(credentials=json_auth_,
                 smtp_username='moudakira.ma@gmail.com',
                 smtp_password='oamw onhc lmjk kpex',
                 company_name="Moudakira.ma",
                 width=200, height=300,
                 logout_button_name='Sortir', hide_menu_bool=False,
                 hide_footer_bool=False,
                 lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()

    if LOGGED_IN == True:
        st.success("Bienvenue!")

st.subheader("S'enregister")
login()


# Custom Footer and Hide right Menu
Hid_Menu = """
<style>
#MainMenu {
   visibility : hidden;}
<\style>
"""
footer = """
    <style>
        .footer {
            position:relative ;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            padding: 10px;
            text-align: center;
            font-size: 10px;
            color: #555;
        }
    </style>
    <div class="footer">
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <hr>
        <p>Made by <a href="https://www.linkedin.com/in/abdessamad-taoufiq-082013209" target="_blank", style="font-style: oblique;">TAOUFIQ ABDESSAMAD</a>.</p>
        <p> tous droits réservés © 2024 </p>

    </div>
"""

st.markdown(footer, unsafe_allow_html=True)
st.markdown(Hid_Menu, unsafe_allow_html=True)
