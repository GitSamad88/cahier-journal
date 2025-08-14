import os,requests
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_extras.app_logo import add_logo
from streamlit_signin_auth_ui.widgets import __login__
import streamlit_star_rating as st_rating

import re,secrets, gspread, pathlib,shutil,time, warnings,json, toml
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import urllib.request


st.set_page_config(page_icon="static/moudkira_dark_v_100_100.png",
                   page_title="Page D'accueil")




#add a logo
add_logo("static/moudkira_dark_v_100_100.png",height=80)

st.image('static/banner-moudakira-no-logo.png')

# Inject Google Analytics
GA_ID = "google_analytics"
ga_script = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2TE23YZQ28"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-2TE23YZQ28');
</script> """

false_ga_script ="""<!-- Google tag (gtag.js) -->
<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-2TE23YZQ28"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-2TE23YZQ28');
</script>"""

g_adsense = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4265574502229447"
     crossorigin="anonymous"></script>
     """
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
        new_html = html.replace('<head>', '<head>\n'+ g_adsense + '\n' + ga_script)
        index_path.write_text(new_html)
    else :

        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)
        else:
            shutil.copy(index_path, bck_index)
        html = str(soup)
        html = html.replace(false_ga_script,"")
        html = html.replace(ga_script, "")
        html = html.replace(g_adsense,"")
        new_html = html.replace('<head>', '<head>\n'+ g_adsense + '\n' + ga_script)
        index_path.write_text(new_html)
inject_ga()



# Scroll to the top
js_code = """
<script>
window.onload = function() {
    window.scrollTo(0, 0);
}
</script>
"""

#components.html(js_code)
st.markdown(js_code, unsafe_allow_html=True)


# write title, subheaders and paragraphes
# add video and images 
st.title("Moudakira.ma: Cahier des Leçons Journalières ")
st.write("Bienvenue, "
         "Moudakira.ma est une application novatrice conçue spécialement pour simplifier la vie des enseignants du "
         "cycle primaire. "
         "Notre application vise à transformer l'expérience de la tenue de cahier journal en une tâche simple, intuitive et "
         "efficace, "
         " offrant ainsi aux enseignants plus de temps pour se concentrer sur l'essentiel : l'éducation de leurs élèves")

col1, col2 = st.columns([0.4, 0.6])
col1.header("Fonctionnalités Clés :")

col1.write("1. ***Création Facile de Cahier Journal :*** "
           "Avec Moudakira.ma, la création de cahier journal n'a jamais été aussi simple. "
           "Les enseignants peuvent enregister les matières, les durées, les éléments du cours, les nombres du séances,"
           "dans 5 minutes avec simples cliques."
           " le tout dans une interface conviviale.")




col2.image("/static/capture_cahier_journal.png")

col3, col4 = st.columns([0.6,0.4])

col3.image("app-images/emplois_presen_d3.png")
col4.write("2. ***Comment ça marche? :*** "
           "Vous créez d'abord un emploi du temps ou vous importez le votre si vous avez déjà créer "
           "un (en format CSV), puis vous créez votre cahier journal en choisissant: les niveaux scolaires ou les "
           "groupes, les manuels utilisés, "
           "l'unité et les horaires, vous enregistrez votre sélectionnes."
           "Enfin, vous télécharger votre cahier journal en format Excel.")


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
           "comment notre application peut transformer "
           "la façon dont les enseignants du cycle primaire gèrent leurs cahiers de journal, "
           "libérant ainsi du temps précieux pour se concentrer sur"
           "l'enseignement et l'épanouissement de leurs élèves.")



# Login form
def login():
  #Initialize variables
  secrets_auth = {}
  smtp_gmail_ = ""
  smtp_password_ = ""
  title_placeholder = st.empty()
  title_placeholder.subheader("Se connecter")


  secrets_auth = os.getenv("google_sheets_api_credentials","{}")
  secrets_auth = json.loads(secrets_auth)


  smtp_gmail_ = os.getenv("smtp_gmail","")
  smtp_password_ = os.getenv("smtp_password","")
    
  __login__obj = __login__(credentials=secrets_auth,
                      smtp_username = smtp_gmail_,
                      smtp_password = smtp_password_,
                      company_name = "moudakira.ma",
                      width = 200, height = 300,
                      logout_button_name = 'Déconnecter', hide_menu_bool = False,
                      hide_footer_bool = False,
                      lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')


  LOGGED_IN = __login__obj.build_login_ui()
  if LOGGED_IN:
    title_placeholder.empty()
    
  return LOGGED_IN


if "LOGGED_IN" not in st.session_state:
    st.session_state["LOGGED_IN"] = False
    #st.info("Si vous n'avez pas un compte, Veuillez cliquer sur ***Créer un compte*** dans la barre de navigation pour créer un.", icon="ℹ️")
#if not st.session_state["LOGGED_IN"]:
    #with st.container(border = False):
        #if __name__ == "__main__":
            #login()
            
elif __name__ == "__main__":
  st.write("")
    #login()



# Add a comment section
@st.cache_resource(show_spinner=False)
def worksheet(_auth):

    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    Worksheet = ServiceAccountCredentials.from_json_keyfile_dict(_auth, scope)
    client = gspread.authorize(Worksheet)
    db = client.open("mydb").worksheets()[1]
    return db

comm_db = worksheet(json.loads(os.getenv("google_sheets_api_credentials","{}")))  
comments = pd.DataFrame(comm_db.get_values(), columns = comm_db.get_values()[0]).drop(index=0)


COMMENT_TEMPLATE_MD = """{} - {}
> {}
>> {}
"""


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

# Comments part

with st.expander("**💬 Avis:**",expanded=True):

    # Show comments

    for index, entry in enumerate(comments.itertuples()):
        st.markdown(COMMENT_TEMPLATE_MD.format( f''':red[{entry.name}]''', f''':green[{entry.date}]''', entry.comment,
                                               f''':violet[{entry.review}]'''))

        is_last = index == len(comments) - 1
        is_new = "just_posted" in st.session_state and is_last
        if is_new:
            st.success("☝️ Ton avis a été posté avec succès!")

    space(2)

    # Insert comment

    st.write("**Ajoutez votre avis:**")
    form = st.form("commentaire")
    name = form.text_input("Nom")
    comment = form.text_area("Commentaire")
    star = st_rating.st_star_rating(label="svp evaluez votre experience", maxValue=5, defaultValue=4, key="rating" )
    #stars = form.write(star)
    submit = form.form_submit_button("Ajoutez un commentaire")

    if submit:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        comm_db.append_row([name, comment, f'{star}🌟',str(date)])
        if "just_posted" not in st.session_state:
            st.session_state["just_posted"] = True
        st.experimental_rerun()


current_year = datetime.now().year


# Custom Footer and Hide right Menu
hid_menu = """
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
        """+ f"""<p style='text-align: center;'>tous droits réservés © {current_year}</p>
    </div>
   
  """

st.markdown(footer, unsafe_allow_html=True)
st.markdown(hid_menu, unsafe_allow_html=True)












































