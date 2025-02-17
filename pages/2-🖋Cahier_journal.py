import time, re, gspread, random
import streamlit as st
from streamlit_modal import Modal
from streamlit_signin_auth_ui.widgets import __login__
import streamlit.components.v1 as components
from streamlit_extras.app_logo import add_logo
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import pathlib,  shutil
from datetime import datetime
import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl.utils import get_column_letter
from babel.dates import format_datetime
from io import BytesIO
import warnings,json
warnings.filterwarnings("ignore")

# page configue
st.set_page_config(page_icon=r"app-images/Moudkira_dark_v_100_100.png",
    page_title="Cahier Journal")

add_logo(r"app-images/Moudkira_dark_v_100_100.png",height=80)


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
#inject_ga()


docs_link = "https://docs.google.com/spreadsheets/d/"
linkc = "/gviz/tq?tqx=out:csv&sheet="

@st.cache_resource
def fr_manuel_level(manuel, level):

    #'''-----------------------------------------------------  Frensh   --------------------------------------------------'''
    #"""retrive reapartition by level and manuel name """

    U_S = {
        "U": [0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 11, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 22, 23],
        "S": [0, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 11, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 22, 23]}

    fr_manuels_dict = {}
    #""" faire,dire """
    if manuel == "Faire Dire":
        faire1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1BM-ZXIFpCWMCdzkFhREMOuge6iG-19YZBMi6nzuCz2A"+linkc+"Repa_Fr_Dire_Faire_1aep")
        faire2 = faire3 = faire4 = faire5 = faire6 = pd.DataFrame()
        global Faire
        Faire = [faire1, faire2 , faire3, faire4, faire5, faire6]
        fr_manuels_dict["Faire Dire"]=Faire

    if manuel=="Mes apprentissages":
        #      """-----mes appreantissges-----"""
        mes_app1 = pd.DataFrame()
        mes_app2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1YpCjGEsGTgcEsd2GycBu_p9WT7SuIkRvuSj7DgwLGPY/gviz/tq?tqx=out:csv&sheet=Repa_Fr_Mes_App_2aep")
        mes_app3 = pd.read_csv("https://docs.google.com/spreadsheets/d/1HpLYUHC9hm234KismLpPjS7WjmjenLSOPO1dN2ppLs4/gviz/tq?tqx=out:csv&sheet=repartition_annuelle_fr_mes_apprentissage_3aep")
        mes_app4 = pd.read_csv("https://docs.google.com/spreadsheets/d/1i0cQ8rw-H_-HZ8HYrDa2tmM20lXlcU9bkYByD-MUN_I/gviz/tq?tqx=out:csv&sheet=repartiton_FR_Mes_apprentissage_4AEP")
        mes_app5 = pd.read_csv("https://docs.google.com/spreadsheets/d/1AZS1Mbv8ht1eAH-bsXrpoAyxzEcg4OFZb6bJzp5yRmo/gviz/tq?tqx=out:csv&sheet=annuelle_repa_mes_app_5aep")
        mes_app6 = pd.read_csv("https://docs.google.com/spreadsheets/d/1MbQy6JjTmIuNV_ZF3FA76Xq9xj1f4oq_SUo5viADrQw/gviz/tq?tqx=out:csv&sheet=Repa_Fr_Mes_app_6aep")
        Mes_app_manuel = [mes_app1, mes_app2, mes_app3, mes_app4, mes_app5, mes_app6]
        fr_manuels_dict["Mes apprentissages"]=Mes_app_manuel
        #print(fr_manuels_dict)


    if manuel=="Espace de l'école":
        #"""-----Espace de l'ècole-----"""
        espace1 = espace3 = espace4 = espace5 = espace6 = pd.DataFrame()
        espace2 = pd.read_csv(docs_link+"1E2tZWzNNdS81H2ljxUzsugxeI2G9AQJx0QdQfv8ipjg"+linkc+"Repa_Fr_Espace_De_Lecole_2aep")
        Espace = [espace1,espace2,espace3,espace4,espace5,espace6]
        fr_manuels_dict["Espace de l'école"]=Espace


    if manuel=="L'école de mots":
        #"""-----L'école de mots-----"""
        ecole1 = ecole2 = ecole3 =  ecole5 = ecole6 = pd.DataFrame()
        ecole4 = pd.read_csv(docs_link+"1XEHukH1KTxTAOf-SAQjSS39UorL-3FIe1MhlLFLysT4"+linkc+"Repa_Fr_Lecole_de_mots_4aep")
        Ecole_de_mots = [ecole1,ecole2,ecole3,ecole4,ecole5,ecole6]
        fr_manuels_dict["L'école de mots"]=Ecole_de_mots

    #"""------L'oasis des mots------"""
    if manuel == "L'oasis des mots":
        oasis1 = oasis4 = oasis5 = oasis6 = pd.DataFrame()
        oasis2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1iWmFNaqBl_gMZ1GczkH9RKpKcpEQWpI25jMVYZdFoyM"+linkc+"Repa_Fr_Loasis_Des_Mots_2aep")
        oasis3 = pd.read_csv("https://docs.google.com/spreadsheets/d/1dao2lt1dXO3zToaHFOtiK19zYdUXQtvzHo7vgsf62Co"+linkc+"Repa_Fr_Loasis_3aep")
        Oasis = [oasis1,oasis2,oasis3,oasis4,oasis5,oasis6]
        fr_manuels_dict["L'oasis des mots"]=Oasis


    if manuel =="Nouvel espace":
        #"""-----Nouvel Espace-----"""
        nouvel_espace1 = nouvel_espace3 = nouvel_espace5 = nouvel_espace6 = pd.DataFrame()
        nouvel_espace2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1n9j1BlRkIVxjGB_74TNfJLTQEGaIrCl1jyuhxq9Dbs8"+linkc+"Repa_Fr_Nouvel_Espace_2aep")
        nouvel_espace4 = pd.read_csv("https://docs.google.com/spreadsheets/d/1EYLaBN3rHkCRgx5HpNRoeQ8RAFabj8-a1ougO-Cu_u4"+linkc+"Repa_Fr_Nouvel_Espace_4aep")
        Nouvel_espace = [nouvel_espace1,nouvel_espace2,nouvel_espace3,nouvel_espace4,nouvel_espace5,nouvel_espace6]
        fr_manuels_dict["Nouvel espace"]=Nouvel_espace


    if manuel == "Parcours français":
        #"""----Parcours Français----"""
        parcours1 = parcours2 = parcours3 = parcours4 = parcours5 =pd.DataFrame()
        parcours6 = pd.read_csv("https://docs.google.com/spreadsheets/d/1ESEZCpX_IuKVNG3gLJ1IEc1jWlBn-xdpUPirpx4vLHY"+linkc+"Repa_Fr_Parcours_6aep")
        Parcours = [parcours1, parcours2, parcours3,parcours4,parcours5,parcours6]
        fr_manuels_dict["Parcours français"]=Parcours


    if manuel == "Pour communiquer":
        pour_comm1 = pour_comm2 = pour_comm3 = pour_comm4 = pour_comm6 = pd.DataFrame()
        pour_comm5 = pd.read_csv("https://docs.google.com/spreadsheets/d/1nkeR0Xdfj7pdkM606hscR7RCHyxRpAVldvVPWEBe3KM"+linkc+"Repa_Fr_Pour_Communiquer_5aep")
        Pour_Communiquer = [pour_comm1, pour_comm2, pour_comm3, pour_comm4, pour_comm5, pour_comm6]
        fr_manuels_dict["Pour communiquer"]=Pour_Communiquer

    for i in fr_manuels_dict.values():
        for n in i:
            if n.empty == False:
                n.index = U_S["S"]
                n["U"] = U_S["U"]
                n["S"] = U_S["S"]
        for n in i[3:]:
            if n.empty == False:
               n["Lecture"] = "Lire un text (type de text): " + n["Lecture"].str.replace("-","")



    try:
        if fr_manuels_dict[str(manuel)][int(level) - 1].empty:
            return "Ce manuel n'est pas disponible pour ce niveau, choisissez un autre manuel!"
        else:
            return fr_manuels_dict[str(manuel)][int(level) - 1]
    except:
        print("Ce manuel n'est pas disponible pour ce niveau, essayez un autre manuel!")
        print("Remarque: le niveau doit être entre 1 et 6!")


