import sys,os,shutil, pathlib,json,gspread,smtplib,toml,re,sys
import streamlit as st
import pandas as pd 
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_signin_auth_ui.widgets import __login__
from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import streamlit.components.v1 as components
from streamlit_extras.app_logo import add_logo


# page configue
st.set_page_config(page_icon="static/moudkira_dark_v_100_100.png",
    page_title="Abonnement")
add_logo("static/moudkira_dark_v_100_100.png",height=80)




# Get absolute path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "static")


if "all_images" not in st.session_state:
  st.session_state["all_images"] = None
  
@st.cache_resource
def preload_images():
    """Load all images from the 'images' folder into memory once."""
    image_dict = {}
    for file in os.listdir(IMAGES_DIR):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            path = os.path.join(IMAGES_DIR, file)
            image_dict[file] = Image.open(path)
    return image_dict

# Load all images into memory before rendering anything
#all_images = preload_images()


  
#st.session_state["all_images"] = all_images


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
    
# load  google sheets api credentials from environment
title_placeholder = st.empty()
secrets_auth = os.getenv("google_sheets_api_credentials","{}")
secrets_auth = json.loads(secrets_auth)
smtp_gmail = os.getenv("smtp_gmail","")
smtp_password = os.getenv("smtp_password","")  

#open prospect sheet
@st.cache_resource(show_spinner=False)
def worksheet(_credentials):
  scope = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
  Worksheet = ServiceAccountCredentials.from_json_keyfile_dict(_credentials, scope)
  client = gspread.authorize(Worksheet)
  sheet = client.open("mydb").worksheets()[2]
  return sheet

sheet = worksheet(_credentials = secrets_auth)

if "LOGOUT_BUTTON_HIT" not in st.session_state:
    st.session_state["LOGOUT_BUTTON_HIT"] = False
def do_login():
    __login__obj = __login__(
        credentials=secrets_auth,
        smtp_username=smtp_gmail,
        smtp_password=smtp_password,
        company_name="Moudakira.ma",
        width=200,
        height=300,
        logout_button_name='Se déconnecter',
        hide_menu_bool=False,
        hide_footer_bool=False,
        lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
    )

    username = __login__obj.get_username()
    LOGGED_IN = __login__obj.build_login_ui()
    return LOGGED_IN, username
    # Initialize session state if not set
if "LOGGED_IN" not in st.session_state:
    st.session_state["LOGGED_IN"] = False

# Only try login if not logged in
if not st.session_state["LOGGED_IN"]:
    st.info(
        "Si vous n'avez pas un compte, veuillez cliquer sur ***Créer un compte*** "
        "dans la barre de navigation pour créer un.",
        icon="ℹ️"
    )
    title_placeholder = st.empty()
    title_placeholder.subheader("Se connecter")
    LOGGED_IN, _ = do_login()
