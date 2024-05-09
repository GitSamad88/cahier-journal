import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from io import BytesIO
from bs4 import BeautifulSoup
from streamlit_extras.app_logo import add_logo
import pathlib
import shutil

# page configue
st.set_page_config(page_icon="app-images/Moudkira_dark_v_100_100.png",
    page_title="Emplois Du Temps")

add_logo("app-images/Moudkira_dark_v_100_100.png",height=80)


# google ads and analytics
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
    else :

        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)
        else:
            shutil.copy(index_path, bck_index)
        html = str(soup)
        html = html.replace(false_ga_script,"")
        html = html.replace(ga_script, "")
        new_html = html.replace('<head>', '<head>\n' + ga_script)
        index_path.write_text(new_html)
        new_soup = BeautifulSoup(index_path.read_text(), features="html.parser")


#inject_ga()


buffer = BytesIO()


def emplois_df(emplois):
    emplois["Jour"] = jours
    emplois["Matière"] = matieres
    emplois["Durée"] = dures
    emplois["Niveau"] = niveaux
    emplois["Séance"] = seances
    emplois.dropna(inplace=True)
    emplois.index=range(emplois.shape[0])
    #st.table(emplois)
    csv_file = emplois.to_csv(index=False)
    st.download_button(
        label="Téléchargez votre emplois",
        data=csv_file,
        file_name=f"emplois_{emplois['Niveau'].unique()[0]}_"
                  f"{emplois['Niveau'].unique()[1] if len(emplois['Niveau'].unique())==2 else emplois['Niveau'].unique()[0] }.csv",
        key="download_button"
    )


#st.markdown("Your Streamlit Application Begins here!")
if "emplois" not in st.session_state:
    st.session_state["emplois"] = pd.DataFrame(columns=["Jour", "Matière","Séance", "Durée","Niveau"])

emplois = pd.DataFrame(columns=["Jour", "Matière","Séance", "Durée","Niveau"])
st.title("Emplois Du Temps")
form = st.form(key="key1")

creat_or_import = form.selectbox("choisissez une option: ", ["Créer un nouveau emplois", "Importer votre emplois"],
                                 # max_selections=1,
                                 index=None, key="crorimpo",
                                 placeholder="Choisissez une option")  # default="Crèer un nouveau emplois")