@st.cache_resource
def maths_manuel_level(manuel, level):
    #'''------------------------------------        Maths         -------------------------------------'''

    #""" retrive maths repa by manuel name and level"""
    U_Maths = [0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 17, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5,
               5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 33]

    S_Maths = [0, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 17, 1, 2, 3, 4, 5, 1, 1, 1, 2, 2, 2,
               3, 3, 3, 4, 4, 4, 5, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 33]

    Maths_seance = [[1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5],
     [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5],
     [1,2,3,4,5], [1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],
     [1,2,3,4,5], [1,2], [3,4], [5], [1,2], [3,4], [5], [1,2], [3,4], [5], [1,2], [3,4],[5],
     [1,2,3,4,5], [1,2], [3,4],[5],[1,2],[3,4],[5],[1,2], [3,4],[5], [1,2], [3,4], [5],
     [1,2,3,4,5],[1,2,3,4,5]]

    Maths_manuels={}
    #"""------- Moufid -------"""
    if manuel=="المفيد":
        #moufid1 = pd.read_csv("https://drive.google.com/uc?export=download&id=1xZYU1fmeIlcsICUw_ePz7nU_sSEYJwra")
        moufid1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1SeiSfWsp7HKiDjPhtWBk_MRPffjsrHhgBIrS99-S9gs"+linkc+"Repa_Maths_Moufid_1aep")
        moufid2 = moufid3  = moufid6 =  pd.DataFrame()
        moufid4 = pd.read_csv("https://docs.google.com/spreadsheets/d/1RWOJDkvdpPyNrM9s6iuP6vq-uWnjD4-grJOJAIViTKM"+linkc+"Repa_Maths_Moufid_4aep")
        moufid5 = pd.read_csv("https://docs.google.com/spreadsheets/d/12C9AT7pIp-SDZ8mn9F7V0pUKK2KNsCt1HZFj4lE7iL8"+linkc+"Repa_Maths_Almoufid_5aep")
        Moufid = [moufid1, moufid2, moufid3, moufid4, moufid5, moufid6]
        Maths_manuels["المفيد"] = Moufid

    #"""----Jayed-----"""
    if manuel == "الجيد":
        jayed1 = jayed3 = jayed5 = pd.DataFrame()
        jayed2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1boAFep-ooci_LQyQ4X3RkX2pjmjbNJM6dpvLgMz8Nyw"+linkc+"Repa_Maths_Jayed_2aep")
        jayed4 = pd.read_csv("https://docs.google.com/spreadsheets/d/1kk4n_1DyGk_aQOKT2xmhNSSjKVMuYj5tcM387qDVt8o"+linkc+"Repa_Maths_Jayed_4aep")
        jayed6 = pd.read_csv("https://docs.google.com/spreadsheets/d/1Jqt50GIXwP3HQZAUnD3wIq0UGexVrfJaETe8O0y2oRE"+linkc+"Repa_Maths_Jayed_6aep")
        Jayed= [jayed1, jayed2, jayed3, jayed4, jayed5, jayed6]
        Maths_manuels["الجيد"] = Jayed

    #"""----Fadaa-----"""
    if manuel == "الفضاء":
        fada1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1fUZRGEnZXn8WNQ0557sQAvcC3ejCzXlUAQVUZ2UHhQQ"+linkc+"Repa_Maths_Fada2_1aep")
        fada4 = fada5 = fada6 = pd.DataFrame()
        fada2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1kNDJfembuOL47-xtL7_tLM_OMk5mDyJlndD5s9v1JQw"+linkc+"Repa_Maths_Fada2_2aep")
        fada3 = pd.read_csv("https://docs.google.com/spreadsheets/d/1zM_tG0zlfV3So3CFOsO2Aaqk4Ca6g_UX093gTZrfotM"+linkc+"Repa_Maths_Fada2_3aep")
        Fadaa = [fada1, fada2, fada3, fada4, fada5, fada6]
        Maths_manuels["الفضاء"] = Fadaa


    #"""---Annajah---"""
    if manuel == "النجاح":
        najah5 = pd.read_csv("https://docs.google.com/spreadsheets/d/1tKcXYG2EteNmNFJsdXJgdvkRAhVL3FCifad1-dRSbnE"+linkc+"Repa_Maths_Anaja7_5aep")
        najah1 = najah2 = najah3 = najah4 = najah6 = pd.DataFrame()
        Anajah = [najah1,najah2,najah3,najah4,najah5,najah6]
        Maths_manuels["النجاح"] = Anajah

    #"""-----Jadid-----"""
    if manuel =="الجديد":
        jadid1 = jadid2 = jadid3 = jadid4 = jadid5 = pd.DataFrame()
        jadid6 = pd.read_csv("https://docs.google.com/spreadsheets/d/1AQnPGRV3EvfiS6JPggjxb2d-bAxkoSoSLEkIw1kiSkk"+linkc+"Repa_Maths_Jadid_6aep")
        Jadid = [jadid1, jadid2, jadid3,jadid4, jadid5,jadid6]
        Maths_manuels["الجديد"]=Jadid

    #"""----Marjii----"""
    if manuel == "المرجع":
        marjii1 = marjii4 = marjii5 = marjii6 = pd.DataFrame()
        marjii2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1PeWXWqVwMHF7MNmTudRo68-5ihoEMkN1gUTkYHfbNa0"+linkc+"Repa_Maths_Marji3_2aep")
        marjii3 = pd.read_csv("https://docs.google.com/spreadsheets/d/1XAQ9UfrHB8X0HwJ6CpxXMVWbszUyYRj2f8VpjWf-q9w"+linkc+"Repa_Maths_Marji3_3aep")
        Marjii = [marjii1,marjii2,marjii3,marjii4,marjii5,marjii6]
        Maths_manuels["المرجع"] = Marjii


    for i in Maths_manuels.values():
        for n in i:
            if n.empty == False:
                n["U"] = U_Maths
                n["S"] = S_Maths
                n["Séance"] = Maths_seance
    try:
        if Maths_manuels[str(manuel)][int(level) - 1].empty:
            return "Ce manuel n'est pas disponible pour ce niveau, choisissez un autre manuel!"
        else:

            return Maths_manuels[str(manuel)][int(level) - 1]

    except:
        print("Ce manuel n'est pas disponible pour ce niveau, choisissez un autre manuel!")
        print("Remarque: le niveau doit être entre 1 et 6!")