else:
    title_placeholder.subheader("Choisissez votre plan et simplifiez votre année scolaire.")
    _ , username = do_login()



    # Session state initialization
    if "verification_code" not in st.session_state:
        st.session_state.verification_code = None
    if "email_verified" not in st.session_state:
        st.session_state.email_verified = False
        
    if ("submitted1" and "submitted2" not in st.session_state):
        st.session_state["submitted1"] = False
        st.session_state["submitted2"] = False

    
    def body_message(verification_code):
        body_html = """ <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Code de vérification</title>
                <style>
                    body {
                        font-family: sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                    }
                    .container {
                        background-color: #ffffff;
                        padding: 40px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        text-align: center;
                        width: 90%;
                        max-width: 600px;
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 20px;
                    }
                    p {
                        color: #555;
                        line-height: 1.6;
                        margin-bottom: 25px;
                    }
                    .verification-code {
                        background-color: #e9ecef;
                        color: #28a745;
                        font-size: 24px;
                        font-weight: bold;
                        padding: 15px 30px;
                        border-radius: 6px;
                        margin-bottom: 30px;
                        display: inline-block;
                    }
                    .button {
                        display: inline-block;
                        background-color: #007bff;
                        color: white;
                        padding: 12px 25px;
                        text-decoration: none;
                        border-radius: 6px;
                        margin-top: 20px;
                    }
                    .button:hover {
                        background-color: #0056b3;
                    }
                    .footer {
                        margin-top: 40px;
                        font-size: 12px;
                        color: #777;
                    }
                </style>
            </head>
                <body>
                    <div class="container">
                        <h1>Vérifiez votre adresse e-mail</h1>
                        <p>Merci de nous contacter! Pour vérifier votre émail, veuillez utiliser le code de vérification ci-dessous :</p>
                        <div class="verification-code">
                            """+f"""{verification_code}"""+"""
                        </div>
                        <p>Veuillez saisir ce code sur la page de vérification.Il expirera  dans 24 heurs.</p>
                        <p>Si vous n'avez pas demandé cette vérification, veuillez ignorer cet e-mail.</p>
                        <div class="footer">
                            <p>Ceci est un e-mail généré automatiquement. Veuillez ne pas répondre à ce message.</p>
                            <p>&copy; Moudakira.ma - 2025</p>
                        </div>
                    </div>
                </body>
            </html>"""
        return body_html
    
    
    
    def send_email_ssl(sender_email, sender_password, receiver_email, subject, body):
      """Sends an email using SMTP.
    
      Args:
        sender_email: The sender's email address.
        sender_password: The sender's email password.
        receiver_email: The receiver's email address.
        subject: The email subject.
        body: The email body (can be HTML).
      """
      msg = MIMEText(body, 'html')  # Set the subtype to 'html'
      msg['Subject'] = subject
      msg['From'] = sender_email
      msg['To'] = receiver_email
    
      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email,
                   sender_password)
        smtp.send_message(msg)
    
    
    
    # Show columns only if form is not submitted
    if (not st.session_state["submitted1"] and not st.session_state["submitted2"]):
        st.title("Plans d'inscription")
    
        col1, col2 = st.columns([0.5, 0.5])
        
        form1 = col1.form(key="transfer")


        form1.header("🔑 Code Clé Pédagogique")

        form1.write(
                "Obtenez un code unique qui débloque l’accès à **toutes les unités pédagogiques de l’année** "
                "(Français, Mathématiques, Activités Scientifiques). "
                "Téléchargez votre cahier journalier en quelques minutes, prêts à être modifiés et imprimés."
            )
        
        #form1.image(all_images["pay_for_code.png"])
        form1.image("static/pay_for_code.webp")

        for i in range (10):
            form1.write("  ")
            
        form1.success("✅ Accès immédiat – Seulement **49 DH** pour toute l’année !")
        submit1 = form1.form_submit_button("👉 Je choisis ce plan")
        
        form2 = col2.form(key="delivery")
        
        form2.header("🎯 Satisfait ou rien à payer !")

        text = (
            "Nous préparons votre cahier journal personnalisé selon vos besoins. "
            "Vous le visualisez d’abord gratuitement, nous ajustons selon vos retours, "
            "et **vous ne payez que si vous êtes satisfait**. "
            "Après validation, vous recevez votre cahier complet par e-mail ou WhatsApp.")
        form2.write(text)
        
        #form2.image(all_images["satisfaid_then_pay.png"])
        form2.image("static/satisfaid_then_pay.webp")

        
        form2.success("💡 Garantie de satisfaction – Seulement **99 DH** !")
        
        submit2 = form2.form_submit_button("👉 Je choisis ce plan")

        # If either form is submitted, update session state and rerun
        if submit1 :
            st.session_state["submitted1"] = True
            st.rerun()
        if submit2:
            st.session_state["submitted2"] = True
            st.rerun()
    
    # Display new content after submission 1
    if st.session_state["submitted1"]:
        st.write("### Veuillez effectuer un virement de **49 DH** sur le numéro de compte ou scanner le QR code.")
        st.info("**Banque**: Attijariwafa Bank \n\n"
                "**Numéro de compte : 007194000702200030726337**")
        col1,col2 = st.columns(2)
        #col1.image(all_images["attijari_logo_resized.png"])#,use_container_width="auto")
        col1.image("static/attijari_logo_resized.webp")
        col2.image("static/account_qrcode.webp")
        #col2.image(all_images["account_qrcode.jpeg"])
        st.write("Veuillez envoyez un justificatif de votre payment sur l'e-mail suivant: **moudakira.ma@gmail.com** "
                 "ou sur le Whatsapp suivant: **https://wa.me/+212667313488**,"
                 " Après une vérification, vous recevrez ***un code*** pour débloquer toutes les unités.")
    
        if st.button("← Retour"):
            st.session_state["submitted1"] = False
            st.rerun()
    
    # Display new content after submission 2
    if st.session_state["submitted2"]:
        with st.form(key="sub2"):
            st.write("### Veuillez remplir le formulaire ci-dessus:")
            family_name = st.text_input("***Votre nom***:")
            first_name = st.text_input("***Votre prénom***:")
            gmail = st.text_input("***Votre gmail***:",placeholder="nom.prenom@gmail.com")
            phone_number = st.text_input("***Votre numéro  de téléphone***:",value="0611111111",)
            if not re.match(r"^0[1-9]\d{8}$",str(phone_number) ):
                st.warning("Le fromat de votre numéro de téléphone est incorrect!")
            
            teaching_lng = st.multiselect("***La matiére que vous enseignez***:",["Français","Arabe"])
            teaching_class = st.multiselect("***Le(s) niveau(x) que vous enseignez***:",range(1,6),)
            continue_btn = st.form_submit_button("Continue")
            
        if continue_btn:
            if all([family_name, first_name, gmail, phone_number]):
                # Generate and send email
                verification_code = str(np.random.randint(10000, 99999))
                try:
                    # send verification code to the user to verify his gmail
                    send_email_ssl(sender_email =  smtp_gmail,
                                   sender_password =smtp_password,
                                   receiver_email = gmail,
                                   subject="Vérification de votre adresse e-mail",
                                   body = body_message(verification_code = verification_code )
                                  )
                    
                    st.session_state.verification_code = verification_code
                    st.success("Un email a été envoyé avec le code de vérification.")
                    
                except: st.warning("Votre gmail est incorrect.")
                
            else:
                st.warning("Veuillez remplir tous les champs.")
        # Verification code input (outside the form)
        if st.session_state.verification_code:
            code_input = st.text_input("Veuillez saisir le code de vérification reçu par email:")
    
            if st.button("Vérifier"):
                if code_input == st.session_state.verification_code:
                    st.session_state.email_verified = True
                    st.success("Votre email est bien vérifié!")
                else:
                    st.warning("Code de vérification incorrect.")
    
        if st.session_state.email_verified:
            if st.button("Enregistrer"):
                try:
                    # Add prospect data to the database (google sheet)
                    sheet.append_row(
                                     [family_name, first_name, gmail, phone_number,
                                      ' et '.join(str(num) for num in teaching_lng),
                                      ' et '.join(str(num) for num in teaching_class)]
                                     )
                    st.info("***Votre demande a été bien enregistrée! Nous vous contacterons dans les plus brefs délais.***")
                    
                    # Send notification to the owner
                    send_email_ssl ( sender_email =  smtp_gmail,
                                     sender_password =smtp_password, 
                                     receiver_email = smtp_gmail,
                                     subject="Un nouveau prospecte est ajouté!",
                                     body =" Tu as une nouvelle demande de cahier journalier sur Moudakira.ma." )
                    
                    # Send successeful enregitrement message to the prospect  
                    send_email_ssl(sender_email =  smtp_gmail,
                                   sender_password =smtp_password, 
                                   receiver_email = gmail,
                                   subject="Votre demande a été bien enregistrée!",
                                   body = """ 
                                                    <h1>Bonjour """+f"""{first_name}"""+"""</h1>
                                                    <p>Votre demande a été bien enregistrée! Nous vous contacterons dans les plus brefs délais :</p>
                                                    <p>Si vous n'avez pas demander un abonnement sur moudakira.ma, veuillez ignorer cet e-mail.</p>
                                                    <div class="footer">
                                                        <p>Ceci est un e-mail généré automatiquement. Veuillez ne pas répondre à ce message.</p>
                                                        <p>&copy; Moudakira.ma - 2025</p>
                                                    </div>"""
                                 )
                except: 
                    st.warning("Une erreur est survenue lors de l'enregistrement de vos données. Veuillez réessayer ultérieurement.")
                
        st.empty()
        for i in range(5): st.write("  ") 
           
        if st.button("← Retour"):
            st.session_state["submitted2"] = False
            st.rerun()
    
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

st.markdown(footer,
            unsafe_allow_html=True)
st.markdown(Hid_Menu,
            unsafe_allow_html=True)
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    








