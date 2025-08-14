import streamlit as st
from streamlit_extras.app_logo import add_logo
import streamlit.components.v1 as components
from datetime import datetime
from PIL import Image

# page configue
st.set_page_config(page_icon = r"static/moudkira_dark_v_100_100.png",
                   page_title = "Comment ça marche?")

add_logo(r"static/moudkira_dark_v_100_100.png",height=80)

all_images = st.session_state["all_images"]

st.title("Comment ça marche?")
st.image(all_images["question.jpg"])#,width=500)#,use_column_width="auto")


st.subheader("Comment créer un emplois de temps? ")
st.write("La création d'emplois sur Moudakira.ma semble être un processus relativement simple. Voici les étapes clés à suivre, telles que décrites dans votre requête :")

st.write(" ***1. Sélectionner les niveaux ou les groupes :***")
st.write(" Commencez par choisir les niveaux ou les groupes d'élèves auxquels s'adresse l'emploi du temps. Cela vous permettra de définir les différentes sections de l'emploi du temps.")

st.write(" ***2. Sélectionner les matières enseignées :*** ")
st.write(" Ensuite, identifiez les matières qui seront enseignées dans le cadre de cet emploi du temps. "
         "Cela peut inclure des matières principales, des matières secondaires et des activités extracurriculaires.")

st.write(" ***3. Entrer les durées et les séances:***")
st.write(" Pour chaque matière et pour chaque niveau ou groupe,"
"définissez la durée de chaque cours et le nombre de séances par semaine. Cela permettra de planifier le temps alloué à chaque matière.")

st.write(" ***4. Enregistrez et téléchargez!:***")
st.write("maintenant, vous pouvez passer directement a la création de votre cahier de leçons journaliers, "
         "  comme vous pouvez aussi télécharger votre emplois se forme d'un fichier Excel pour l'utiliser ultérieurement. ")


st.write("En suivant ces étapes, vous devriez être en mesure de créer un emploi du temps clair et organisé sur Moudakira.ma."
"N'oubliez pas de vérifier les instructions spécifiques de la plateforme pour vous assurer de bien suivre la procédure.")

st.write("Si vous rencontrez des difficultés ou avez besoin d'aide supplémentaire,"
" n'hésitez pas à consulter la documentation de Moudakira.ma ou à contacter leur service d'assistance." )

st.write("La vidéo ci-dessus va vous illustrer tous ces étapes. ")
st.video("https://www.youtube.com/watch?v=PY7iry6sG3g")


st.subheader("comment créer un cahier des leçons journalières?")
st.write("Après avoir créé votre emploi du temps sur Moudakira.ma, vous pouvez compléter"
         " votre organisation pédagogique en générant votre cahier journal. Voici les étapes à suivre :")

st.write("***1. Choix des manuels adoptés:***")
st.write("Sélectionnez les manuels scolaires utilisés pour les cours de mathématiques, français et éveil scientifique dans chaque niveau. Cela permettra de lier les leçons aux ressources pédagogiques spécifiques.")

st.write("***2. Définition des séances:***")
st.write("Choisissez la séance du lundi (ou une autre journée selon vos besoins) et définissez les horaires d'entrée et de sortie des élèves, tant pour les cours du matin que de l'après-midi. Cela permettra de structurer le déroulement de la journée scolaire.")

st.write("***3. Enregistrement et téléchargement:***")
st.write("Une fois les informations saisies, enregistrez votre cahier journal. "
         "Vous devriez ensuite avoir la possibilité de le télécharger au format Excel")

st.video("https://www.youtube.com/watch?v=EpgrbQzYlI0")

st.write("***Remarques importantes:***")
st.write("- Les fonctionnalités spécifiques de création du cahier journal peuvent varier légèrement en fonction de la version de Moudakira.ma que vous utilisez.")
st.write("- Assurez-vous de disposer des informations correctes concernant les manuels adoptés et les horaires des cours avant de commencer la création du cahier journal.")
st.write("- Le cahier journal est un outil précieux pour suivre vos leçons, noter les progrès des élèves et organiser vos ressources pédagogiques.")

st.write("***N'hésitez pas à nous contacter si vous avez besoin d'aide supplémentaire pour créer votre cahier journal sur Moudakira.ma.***")
st.markdown("""<a href="mailto:moudakira.ma@gmail.com"> nous contacter</a>""",unsafe_allow_html=True)







# Custom Footer and Hide right Menu
Hid_Menu = """
<style>
#MainMenu {
   visibility : hidden;
<\style>
"""

current_year = datetime.now().year

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
        """+ f"""<p style='text-align: center;'>tous droits réservés © {current_year}</p>

    </div>
"""


st.markdown(footer,unsafe_allow_html=True)
st.markdown(Hid_Menu,unsafe_allow_html=True)