@st.cache_resource
def EvSc_manuel_level(level, manuel):
    #"""------------------------------------------------     Eveil Scientifque      ---------------------------------------------"""
    #"""retrive EvSc repartition by level and manuel name """
    EvSc_manuels={}

    if manuel=="الجديد":
        #""""----Jadid----"""
        es_Jadid1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1s61a71JzE4MQsC5AYRy20kTlpYskfuU8UovoU9yfeJg"+linkc+"Repa_EvSc_Jadid_1aep")
        es_Jadid1 = es_Jadid1[["U", "S", "Eveil Scientifique", "Séance"]].dropna(axis=0)
        es_Jadid1["Séance"] = [json.loads(es_Jadid1["Séance"][i]) for i in range(len(es_Jadid1["Séance"]))]

        es_Jadid2 = es_Jadid3 = es_Jadid4 = es_Jadid5 = es_Jadid6 = pd.DataFrame()
        es_jadid_manuel = [es_Jadid1,es_Jadid2,es_Jadid3,es_Jadid4,es_Jadid5,es_Jadid6]
        EvSc_manuels["الجديد"]=es_jadid_manuel

    #"""----Fadaa----"""
    if manuel == "الفضاء":
        es_fadaa1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1jCKg31ZFO3ONJsGA9hPDGbkxsMvyRCNLLUasRbtfCRo"+linkc+"Repa_EvSc_Fadaa_1aep")
        es_fadaa1["Séance"] = [json.loads(es_fadaa1["Séance"][i]) for i in range(len(es_fadaa1["Séance"]))]

        es_fadaa2 = es_fadaa3 =es_fadaa5= pd.DataFrame()
        pd.DataFrame()
        es_fadaa4 = pd.read_csv("https://docs.google.com/spreadsheets/d/1QM8kJ1YBexKcdPWAPBWg8Jz7H8u4RPehvfco6zMfqCU"+linkc+"Repa_EvSc_Fadaa_4aep")
        es_fadaa4["Séance"] = [json.loads(es_fadaa4["Séance"][i]) for i in range(len(es_fadaa4["Séance"]))]

        es_fadaa6 = pd.read_csv("https://docs.google.com/spreadsheets/d/1u4z1-1t_KqqeRRXmwlIS7PNPvUjZL_dLErNjmqm3HkM"+linkc+"Repa_EvSc_Fada2_6aep")
        es_fadaa6 = es_fadaa6[["U", "S", "Eveil Scientifique", "Séance"]].dropna(axis=0)
        es_fadaa6["Séance"] = [json.loads(es_fadaa6["Séance"][i]) for i in range(len(es_fadaa6["Séance"]))]
        es_fadaa_manuel = [es_fadaa1,es_fadaa2,es_fadaa3, es_fadaa4, es_fadaa5,es_fadaa6]
        EvSc_manuels["الفضاء"]= es_fadaa_manuel


    #"""----Manhal----"""
    if manuel == "المنهل":
        manhal1 = manhal2 = manhal4 = manhal6 = pd.DataFrame()

        manhal3=pd.read_csv("https://docs.google.com/spreadsheets/d/1tPN6uHeAEci7tizdQ_FXxzmzMCVO_5G_Y_ZBkojODc8"+linkc+"Repa_EvSc_Manhal_3aep")
        manhal3 = manhal3[["U", "S", "Eveil Scientifique", "Séance"]].dropna(axis=0)
        manhal3["Séance"] = [json.loads(manhal3["Séance"][i]) for i in range(len(manhal3["Séance"]))]

        manhal5 = pd.read_csv("https://docs.google.com/spreadsheets/d/1Ecdj4XNidyM7cykdN3SgGOBfcWslTQd1zUxwAnxVsqU"+linkc+"Repa_EvSc_Manhal_5aep")
        manhal5 = manhal5[["U", "S", "Eveil Scientifique", "Séance"]].dropna(axis=0)
        manhal5["Séance"] = [json.loads(manhal5["Séance"][i]) for i in range(len(manhal5["Séance"]))]
        manhal_manuel = [manhal1,manhal2,manhal3,manhal4,manhal5,manhal6]
        EvSc_manuels["المنهل"]=manhal_manuel

    #"""----Moufid----"""
    if manuel == "المفيد":
        es_moufid3 = es_moufid4 = es_moufid5 = es_moufid1 = pd.DataFrame()

        es_moufid2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1VcejNF4me-4DtCCyDi3o6TQe0C9GrUkO-jtE98r8lkQ"+linkc+"Repa_EvSc_Moufid_2aep")
        es_moufid2["Séance"] = [json.loads(es_moufid2["Séance"][i]) for i in range(len(es_moufid2["Séance"]))]

        es_moufid6 = pd.read_csv("https://docs.google.com/spreadsheets/d/16fjZLb5nYGlf7blJ1xLdBZL7ABProSyQ9ebJDdjQyDs"+linkc+"Repa_EvSc_Moufid_6aep")
        es_moufid6["Séance"] = [json.loads(es_moufid6["Séance"][i]) for i in range(len(es_moufid6["Séance"]))]

        es_moufid_manuel = [es_moufid1,es_moufid2,es_moufid3,es_moufid4,es_moufid5,es_moufid6]
        EvSc_manuels["المفيد"]=es_moufid_manuel

    #"""----Mounir----"""
    if manuel == "المنير":
        es_mounir1 = es_mounir2 = es_mounir3 = es_mounir6 = pd.DataFrame()

        es_mounir4 = pd.read_csv("https://docs.google.com/spreadsheets/d/1RX9M3ArHvnS6DSEuVG_FvaENqtCjP44G1KQVP4LlDy0"+linkc+"Repa_EvSc_Mounir_4aep")
        es_mounir4["Séance"] = [json.loads(es_mounir4["Séance"][i]) for i in range(len(es_mounir4["Séance"]))]

        es_mounir5 = pd.read_csv("https://docs.google.com/spreadsheets/d/1DE3EljplflalGIi5ncTYCa1G2FkHHCrH2oiW8G0jrJI"+linkc+"Repa_EvSc_Mounir_5aep")
        es_mounir5["Séance"] = [json.loads(es_mounir5["Séance"][i]) for i in range(len(es_mounir5["Séance"]))]
        es_mounir_manuel = [es_mounir1,es_mounir2,es_mounir3,es_mounir4,es_mounir5, es_mounir6]
        EvSc_manuels["المنير"]=es_mounir_manuel

    #"""----Wadih-----"""
    if manuel == "الواضح":
        es_wadih1= pd.read_csv("https://docs.google.com/spreadsheets/d/1GXpi5_SEc09vzLteRnzzRFupN9r5YClEFM9xs0VfOII"+linkc+"Repa_EvSc_Wadih_1aep")
        es_wadih1["Séance"] = [json.loads(es_wadih1["Séance"][i]) for i in range(len(es_wadih1["Séance"]))]

        es_wadih3= pd.read_csv("https://docs.google.com/spreadsheets/d/12Ul287wF9tJx7qhGmXhN7Ru4UP7lekFdFJYVafAyoXs"+linkc+"Repa_EvSc_Wadih_3aep")
        es_wadih3["Séance"] = [json.loads(es_wadih3["Séance"][i]) for i in range(len(es_wadih3["Séance"]))]

        es_wadih5 = pd.read_csv("https://docs.google.com/spreadsheets/d/1VE365OOkdjnrzZGSCR0LbUW5OMKBUEDdyTFPZb_td8g"+linkc+"Repa_EvSc_Wadih_5aep")
        es_wadih5["Séance"] = [json.loads(es_wadih5["Séance"][i]) for i in range(len(es_wadih5["Séance"]))]

        es_wadih2 =  es_wadih4 =  es_wadih6 = pd.DataFrame()
        es_wadih_manuel = [es_wadih1,es_wadih2,es_wadih3,es_wadih4,es_wadih5,es_wadih6]
        EvSc_manuels["الواضح"]=es_wadih_manuel

    #"""----Mourchid----"""
    if manuel == "المرشد":
        es_mourchid4 = pd.read_csv("https://docs.google.com/spreadsheets/d/1IT6WyFyRBJk49vjmw3dtfCljqDXpvNlyqj3ajBd498g"+linkc+"Repa_EvSc_Mourchid_4aep")
        es_mourchid4["Séance"] = [json.loads(es_mourchid4["Séance"][i]) for i in range(len(es_mourchid4["Séance"]))]

        es_mourchid1 = es_mourchid2 = es_mourchid3 = es_mourchid5 = es_mourchid6 = pd.DataFrame()
        es_mourchid_manuel = [es_mourchid1, es_mourchid2, es_mourchid3,es_mourchid4
                              ,es_mourchid5,es_mourchid6]
        EvSc_manuels["المرشد"]=es_mourchid_manuel

    #"""----Moukhtar----"""
    if manuel == "المختار":
        es_moukhtar1 =es_moukhtar3 = es_moukhtar4 = es_moukhtar5 = es_moukhtar6 = pd.DataFrame()
        es_moukhtar2 = pd.read_csv("https://docs.google.com/spreadsheets/d/1ILNnj6AIwLGXfbrtfOsYGrb4p9VsCmYmDJ7PeXuwfpY"+linkc+"Repa_EvSc_Mouhktar_2aep")
        es_moukhtar2["Séance"] = [json.loads(es_moukhtar2["Séance"][i]) for i in range(len(es_moukhtar2["Séance"]))]
        es_moukhtar_manuel = [es_moukhtar1, es_moukhtar2,es_moukhtar3,
                              es_moukhtar4,es_moukhtar5,es_moukhtar6]
        EvSc_manuels["المختار"] = es_moukhtar_manuel

    #"""----Attajdid----"""
    if manuel == "التجديد":
        es_tajdid1 = es_tajdid2 = es_tajdid3 = es_tajdid4 = es_tajdid5 = pd.DataFrame()

        es_tajdid6 = pd.read_csv("https://docs.google.com/spreadsheets/d/1adwmq-D2sc1JwcxaTFBUzT8hzOy5Rp0c7_dq_WMa5a8"+linkc+"Repa_EvSc_Attajdid_6aep")
        es_tajdid6["Séance"] = [json.loads(es_tajdid6["Séance"][i]) for i in range(len(es_tajdid6["Séance"]))]
        es_tajdid_manuel = [es_tajdid1,es_tajdid2,es_tajdid3,es_tajdid4,
                            es_tajdid5,es_tajdid6]
        EvSc_manuels["التجديد"] = es_tajdid_manuel

    try:
        if EvSc_manuels[str(manuel)][int(level) - 1].empty:
            return "Ce manuel n'est pas disponible pour ce niveau, choisissez un autre manuel!"

        else:

            return EvSc_manuels[str(manuel)][int(level) - 1]
    except:
        print("Ce manuel n'est pas disponible pour ce niveau, choisissez un autre manuel!")
        print("Remarque: le niveau doit être entre 1 et 6!")

