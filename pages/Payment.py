import sys
import streamlit as st
import pandas as pd 
import numpy as np
import gspread,smtplib,toml,re,sys
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from email.mime.text import MIMEText
import streamlit.components.v1 as components
#from streamlit_extras.app_logo import add_logo


# page configue
st.set_page_config(page_icon="app-images/Moudkira_dark_v_100_100.png",
    page_title="Abonnement")


#add_logo("app-images/Moudkira_dark_v_100_100.png",height=80)


# load  google sheets api credentials (temporary method)
with open(r"C:\Users\hp\PycharmProjects\Streamlitt_App\credentials.toml","r+") as cred:
    credentials = toml.load(cred)
    
# load  google sheets api credentials from secrets
#secrets_auth = st.secrets["google_sheets_api_credentials"]
#secrets_auth_ = secrets_auth

#open prospect sheet
@st.cache_resource(show_spinner=False)
def worksheet(_credentials):
  scope = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
  Worksheet = ServiceAccountCredentials.from_json_keyfile_dict(_credentials, scope)
  client = gspread.authorize(Worksheet)
  sheet = client.open("mydb").worksheets()[2]
  return sheet


sheet = worksheet(_credentials = credentials["google_sheets_api_credentials"])
#sheet = worksheet(_credentials = secrets_auth_)

# Session state initialization
if "verification_code" not in st.session_state:
    st.session_state.verification_code = None
if "email_verified" not in st.session_state:
    st.session_state.email_verified = False
    
if ("submitted1" and "submitted2" not in st.session_state):
    st.session_state["submitted1"] = False
    st.session_state["submitted2"] = False




#sys.stdout.reconfigure(encoding='utf-8')
smtp_gmail = "moudakira.ma@gmail.com"
#smtp_gmail = st.secrets["smtp_gmail"]
smtp_password = "xjsr ppjo azos seqd"
#smtp_password = st.secrets["smtp_password"]  

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
                    <img src="C:/Users/hp/OneDrive/Images/Moudakira/app_images/Moudkira_dark_v_100_100.png" width="300" height="200">
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
    smtp.login(sender_email, sender_password)
    smtp.send_message(msg)





# Show columns only if form is not submitted
if (not st.session_state["submitted1"] and not st.session_state["submitted2"]):
    st.title("Plans d'inscription")

    col1, col2 = st.columns([0.5, 0.5])
    
    form1 = col1.form(key="transfer")
    form1.header("Code Clé Pédagogique")
    
    form1.write("Une fois le paiement effectué par un virement, un code vous sera envoyé à saisir pour débloquer l'accès à toutes les unités.")
    #form1.image(r"C:\Users\hp\Downloads\payment_with_code.png",use_container_width = True)
    for i in range (3):
        form1.write("  ")
    form1.info("Seulement à 99 DH!")
    submit1 = form1.form_submit_button("Continue")
    
    form2 = col2.form(key="delivery")
    
    form2.header("Satisfait ou rien à payer!")
    text = ("Une fois que vous avez saisi les informations requises, nous créons votre cahier journalier et vous permettons de le visualiser en avant-première. "
            "Nous recueillons ensuite vos retours pour apporter les modifications nécessaires. Enfin, vous procédez au paiement par virement et recevez votre cahier journalier par e-mail ou via WhatsApp.")
    form2.write(text)
    form2.info("Tout ça coûte 149 DH")
    submit2 = form2.form_submit_button("Continue")
    
    # If either form is submitted, update session state and rerun
    if submit1 :
        st.session_state["submitted1"] = True
        st.rerun()
    if submit2:
        st.session_state["submitted2"] = True
        st.rerun()

# Display new content after submission 1
if st.session_state["submitted1"]:
    st.write("### Veuillez effectuer un virement de **99 DH** sur le numéro de compte ou scanner le QR code.")
    st.info("**Banque**: Attijariwafa Bank \n\n"
            "**Numéro de compte : 007194000702200030726337**")
    col1,col2 = st.columns(2)
    col1.image(r"C:\Users\hp\Downloads\Attijari_logo_resized.png",use_container_width="auto")
    col2.image(r"C:\Users\hp\Downloads\account_QRCode.jpeg")
    st.write("Veuillez envoyez une capture d'écran de votre payemnt sur l'email suivant: **moudakira.ma@gmail.com** "
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
        if not re.match(r"^0[1-9]\d{8}$",str(phone_number) ): st.warning("Le fromat de votre numéro de téléphone est incorrect!")
        
        teaching_lng = st.multiselect("***La matiére que vous enseignez***:",["Français","Arabe"])
        teaching_class = st.multiselect("***Le(s) niveau(x) que vous enseignez***:",range(1,6),)
        continue_btn = st.form_submit_button("Continue")
        
    if continue_btn:
        if all([family_name, first_name, gmail, phone_number]):
            # Generate and send email
            verification_code = str(np.random.randint(10000, 99999))
            try:
                # send verification code to the user to verify his gmail
                send_email_ssl(sender_email =  smtp_gmail, sender_password =smtp_password, receiver_email = gmail,
                                    subject="Vérification de votre adresse e-mail",body = body_message(verification_code = verification_code ))
                
            except: st.warning("Votre gmail est incorrect.")
            
            st.session_state.verification_code = verification_code
            st.write(verification_code)
            st.success("Un email a été envoyé avec le code de vérification.")
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
                sheet.append_row(
                                 [family_name, first_name, gmail, phone_number,
                                  teaching_lng[0] +" et "+teaching_lng[1], 
                                  ' et '.join(str(num) for num in teaching_class)]
                                 )
                send_email_ssl(sender_email =  smtp_gmail, sender_password =smtp_password, receiver_email = "moudakira.ma@gmail.com",
                                    subject="Un nouveau prospecte est ajouté!",
                                    body =" Tu as une nouvelle demande de cahier journalier sur Moudakira.ma." )
                st.info("***Votre demande a été bien enregistrée! Nous vous contacterons dans les plus brefs délais.***")
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
 