form.form_submit_button("Confirmez votre choix")
if (creat_or_import == "Créer un nouveau emplois"):

    jours, matieres, dures, niveaux,seances = [],[],[],[],[]

    level1_courses = ["",'Maths', 'Eveil Scientifique', 'Act. Orales', 'Oral ', 'Lecture','Act. rituelle',
                      'Graphisme/ Ecriture/ Copie', 'Comptine/ Chant', 'Projet de classe','D.C.V','Amazigh & A.V.S']

    level2_courses= ["",'Maths', 'Eveil Scientifique','Act. orales', 'Exercices écrits','Act. rituelle'
                     'Projet de classe','Lecture', 'Ecriture',
                     'Poésie', 'Lecture/ Ecriture','Copie/ Dictée','D.C.V','Amazigh & A.V.S']
    level3_courses = ["",'Maths', 'Eveil Scientifique','Act. Orales', 'Lecture','Exercices écrits',
                      "Prod. de l'écrit", 'Ecriture / Copie', 'Dictée','Act. rituelle',
                      'Projet de classe','Poésie','D.C.V','Amazigh & A.V.S']

    level4_courses = ["",'Maths', 'Eveil Scientifique', 'Act.Orales', 'Grammaire', 'Conjugaison', 'Poésie',
                      'Ecriture / Copie','Lecture', "Prod. de l’écrit",'Act. rituelle',
                      'Projet de classe','Orth / Dictée','D.C.V','Amazigh & A.V.S']

    level5_courses = ["",'Maths', 'Eveil Scientifique','Act. Orales', 'Lecture diction','Act. rituelle',
                         'Orthographe', 'Lexique', 'Poésie', 'Lecture','Conjugaison', 'Projet de classe',
                          'Prod. de l’écrit','Grammaire',"Pro. de l'écrit/ Lecture diction",'D.C.V','Amazigh & A.V.S']

    level6_courses = ["",'Maths', 'Eveil Scientifique', 'Act. Orales', 'Conjugaison','Lexique',
                       'Projet de classe', 'Grammaire', 'Lecture','Act. rituelle',
                      "Pro. de l'écrit/ Lecture diction", 'Orthographe','D.C.V','Amazigh & A.V.S']

    for n, m in enumerate(["premier", "deuxième"]):
        niveau = form.selectbox("Sélectionnez le niveau", range(1, 7),
                                placeholder="choisissez une option",
                                index=None, key=f"niveau{n}")

        form.form_submit_button(f"Confirmez le {m} niveau")

        form.header(f"Emplois Du Niveau: {niveau if niveau != None else ''}")
        for jour in range(1, 7):
            form.info(f"Jour : {jour}")
            for i in range(1, 7):
                form.markdown(f"<h3 style='text-align: center;font-size: 12px;'> Matière : {i}</h1>",
                              unsafe_allow_html=True)
                col1, col2,col3 = form.columns(3)
                matiere = col1.selectbox("Sélectionnez une matière:",
                                         level1_courses if niveau == 1
                                         else level2_courses if niveau == 2
                                         else level3_courses if niveau == 3
                                         else level4_courses if niveau == 4
                                         else level5_courses if niveau == 5
                                         else level6_courses if niveau == 6
                                         else [None]
                                         , key=f"matière{i}jour{jour}niveau{n}")

                duree = col2.number_input("Entrez la durée: ",value=0,
                                          key=f"dure{i}jour{jour}niveau{n}")
                seance = col3.number_input("Entrez la séance: ",value=0,
                                          key=f"seance{i}jour{jour}niveau{n}")

                form.write("----------------")

                matieres.append(matiere)
                dures.append(int(duree) if duree!=0 else np.nan )
                seances.append(int(seance) if seance!=0 else np.nan)
                jours.append(jour)
                niveaux.append(niveau)
    emplois[["Séance", "Durée"]] = emplois[["Séance", "Durée"]].astype("int")
    enregistrer=form.form_submit_button("Enregistrez") 
    if enregistrer:
        try:
            emplois_df(emplois=emplois)
            st.success("votre emplois a été bien enregistré!")
        except Exception as ex:
            st.warning("Il faut au moins sélectionner une matière avec sa durée "
                      "et le numèro de sa séance!")


elif creat_or_import == "Importer votre emplois":
    # """warnings: you have to add instructions!"""
    st.warning(
        'Remarque: Votre fichier doit  être en format CSV.'
        'Les colonnes de votre fichier doivent être "Niveau", "Jour", "Matière", "Séance" et "Durée"')

    if st.button("Cliquez pour voir un exemple! "):
        example = pd.read_csv(
            "https://docs.google.com/spreadsheets/d/17Od8aGyqZPRXSyIIMLDklIhOLg1vApSrj5DXjs31nnI/gviz/tq?tqx=out:csv&sheet=emplois_3_4_LV")
        st.info("Emplois du temps de 3aep et 4aep:")
        st.table(example)
    # Upload a CSV file
    file = st.file_uploader("Importez votre emplois", type=["csv"])

    if file is not None:
        # Read the CSV file into a DataFrame

        emplois = pd.read_csv(file)
        if all(item in list(emplois.columns) for item in ["Jour", "Matière", "Séance", "Durée", "Niveau"]):
            emplois.dropna(inplace=True)
            emplois.index = range(emplois.shape[0])
            emplois[["Séance", "Durée"]] = emplois[["Séance", "Durée"]].astype("int")
            st.success("votre emplois a été bien importé!")
        else:
            #warnings
            st.warning("Attention! Les colonnes de votre fichier doivent "
                       "être :  Jour, Matière, Séance, Durée et Niveau!")

else:
    st.warning("svp, choisissez une option!")
    # creat_or_import == None:


st.table(emplois)
st.session_state["emplois"] = emplois

# Custom Footer and Hide right Menu
Hid_Menu = """
<style>
#MainMenu {
visibility : hidden;
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
    <p>Made by <a href="https://www.linkedin.com/in/abdessamad-taoufiq-082013209" target="_blank" style="font-style: oblique;">TAOUFIQ ABDESSAMAD</a>.</p>
    <p> tous droits réservés © 2023 </p>

</div>
"""


st.markdown(footer,unsafe_allow_html=True)
st.markdown(Hid_Menu,unsafe_allow_html=True)
