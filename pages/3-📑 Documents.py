import sys
import streamlit as st
from datetime import datetime
from streamlit_extras.app_logo import add_logo
#from streamlit_extras.switch_page_button import switch_page



st.set_page_config(page_icon="static/moudkira_dark_v_100_100.png",
                   page_title="Documents")
#add a logo
add_logo("static/moudkira_dark_v_100_100.png",height=80)

st.title("📑 Documents prêts à imprimer pour votre cahier journal")
st.write("Retrouvez ici une sélection de pages utiles déjà prêtes à l’emploi pour vos cahiers journaliers."
"Chaque document est disponible en version PDF et peut être ouvert directement sur Google Drive. Vous pourrez ensuite l’imprimer ou le télécharger pour l’utiliser dans votre classe.")





st.subheader("📘 Page de Garde ")
st.image("static/moudakira_cover_page.JPG", width=200)

st.subheader("📄 Pages Vides ")
st.image("static/page_vide_moudakira.JPG", width=200)


st.subheader("📝 Documents Pédagogiques ")
st.image("static/doc_peda.JPG", width=200)



st.markdown("[      Télécharger les documents     ](https://drive.google.com/drive/folders/1eAI1mIRtI3DJFpGzGvBs7iXHIZfYc6CA?usp=sharing)")