@st.cache_resource()
# Ritual of lecture 
def rituel_lecture(manuel, level):
    
    if (manuel == "Mes rituels en lecture (Objectifs complets)") or (manuel == "Mes rituels en lecture (Objectifs résumés par IA)"):
        
        if level == 1:
            rituel_ = pd.read_csv("https://docs.google.com/spreadsheets/d/1R36mcDc8E2oBitaZ-6L1u5p_-evHEvyYiPvcxJdwsIY/gviz/tq?tqx=out:csv&sheet=Rituel_fr_1aep")
        if level == 2:
            rituel_ = pd.read_csv("https://docs.google.com/spreadsheets/d/1X0HZn_JR6PqA_dakApdqssGOhNb7uG_Bd_EzU3Kz1KQ/gviz/tq?tqx=out:csv&sheet=Rituel_fr_2aep")
        if level == 3:
            rituel_ = pd.read_csv("https://docs.google.com/spreadsheets/d/1oYzmmG7Q0qaEVm_pb1_Ewc0ZWLgQaO_DtmjntBwcDys/gviz/tq?tqx=out:csv&sheet=Rituel_fr_3aep")
            rituel_ = rituel_[["Jour","Semaine","Objectif","Objectif_Resume"]]
        if level == 4:
            rituel_ = pd.read_csv("https://docs.google.com/spreadsheets/d/183mIvzLuEbWCD-Y12DFrpTdhcaB5vCz4C1FE2nI69UY/gviz/tq?tqx=out:csv&sheet=Rituel_fr_4aep")
        if level == 5:
            rituel_ = pd.read_csv("https://docs.google.com/spreadsheets/d/1XBvsaVmkHkxQpWQfZt4JKE9k6ZQ4-lyHibRwR1L0mb0/gviz/tq?tqx=out:csv&sheet=Rituel_fr_5aep")
        if level == 6:
            rituel_ = pd.read_csv("https://docs.google.com/spreadsheets/d/1nKrhINMuy-uvgC1igDw7CzZ4ukdFGE1L1kFEoQOJ0QI/gviz/tq?tqx=out:csv&sheet=Rituel_fr_6aep")
        
        Total_Days = (rituel_['Semaine'] - 1) * 5 + rituel_['Jour']
        rituel_["U"]  = ((Total_Days - 1) // 25) + 1  
        rituel_["S"] = S = (rituel_['Semaine'] - 1) % 5 + 1 
        rituel_["S"] = [S[i] + 1 if S[i] == 0 else S[i] for i in range(len(S))]
        rituel_ = rituel_[["U","S","Semaine","Jour","Objectif","Objectif_Resume"]]
        return rituel_
    else :
        return None    

# 2 weeks for ED, 5 weeks for each Unit and 1 week for each EV ,pedagical_week=6 days
@st.cache_resource(show_spinner=False)
def U_W_D(fr_manuel1, fr_manuel2,lecture_rituel1, lecture_rituel2,math_manuel1, math_manuel2, es_manuel1, es_manuel2, C1, C2, séance_de_lundi, u):#,in_t,ou_t,rec_t,switch_t):
    global buffer
    buffer = BytesIO()
    emplois=st.session_state["emplois"]
    emplois.dropna(inplace=True)
    emplois.index = range(emplois.shape[0])
    emplois[["Séance", "Durée"]] = emplois[["Séance", "Durée"]].astype("int")
    emplois[["Matière", "Séance", "Durée"]] = emplois[["Matière", "Séance", "Durée"]].astype("str")

    #"""--------------------------------Reparations-------------------------------"""
    #Fr
    my_fr_class_1 = fr_manuel_level(manuel=fr_manuel1,level=C1)
    my_fr_class_2 = fr_manuel_level(manuel=fr_manuel2,level=C2)
    fr_class = [my_fr_class_1, my_fr_class_2]


    #Maths
    my_math_class_1 = maths_manuel_level(manuel=math_manuel1, level=C1)
    my_math_class_2 = maths_manuel_level(manuel=math_manuel2, level=C2)
    math_class = [my_math_class_1, my_math_class_2]

    #Eveil Scientifique
    my_EvSc_class_1 = EvSc_manuel_level(level=C1, manuel=es_manuel1)
    my_EvSc_class_2 = EvSc_manuel_level(level=C2, manuel=es_manuel2)
    EvSc_class = [my_EvSc_class_1, my_EvSc_class_2]

    #Rituel en lecture
    fr_rituel_class_1 = rituel_lecture(manuel=lecture_rituel1, level=C1)
    fr_rituel_class_2 = rituel_lecture(manuel=lecture_rituel2, level=C2)
    fr_rituel_class = [fr_rituel_class_1, fr_rituel_class_2]

    

    # """------------------Dates-----------------"""
    all_time = np.arange(dt.date(2024, 9, 3), dt.date(2025, 6, 20)).astype(datetime)
    holiday_list = pd.Series({
        "Mawlid_nabawi": [dt.date(2024, 10, 16), dt.date(2024, 10, 17)],
        "V1S1": np.arange(dt.date(2024, 10, 20), dt.date(2024, 10, 27)),
        "March_vert": [dt.date(2024, 11, 6)],
        "Aid_isstiklal": [dt.date(2024, 11, 18)],
        "V2S1": np.arange(dt.date(2024, 12, 8), dt.date(2024, 12, 15)),
        "Bonne_annee": [dt.date(2024, 1, 1)],
        "Watika_Isstiklala": [dt.date(2025, 1, 11)],
        "Amazigh_Day": [dt.date(2025, 1, 14)],
        "Middle_V": np.arange(dt.date(2025, 1, 26), dt.date(2025, 2, 2)),
        "V1S2": np.arange(dt.date(2025, 3, 16), dt.date(2025, 3, 22)),
        "Aid_Fiter": np.arange(dt.date(2025, 3, 31), dt.date(2025, 4, 1)),
        "V2S2": np.arange(dt.date(2025, 5, 4), dt.date(2024, 5, 11)),
        "Aid_Adha": [dt.date(2025, 6, 6), dt.date(2025, 6, 7)]
    })

    for i in range(len(holiday_list.values)):
        for j in range(len(holiday_list.values[i])):
            if holiday_list.values[i][j] in all_time:
                all_time = all_time[all_time != holiday_list.values[i][j]]

    No_wekends_all_dates = []
    for date in all_time:

        str_date = date.strftime("%A, %d %B, %Y")
        if ("Sunday" in str_date):
            day = "Weekend!"
        else:
            No_wekends_all_dates.append(date)

    # """------Units, Classes And Manuels------"""

    ED = No_wekends_all_dates[0:12]
    U1 = No_wekends_all_dates[12:42]
    U2 = No_wekends_all_dates[42:72]
    U3 = No_wekends_all_dates[72:102]

    EV_S1 = No_wekends_all_dates[102:108]

    U4 = No_wekends_all_dates[108:138]
    U5 = No_wekends_all_dates[138:168]
    U6 = No_wekends_all_dates[168:198]

    EV_S2 = No_wekends_all_dates[198:204]

    Unites = {"U1": U1, "U2": U2, "U3": U3, "U4": U4, "U5": U5, "U6": U6}
    unite = Unites[u]
    classes = [C1, C2]
    fr_manuels = [fr_manuel1, fr_manuel2]
    math_manuels = [math_manuel1, math_manuel2]
    es_manuels = [es_manuel1, es_manuel2]
    lecture_manuels = [lecture_rituel1, lecture_rituel2]

    #"""------Sheet Format preparation------"""
    align = Alignment(horizontal="center",
                      vertical="top",
                      wrapText=True)

    thin = Side(border_style="thin", color="4617F1")

    bord = Border(left=thin,
                  right=thin,
                  top=thin,
                  bottom=thin)
    font = Font(name="Lucida Handwriting",sz=12)

    weeks_days = []
    sheets = []
    wb = Workbook()
    ws = wb.active

    # initialize citations
    citations = pd.read_csv(r"https://docs.google.com/spreadsheets/d/1VJs8_Z3zsww-LaiMmMZAtcmUJKBqW7KsTmuGJtiCdyA"+linkc+"citations")
    random_list = random.sample(range(citations.shape[0]), citations.shape[0])
    citation = citations["Définition"] + "\n" + "source: " + citations["Source"]

    for k in range(len(unite)):
        sheets.append(wb.create_sheet(f'feuille {k}'))

    for i, date, sheet in zip(enumerate(unite), unite, sheets):
        date_list = format_datetime(date, 'full', locale='fr_FR').split()[0:4]
        str_date = " ".join(date_list).replace(",", " ")

        for cell in sheet["B4:H7"] + sheet["B8:G8"] :
            for x in cell:
                x.alignment = align
                x.border = bord

        sheet["F2"].border = bord
        sheet["F3"].border = bord

        for cell in sheet["B9:F9"]:
            for y in cell:
                y.border = bord
                y.alignment = Alignment(horizontal='left', vertical='top')

        for cell in sheet["B4:H4"] + sheet["B8:H8"]:
            for w in cell:
                w.fill = PatternFill("solid", "FFA500")
        sheet["B6"].fill = PatternFill("solid", "FFA500")

        for cell in sheet["B5:G5"] + sheet["B7:G7"]:
            for v in cell:
                v.font = font

        for cell in sheet["B5:C5"] + sheet["B7:C7"]:
            for c in cell:
                c.alignment = Alignment(horizontal="center",vertical="center",wrapText=True)


        sheet.column_dimensions["F"].width = 80

        sheet.column_dimensions["D"].width = 22
        sheet.column_dimensions["B"].width = 12
        for lettre in ["C", "E", "G", "H"]:
            sheet.column_dimensions[lettre].width = 8
            
        for row in [5, 7, 9]:
            sheet.row_dimensions[row].height = 130

        # citation
        sheet.merge_cells('B9:E9')
        sheet["B9"].alignment = Alignment(horizontal="left",vertical="top",wrapText=True)
        sheet["B9"].font = font
        sheet["B9"] = f"CITATION: {citation[random_list[i[0]]]}"

        # remarque
        # sheet.merge_cells('B9:E9')
        sheet["F9"] = "REMARQUES: "

        sheet.merge_cells('B6:H6')
        sheet["B6"] = "RECREATION"

        sheet.merge_cells('G8:H8')
        sheet["G8"] = f'Unité: {1 + list(Unites.values()).index(unite)}'

        sheet["F2"] = f'Date: ............................................... '#{str_date}'

        #----------------in and out time---------------------

        sheet["B4"] = "Temps"
        outmor_torec_t = inmor_t + ((outmor_t - inmor_t) - rec_t) / 2
        inmor_fromrec_t = outmor_torec_t + rec_t
        outeven_torec_t = ineven_t + ((outeven_t - ineven_t) - rec_t) / 2
        ineven_fromrec_t = outeven_torec_t + rec_t
        if séance_de_lundi == "Matinée":

            if date_list[0] in ["lundi", "mercredi", "samedi"]:

                sheet["B5"] = f'De\n\n {inmor_t}  à\n\n  {outmor_torec_t}'
                sheet["B7"] = f'De \n\n {inmor_fromrec_t}  à\n\n  {outmor_t}'

            else:

                sheet["B5"] = f'De\n\n {ineven_t}  à\n\n  {outeven_torec_t}'
                sheet["B7"] = f'De\n\n {ineven_fromrec_t}  à\n\n  {outeven_t}'
                
        else:
            
            if date_list[0] in ["mardi", "jeudi", "vendredi"]:
                sheet["B5"] = f'De\n\n  {inmor_t}  à\n\n {outmor_torec_t}'
                sheet["B7"] = f'De\n\n {inmor_fromrec_t}  à\n\n {outmor_t}'

            else:
                sheet["B5"] = f'De\n\n  {ineven_t}  à\n\n {outeven_torec_t}'
                sheet["B7"] = f'De\n\n {ineven_fromrec_t}  à\n\n {outeven_t}'

        # Discipline
        sheet["D4"] = "Discipline"

        # Classe
        sheet["C4"] = "Classe"

        # Maths
        def Maths_peda_class(niveau):
            my_class = math_class[niveau]
            if type(my_class) == pd.core.frame.DataFrame:
                maths_Unite_Repa = my_class[my_class["U"] == 1 + list(Unites.values()).index(unite)]
                maths_Week_Repa = maths_Unite_Repa[maths_Unite_Repa["S"] == 1 + int(i[0] / 6)]
                return (maths_Week_Repa)
            else:
                return my_class

        # Frensh
        def fr_peda_class(niveau):
            my_class =fr_class[niveau]
            if type(my_class) == pd.core.frame.DataFrame:
                fr_Unite_Repa = my_class[my_class["U"] == 1 + list(Unites.values()).index(unite)]
                fr_Week_Repa = fr_Unite_Repa[fr_Unite_Repa["S"] == 1 + int(i[0] / 6)]
                return (fr_Week_Repa)
            else:
                return my_class
                
        # Ritual of Lecture        
        def fr_rituel_peda_class(niveau):
            my_class = fr_rituel_class[niveau]
            if type(my_class) == pd.core.frame.DataFrame:
                fr_rituel_Unite_Repa = my_class[my_class["U"] == 1 + list(Unites.values()).index(unite) ]
                fr_rituel_Week_Repa = fr_rituel_Unite_Repa[fr_rituel_Unite_Repa["S"] ==  1 + int(i[0] / 6) ]
                return (fr_rituel_Week_Repa)
            else:
                return my_class

        # eveil scientifique:
        def EvSc_peda_class(niveau):
            my_class = EvSc_class[niveau]
            if type(my_class) == pd.core.frame.DataFrame:
                EvSc_Unite_Repa = my_class[my_class["U"] == 1 + list(Unites.values()).index(unite)]
                EvSc_Week_Repa = EvSc_Unite_Repa[EvSc_Unite_Repa["S"] == 1 + int(i[0] / 6)]
                return (EvSc_Week_Repa)
            else:
                return my_class
        rituel_lines = []
        def courses(niveau, matiéres_cell):
            global classe_emploi
            classe_emploi = emplois[emplois["Niveau"] == classes[niveau]]
            for peda_day in classe_emploi["Jour"]:

                if peda_day == (1 + len(weeks_days) % 6):
                    global jour_emploi
                    jour_emploi = classe_emploi[classe_emploi["Jour"] == peda_day]
                    sheet[matiéres_cell] = "".join([i+"\n\n\n" if i == "Rituel en lecture" else i+"\n" for i in jour_emploi["Matière"]]) #'\n'.join(jour_emploi["Matière"].to_list())
        
        def course_element(niveau, element_cell):
            courses_elements = []
            jour_emploi = classe_emploi[classe_emploi["Jour"] == 1 + len(weeks_days) % 6]
            emplois_week_Maths = classe_emploi[classe_emploi["Matière"] == "Maths"]
            emplois_week_EvSc = classe_emploi[classe_emploi["Matière"] == "Eveil Scientifique"]

            for course in jour_emploi["Matière"]:
                # FR
                fr_repa = fr_peda_class(niveau)
                if course in fr_repa.columns:
                    crs = fr_repa[course][1 + int(i[0] / 6)]
                    fr_repa[course] = "Ecrire en majiscule et en miniscule les lettres: "  + (fr_repa[course] if (course == "Ecriture / Copie") and (classes[niveau] == 4)  else fr_repa[course])
                    fr_repa[course] = "Ecrire :"  + (fr_repa[course] if (course == "Ecriture / Copie") and (classes[niveau] in [1,2,3]) else fr_repa[course])
                    courses_elements.append(crs)
                   
                # Rituel en lecture:
                if (course == "Rituel en lecture"):
                    fr_rituel_repa = fr_rituel_peda_class(niveau)
                    if lecture_manuels[niveau] == "Mes rituels en lecture (Objectifs complets)":
                        fr_rituel = fr_rituel_repa[fr_rituel_repa["Jour"] == 1 + int(i[0] / 6)]["Objectif"]
                        rituel = fr_rituel.to_list()[0] if fr_rituel.to_list() else "Rituel en lecture"
                        rituel = re.split(r'[.,]', rituel)
                        rituel = [rit for rit in rituel if rit != ''] 
                        rituel_lines.append(len(rituel) if rituel else 1 )
                        sheet["G9"] = len(rituel) if rituel else 1
                        courses_elements.append( "\n".join(rituel) if rituel else "")
                        
                    elif lecture_manuels[niveau] == "Mes rituels en lecture (Objectifs résumés par IA)":
                        fr_rituel = fr_rituel_repa[fr_rituel_repa["Jour"] == 1 + int(i[0] / 6) ]["Objectif_Resume"]
                        rituel = fr_rituel.to_list()[0]
                        rituel = re.split(r'[.,]', rituel)
                        rituel = [rit for rit in rituel if rit != '']
                        sheet["G9"] = len(rituel)
                        rituel_lines.append(len(rituel) if rituel else 1 )
                        courses_elements.append( "\n".join(rituel) if rituel else "")
                    else:
                        courses_elements.append("...................................................")    
                    
                # Maths
                math_repa = Maths_peda_class(niveau)
                if course in math_repa.columns:
                    emplois_jour_Maths = emplois_week_Maths[emplois_week_Maths["Jour"] == 1 + len(weeks_days) % 6]
                    seance = 6 if emplois_jour_Maths.empty else int(list(emplois_jour_Maths["Séance"])[0])
                    for s in list(math_repa["Séance"]):
                        if seance in s:
                            indices = math_repa[math_repa['Séance'].apply(lambda x: any(item in x for item in s))].index
                            courses_elements.append(math_repa["Maths"][indices[0]])

                # Eveil Scientifique:
                es_repa = EvSc_peda_class(niveau)
                if course in es_repa.columns:
                    emplois_jour_EvSc = emplois_week_EvSc[emplois_week_EvSc["Jour"] == 1 + len(weeks_days) % 6]
                    seance = 6 if emplois_jour_EvSc.empty else int(emplois_jour_EvSc["Séance"])
                    for s in list(es_repa["Séance"]):
                        if seance in s:
                            indices = es_repa[es_repa['Séance'].apply(lambda x: any(item in x for item in s))].index
                            courses_elements.append(es_repa["Eveil Scientifique"][indices[0]])
                if course in ["Act. rituelle","Amazigh & A.V.S","D.C.V","Rituel en maths"]:
                    courses_elements.append("...........................................................................")


            if "U. D / Thème" in fr_peda_class(niveau).columns:
                title = fr_peda_class(niveau)["U. D / Thème"][1 + int(i[0] / 6)]
            elif "Thème" in fr_peda_class(niveau).columns:
                title = fr_peda_class(niveau)["Thème"][1 + int(i[0] / 6)]
            else: title=""


            sheet["F3"] = f'Théme:  {title}'
            course_element = [str(cours_elem) for cours_elem in courses_elements]
            sheet[element_cell] = '\n'.join(course_element)
            
        sheet['H9'] = len(rituel_lines)
            
        def periode_seance(niveau, period_cell, seance_cell):
            for peda_day in classe_emploi["Jour"]:
                if peda_day == (1 + len(weeks_days) % 6):
                    global jour_emploi
                    jour_emploi = classe_emploi[classe_emploi["Jour"] == peda_day]
                    sheet[period_cell] = "".join([str(num) + 3*"\n"  if (num=="10")  and (i==2) else str(num)+"\n"  for i,num in enumerate(jour_emploi["Durée"].to_list())])#'\n'.join(jour_emploi["Durée"].to_list())
                    sheet[seance_cell] = "".join([str(num) + 3*"\n" if (i==2) else str(num)+"\n"  for i,num in enumerate(jour_emploi["Séance"].to_list())])#'\n'.join(jour_emploi["Séance"].to_list())
                    #(rituel_lines[0]*"\n" if rituel_lines[0] != 0 else "\n")
        if date_list[0] in ["lundi", "mercredi", "vendredi"]:

            sheet["C5"] = classes[0]
            courses(0, "D5") 
            periode_seance(0, "E5", "G5")
            course_element(0, "F5")

            sheet["C7"] = classes[1]
            courses(1, "D7")
            periode_seance(1, "E7", "G7")
            course_element(1, "F7")


        else:
            sheet["C5"] = classes[1]
            courses(1, "D5")
            periode_seance(1, "E5", "G5")
            course_element(1, "F5")

            sheet["C7"] = classes[0]
            courses(0, "D7")
            periode_seance(0, "E7", "G7")
            course_element(0, "F7")


        # Théme

        # Durée
        sheet["E4"] = "Durée"

        # Elements du cours
        sheet["F4"] = "Elements du cours (Intitulé / Objectifs / Etapes..)"

        # Nombre de Séance
        sheet["G4"] = "Séance"

        # Nombre de fiche
        sheet["H4"] = "Fiche"

        # Smaine
        sheet["F8"] = f'Semaine: {1 + int(i[0] / 6)}'
        # Jour
        sheet.merge_cells('B8:E8')
        sheet["B8"] = f'Jour: {1 + len(weeks_days) % 6}'
        weeks_days.append(i[0])


    def autofit_columns_and_rows(sheet):
        
        """
        Adjusts column width based on the longest content in each column.
        Adjusts row height based on the number of line breaks in a cell.
        """
        for col in sheet.columns:
            max_length = 0
            col_letter = get_column_letter(col[0].column)
            
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            
            sheet.column_dimensions[col_letter].width = max_length + 2  # Add padding
        
        for row in sheet.iter_rows():
            max_height = 15  # Default row height
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    lines = cell.value.count("\n") + 1  # Count line breaks
                    max_height = max(max_height, lines * 15)  # Approximate row height
            
            sheet.row_dimensions[row[0].row].height = max_height
    #for sheet in sheets:
     #   autofit_columns_and_rows(sheet = sheet)
    wb.save(buffer)
    return buffer

# """---------------------LOGIN----------------------------"""
secrets_auth = st.secrets["google_sheets_api_credentials"]
secrets_auth = secrets_auth
smtp_gmail_ = st.secrets.smtp_gmail
smtp_password_ = st.secrets.smtp_password
def login():
    title_placeholder = st.empty()
    title_placeholder.subheader("S'enregistrer")
    __login__obj = __login__(credentials = secrets_auth,
                        smtp_username = smtp_gmail_,
                        smtp_password = smtp_password_,
                        company_name = "Moudakira.ma",
                        width = 200, height = 300,
                        logout_button_name = 'Sortir', hide_menu_bool = False,
                        hide_footer_bool = False,
                        lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')
    LOGGED_IN = __login__obj.build_login_ui()
    if  LOGGED_IN:
        title_placeholder.empty()
        
    return LOGGED_IN
    
if "LOGGED_IN" not in st.session_state:
    st.session_state["LOGGED_IN"] = False

if not st.session_state["LOGGED_IN"]:
    with st.container(border=True):
        if __name__ == "__main__":
            login()
            st.info(
                "Si vous n'avez pas un compte, Veuillez cliquer sur ***Créer un compte*** dans la barre de navigation pour créer un.",
                icon="ℹ️")
else :
    login()
        
    # """"----------------Streamlit App-----------------"""
    st.title("Le Cahier des Leçons Journalières ")
    st.empty()


    french_dispo_manuels1 = ["Faire Dire","","",""]
    french_dispo_manuels2 = ["Mes apprentissages", "Espace de l'école", "L'oasis des mots", "Nouvel espace"]
    french_dispo_manuels3 = ["Mes apprentissages", "L'oasis des mots","",""]
    french_dispo_manuels4 = ["Mes apprentissages","Nouvel espace","",""]
    french_dispo_manuels5 = ["Mes apprentissages", "Pour communiquer","",""]
    french_dispo_manuels6 = ["Mes apprentissages", "Parcours français","",""]
    # Create a DataFrame
    french_dispo_manuels=pd.DataFrame( {
        'Niveau 1': french_dispo_manuels1,
        'Niveau 2': french_dispo_manuels2,
        'Niveau 3': french_dispo_manuels3,
        'Niveau 4': french_dispo_manuels4,
        'Niveau 5': french_dispo_manuels5,
        'Niveau 6': french_dispo_manuels6 })

    #Maths available manuels
    Maths_dispo_manuels1 = ["المفيد","الفضاء",""]
    Maths_dispo_manuels2 = ["الجيد","الفضاء","المرجع"]
    Maths_dispo_manuels3 = ["","الفضاء","المرجع"]
    Maths_dispo_manuels4 = ["الجيد","المفيد",""]
    Maths_dispo_manuels5 = ["المفيد","النجاح",""]
    Maths_dispo_manuels6 = ["الجيد","الجديد",""]
    Maths_dispo_manuels = pd.DataFrame({
                                    'Niveau 1':Maths_dispo_manuels1,
                                    'Niveau 2':Maths_dispo_manuels2,
                                    'Niveau 3':Maths_dispo_manuels3,
                                    'Niveau 4':Maths_dispo_manuels4,
                                    'Niveau 5':Maths_dispo_manuels5,
                                    'Niveau 6':Maths_dispo_manuels6,
                                     })
    #EvSc available manules

    EvSc_available_manules1 = ['الجديد', 'الفضاء', 'الواضح']
    EvSc_available_manules2 = ['المفيد','المختار',""]
    EvSc_available_manules3 = ['المنهل', 'الواضح',""]
    EvSc_available_manules4 = ['الفضاء', 'المنير', 'المرشد']
    EvSc_available_manules5 = ['المنهل', 'المنير', 'الواضح']
    EvSc_available_manules6 = ['الفضاء', 'المفيد', 'التجديد']

    EvSc_available_manules = pd.DataFrame({
        'Niveau 1' : EvSc_available_manules1 ,
        'Niveau 2' : EvSc_available_manules2 ,
        'Niveau 3' : EvSc_available_manules3 ,
        'Niveau 4' : EvSc_available_manules4 ,
        'Niveau 5' : EvSc_available_manules5 ,
        'Niveau 6' :EvSc_available_manules6
                                           })

    # Select Teaching Language
    col1,col2=st.columns([0.8, 0.2])
    form = col1.form(key="my_form")


    teaching_language = form.selectbox("Sélectionez la langue ", ["Français"],
                                       placeholder="choisissez une option",index=None)

    next = form.form_submit_button("Cliquez pour choisir les niveaux ou les groupes")


    # Define function to select options
    # Select Manual Names
    if (teaching_language == "Français"):
        # Select Levels
        level1 = form.multiselect(
            "Veuillez choisir le premier groupe ou niveau que vous accueillerez pendant la séance de lundi.",
            [1,2,3,4,5,6], max_selections=1,key="level1")

        level2 = form.multiselect(
            "Veuillez choisir le deuxieme groupe ou niveau que vous accueillerez pendant la séance de lundi.",
            [1,2,3,4,5,6], max_selections=1,key="leve2")
        
        form.form_submit_button(label="Cliquez pour choisir les manuels")
        selected_manuels = []

        if (len(level1) != 0) and (len(level2) != 0):
        
            # disponible manuels:
            st.write("Les manuels de français disponibles: ")
            st.table(french_dispo_manuels)
            st.write("Les manuels de Maths disponibles: ")
            st.table(Maths_dispo_manuels)
            st.write("Les manuels d'eveil scientifique disponibles: ")
            st.table(EvSc_available_manules)
            st.write("Le manuel de rituel en lecture disponible pour tous les niveaux est: Mes Rituels En Lecture.")

            # French
            french_manual_name1 = form.multiselect(f"Choisissez le manuel de français pour le niveau:{level1[0]}",
                                                   [i for i in french_dispo_manuels1 if i != ""] if level1[0] == 1
                                                   else [i for i in french_dispo_manuels2 if i != ""] if level1[0] == 2
                                                   else [i for i in french_dispo_manuels3 if i != ""] if level1[0] == 3
                                                   else [i for i in french_dispo_manuels4 if i != ""] if level1[0] == 4
                                                   else [i for i in french_dispo_manuels5 if i != ""] if level1[0] == 5
                                                   else [i for i in french_dispo_manuels6 if i != ""] if level1[0] == 6
                                                   else [None]
                                                   ,key="fr1", max_selections=1)
            french_manual_name2 = form.multiselect(f"Choisissez le manuel de français pour le niveau:{level2[0]}",
                                                   [i for i in french_dispo_manuels1 if i != ""] if level2[0] == 1
                                                   else [i for i in french_dispo_manuels2 if i != ""] if level2[0] == 2
                                                   else [i for i in french_dispo_manuels3 if i != ""] if level2[0] == 3
                                                   else [i for i in french_dispo_manuels4 if i != ""] if level2[0] == 4
                                                   else [i for i in french_dispo_manuels5 if i != ""] if level2[0] == 5
                                                   else [i for i in french_dispo_manuels6 if i != ""] if level2[0] == 6
                                                   else [None],
                                                   key="fr2", max_selections=1)
            
            fr_rituel_manual_name1 = form.multiselect(f"Choisissez le manuel de rituel en lecture pour les niveaux: {level1[0]} ",
                                                     ["Mes rituels en lecture (Objectifs complets)",
                                                      "Mes rituels en lecture (Objectifs résumés par IA)",
                                                      "rituels personalisés(un espace sera disponible pour ajouter vos rituels.)"],
                                                     key = "lecture_rituel1",
                                                     max_selections=1)
            fr_rituel_manual_name2 =  fr_rituel_manual_name1 #form.multiselect(f"Choisissez le manuel de rituel en lecture pour les niveaux: {level2[0]} ",
                                                    # ["Mes rituels en lecture (Objectifs complets)",
                                                    # "Mes rituels en lecture (Objectifs résumés par IA)",
                                                    #  "rituels personalisés(un espace sera disponible pour ajouter vos rituels.)"],
                                                    # key = "lecture_rituel2",
                                                    # max_selections=1)
           

            # Maths
            maths_manual_name1 = form.multiselect(f"Choisissez le manuel de maths pour le niveau: {level1[0]}",
                                                  [i for i in Maths_dispo_manuels1 if i != ""] if level1[0] == 1
                                                  else [i for i in Maths_dispo_manuels2 if i != ""] if level1[0] == 2
                                                  else [i for i in Maths_dispo_manuels3 if i != ""] if level1[0] == 3
                                                  else [i for i in Maths_dispo_manuels4 if i != ""] if level1[0] == 4
                                                  else [i for i in Maths_dispo_manuels5 if i != ""] if level1[0] == 5
                                                  else [i for i in Maths_dispo_manuels6 if i != ""] if level1[0] == 6
                                                  else [None],
                                                  key="math1", max_selections=1)

            maths_manual_name2 = form.multiselect(f"Choisissez le manuel de maths pour le niveau: {level2[0]}",
                                                  [i for i in Maths_dispo_manuels1 if i != ""] if level2[0] == 1
                                                  else [i for i in Maths_dispo_manuels2 if i != ""] if level2[0] == 2
                                                  else [i for i in Maths_dispo_manuels3 if i != ""] if level2[0] == 3
                                                  else [i for i in Maths_dispo_manuels4 if i != ""] if level2[0] == 4
                                                  else [i for i in Maths_dispo_manuels5 if i != ""] if level2[0] == 5
                                                  else [i for i in Maths_dispo_manuels6 if i != ""] if level2[0] == 6
                                                  else [None],
                                                  key="math2", max_selections=1)

            # Act. Sc.
            act_sc_manual_name1 = form.multiselect(f"Choisissez le manuel d'éveil scientifique pour le niveau:{level1[0]}",
                                                   [i for i in EvSc_available_manules1 if i !=""] if level1[0] == 1
                                                   else [i for i in EvSc_available_manules2 if i !=""] if level1[0] == 2
                                                   else [i for i in EvSc_available_manules3 if i !=""] if level1[0] == 3
                                                   else [i for i in EvSc_available_manules4 if i !=""] if level1[0] == 4
                                                   else [i for i in EvSc_available_manules5 if i !=""] if level1[0] == 5
                                                   else [i for i in EvSc_available_manules6 if i !=""] if level1[0] == 6
                                                   else [None],
                                                   key="evsc1", max_selections=1)

            act_sc_manual_name2 = form.multiselect(f"Choisissez le manuel d'éveil scientifique pour le niveau:{level2[0]}",
                                                   [i for i in EvSc_available_manules1 if i !=""] if level2[0] == 1
                                                   else [i for i in EvSc_available_manules2 if i !=""] if level2[0] == 2
                                                   else [i for i in EvSc_available_manules3 if i !=""] if level2[0] == 3
                                                   else [i for i in EvSc_available_manules4 if i !=""] if level2[0] == 4
                                                   else [i for i in EvSc_available_manules5 if i !=""] if level2[0] == 5
                                                   else [i for i in EvSc_available_manules6 if i !=""] if level2[0] == 6
                                                   else [None],
                                                   key="evsc2", max_selections=1)
            # Select Period
            period = form.selectbox("sélectionnez la séance de Lundi", ["Matinée", "Après midi"])

            # Select Unit, all U if user payed else U1
            @st.cache_resource(show_spinner=False)
            def worksheet(_credentials):

                scope = ["https://www.googleapis.com/auth/spreadsheets",
                         "https://www.googleapis.com/auth/drive"]
                Worksheet = ServiceAccountCredentials.from_json_keyfile_dict(_credentials, scope)
                client = gspread.authorize(Worksheet)
                sheet = client.open("mydb").sheet1
                return sheet

            secrets_auth = st.secrets["google_sheets_api_credentials"]
            secrets_auth_ = secrets_auth
            sheet = worksheet(_credentials = secrets_auth_)
            users = pd.DataFrame(sheet.get_values(), columns=sheet.get_values()[0]).drop(index=0)
            codes = users.code.to_list()
            codes = [code for code in codes if code != '']

            code = form.text_input("Si vous voulez choisir d'autre unité, entrez votre code ici :",
                                 placeholder="Entrez votre code")
            if code in codes:
                form.success("Félicitation! vous pouvez maintenant choisir parmi toutes les unités.")
                #st.balloons()
            elif code =="" : form.info("NB: La première unité U1 est gratuite.")
            else : form.warning("Le code enregistré est invalide!")
            form.form_submit_button("Confirmez")

            unit = form.multiselect("sélectionnez l'unitè", ["U1", "U2", "U3", "U4", "U5", "U6"] if code in codes else ["U1"],
                                    max_selections=1, default=["U1"])
            # select enter time on the morning
            inmor_t = form.time_input("Sélectionnez l'heure d'entrée au matin", dt.time(hour=9, minute=0),
                                    key="inmor_t",step=dt.timedelta(minutes=5))
            inmor_t = dt.timedelta(hours=inmor_t.hour, minutes=inmor_t.minute)
            # select the out time on the morning
            outmor_t = form.time_input("sélectionnez l'heure de sortie au matin", dt.time(hour=13, minute=30),
                                     key="outmor_t",step=dt.timedelta(minutes=5))
            outmor_t = dt.timedelta(hours=outmor_t.hour,minutes=outmor_t.minute)
            # select the in time on the evening
            ineven_t = form.time_input("Sélectionnez l'heure d'entrée au soir", dt.time(hour=13, minute=40),
                                     key="ineven_t",step=dt.timedelta(minutes=5))
            ineven_t = dt.timedelta(hours=ineven_t.hour, minutes=ineven_t.minute)
            # select the out time on the evening
            outeven_t =  form.time_input("Sélectionnez l'heure de sortie au soir", dt.time(hour=18, minute=30),
                                       key="outeven_t",step=dt.timedelta(minutes=5))
            outeven_t = dt.timedelta(hours=outeven_t.hour, minutes=outeven_t.minute)
            # select the recreation time
            rec_t = form.time_input("Sélectionnez la durée de la rècreation:",dt.time(minute=10),
                                    key= "rec_t",step=dt.timedelta(minutes=1))
            rec_t = dt.timedelta(minutes=rec_t.minute)

            enregistre = form.form_submit_button("Enregistrez!")

            options = [french_manual_name1, french_manual_name2,
                       maths_manual_name1, maths_manual_name2,
                       act_sc_manual_name1, act_sc_manual_name2]
            if all(len(val) != 0 for val in options) and (enregistre == True):
                

                selected_manuels.extend([level1, level2, french_manual_name1, french_manual_name2, fr_rituel_manual_name1,
                                         maths_manual_name1, maths_manual_name2,
                                         act_sc_manual_name1, act_sc_manual_name2])

            #if all(str(value[0]) in dispo_manuels for value in selected_manuels):
                # """"-------------Emplois Du Temps-----------""""
                if "emplois" in st.session_state:
                    emplois = st.session_state["emplois"]
                    emplois.dropna(inplace=True)
                    emplois.index = range(emplois.shape[0])
                    emplois[["Séance", "Durée"]] = emplois[["Séance", "Durée"]].astype("int")
                    emplois[["Matière", "Séance", "Durée"]] = emplois[["Matière", "Séance", "Durée"]].astype("str")
                    modal_title = "Veuillez patienter!"
                    modal = Modal(key="modal001",title=modal_title)
                    with modal.container():
                        with st.spinner("La création de votre cahier journal est en cours...    استغفر الله"):
                            
    
                            journal = U_W_D(
                                  fr_manuel1 = french_manual_name1[0],
                                  fr_manuel2 = french_manual_name2[0],
                                  lecture_rituel1 = fr_rituel_manual_name1[0],
                                  lecture_rituel2 = fr_rituel_manual_name2[0],
                                  math_manuel1 = maths_manual_name1[0],
                                  math_manuel2 = maths_manual_name2[0],
                                  es_manuel1 = act_sc_manual_name1[0],
                                  es_manuel2 = act_sc_manual_name2[0],
                                  C1 = level1[0],
                                  C2 = level2[0],
                                  séance_de_lundi = period,
                                  u = unit[0],
                                  )
                            st.success("Votre cahier journal a été crèer avec succès! ")
                            download = st.download_button(
                                   label="Téléchargez votre cahier journal",
                                   data=journal,
                                   key="workbook.xlsx",
                                   file_name=f"Cahier_Journalier_{unit[0]}_niveaux {level1[0]}-{level2[0]}_{period}.xlsx",
                                    )
                else:
                    modal_title = "Pas d'emplois!"
                    modal = Modal(key="modal002", title=modal_title, padding=10, max_width=400)
                    with modal.container():
                        st.warning("Veuillez d'abord importer ou créer votre emplois!")
                    #st.warning("Veuillez importez ou créer votre emplois d'abord!")
            elif all(len(val) == 0 for val in options) and (enregistre == False):
                st.warning("Veuillez sélectionner toutes les options!")



components.html(
    """
     <script>
    // Modify the decoration on top to reuse as a bannerimport streamlit.components.v1 as components


    // Locate elements
    var sidebar = window.parent.document.querySelectorAll('[data-testid="stSidebar"]')[0];
    var decoration = window.parent.document.querySelectorAll('[data-testid="stDecoration"]')[0];

    // Observe sidebar size
    function outputsize() {
        decoration.style.left = `${sidebar.offsetWidth}px`;
    }

    new ResizeObserver(outputsize).observe(sidebar);

    // Adjust sizes
    outputsize();
    decoration.style.height = "4.0rem";
    decoration.style.right = "55px";

    // Adjust image decorations
    // https://drive.google.com/uc?export=view&id=1MrUbzDZv9v2kBppQApn_y543LUlisYOm
    decoration.style.backgroundImage = "url(https://drive.google.com/uc?export=view&id=1xeNVW7CPhPgTxHmSv7zd3cF7fe7MViQk)";
    decoration.style.backgroundSize = "contain";
    decoration.style.backgroundRepeat = "no-repeat";
    decoration.style.backgroundPosition = "center";
    decoration.style.zIndex = "1"; 
    </script>        
    """, width=0, height=0)



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
        <p> tous droits réservés © 2025 </p>

    </div>
"""

st.markdown(footer,unsafe_allow_html=True)
st.markdown(Hid_Menu,unsafe_allow_html=True)
