# utils/email_sender.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from dotenv import load_dotenv

load_dotenv()

# Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@artsclinic.com")
EMAIL_NAME = os.getenv("EMAIL_NAME", "Art's Clinic")

# Vérifier la configuration
SMTP_CONFIGURED = all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM])

if not SMTP_CONFIGURED:
    logging.warning("⚠️ SMTP credentials not configured. Email sending will be simulated.")
    print("[EMAIL] ⚠️  SMTP non configuré. Simulation activée.")

def send_email(to_email: str, subject: str, html_body: str, text_body: str = None) -> dict:
    """
    Envoie un email avec HTML et texte
    """
    if not SMTP_CONFIGURED:
        # Mode simulation
        print(f"[EMAIL SIMULATION] ✉️  À: {to_email}")
        print(f"[EMAIL SIMULATION] 📧 Sujet: {subject}")
        print(f"[EMAIL SIMULATION] 📄 Contenu simulé (premières 100 chars): {html_body[:100]}...")
        return {"success": True, "message": "Email simulé (SMTP non configuré)"}
    
    try:
        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{EMAIL_NAME} <{EMAIL_FROM}>"
        msg['To'] = to_email
        
        # Version texte
        if text_body:
            part1 = MIMEText(text_body, 'plain')
            msg.attach(part1)
        
        # Version HTML
        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)
        
        # Connexion et envoi
        print(f"[EMAIL] 🔗 Connexion à {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            print(f"[EMAIL] 🔐 Authentification avec {SMTP_USERNAME}...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            print(f"[EMAIL] 📤 Envoi à {to_email}...")
            server.send_message(msg)
        
        print(f"[EMAIL] ✅ Email envoyé à {to_email}")
        return {"success": True, "message": "Email envoyé avec succès"}
        
    except Exception as e:
        error_msg = f"Erreur envoi email: {str(e)}"
        print(f"[EMAIL] ❌ {error_msg}")
        return {"success": False, "error": error_msg}

def send_confirmation_email(to_email: str, subject: str, html_body: str) -> dict:
    """Alias pour send_email"""
    return send_email(to_email, subject, html_body)

def send_cancellation_email(to_email: str, subject: str, html_body: str) -> dict:
    """Alias pour send_email"""
    return send_email(to_email, subject, html_body)

def send_update_email(to_email: str, subject: str, html_body: str) -> dict:
    """Alias pour send_email"""
    return send_email(to_email, subject, html_body)

# Templates HTML pour les emails
def create_appointment_confirmation_email(
    patient_name: str,
    appointment_date: str,
    appointment_time: str,
    doctor_name: str,
    service: str,
    appointment_id: str = None
) -> str:
    """Crée le HTML pour l'email de confirmation"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Confirmation de rendez-vous</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            .appointment-id {{ background: #f0f0f0; padding: 10px; border-radius: 5px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>✅ Rendez-vous Confirmé</h1>
            <p>Art's Clinic - Centre Dentaire</p>
        </div>
        
        <div class="content">
            <p>Bonjour <strong>{patient_name}</strong>,</p>
            <p>Votre rendez-vous a été confirmé avec succès.</p>
            
            <div class="details">
                <h3>📋 Détails du rendez-vous</h3>
                <p><strong>Date:</strong> {appointment_date}</p>
                <p><strong>Heure:</strong> {appointment_time}</p>
                <p><strong>Docteur:</strong> {doctor_name}</p>
                <p><strong>Service:</strong> {service}</p>
                {f'<p><strong>ID RDV:</strong> <span class="appointment-id">{appointment_id}</span></p>' if appointment_id else ''}
            </div>
            
            <p><strong>📍 Adresse:</strong> 123 Avenue Mohammed V, Casablanca</p>
            <p><strong>📞 Téléphone:</strong> +212 5 22 22 22 22</p>
            
            <p><strong>📝 Instructions:</strong></p>
            <ul>
                <li>Arrivez 15 minutes avant l'heure du rendez-vous</li>
                <li>Apportez votre carte d'identité et carte d'assurance</li>
                <li>Pour annuler ou modifier, appelez-nous au moins 24h à l'avance</li>
            </ul>
            
            <p>Cordialement,<br>L'équipe d'Art's Clinic</p>
        </div>
        
        <div class="footer">
            <p>© 2024 Art's Clinic. Tous droits réservés.</p>
            <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
        </div>
    </body>
    </html>
    """

def create_cancellation_email_template(
    patient_name: str,
    appointment_date: str,
    appointment_time: str,
    cancellation_reason: str = "À la demande du patient"
) -> str:
    """Crée le HTML pour l'email d'annulation"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Annulation de rendez-vous</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>❌ Rendez-vous Annulé</h1>
            <p>Art's Clinic - Centre Dentaire</p>
        </div>
        
        <div class="content">
            <p>Bonjour <strong>{patient_name}</strong>,</p>
            <p>Votre rendez-vous a été annulé avec succès.</p>
            
            <div class="details">
                <h3>📋 Détails de l'annulation</h3>
                <p><strong>Date annulée:</strong> {appointment_date}</p>
                <p><strong>Heure annulée:</strong> {appointment_time}</p>
                <p><strong>Motif:</strong> {cancellation_reason}</p>
            </div>
            
            <p>Pour prendre un nouveau rendez-vous, vous pouvez:</p>
            <ul>
                <li>Appeler notre secrétariat au +212 5 22 22 22 22</li>
                <li>Utiliser notre système de réservation en ligne</li>
                <li>Nous envoyer un email à contact@artsclinic.com</li>
            </ul>
            
            <p>Cordialement,<br>L'équipe d'Art's Clinic</p>
        </div>
        
        <div class="footer">
            <p>© 2024 Art's Clinic. Tous droits réservés.</p>
            <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
        </div>
    </body>
    </html>
    """ 
# Ajoute cette fonction à la fin de utils/email_sender.py

def create_update_email_template(
    patient_name: str,
    old_date: str,
    old_time: str,
    new_date: str,
    new_time: str,
    doctor_name: str,
    service: str
) -> str:
    """Crée le HTML pour l'email de mise à jour de RDV"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .old {{ background: #ffebee; padding: 10px; margin: 10px 0; border-left: 4px solid #f44336; }}
            .new {{ background: #e8f5e9; padding: 10px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔄 Modification de Rendez-vous</h1>
            <p>Art's Clinic - Centre Dentaire</p>
        </div>
        
        <div class="content">
            <p>Bonjour <strong>{patient_name}</strong>,</p>
            <p>Votre rendez-vous a été modifié avec succès.</p>
            
            <div class="old">
                <h3>📅 Ancien rendez-vous</h3>
                <p><strong>Date:</strong> {old_date}</p>
                <p><strong>Heure:</strong> {old_time}</p>
            </div>
            
            <div class="new">
                <h3>📅 Nouveau rendez-vous</h3>
                <p><strong>Date:</strong> {new_date}</p>
                <p><strong>Heure:</strong> {new_time}</p>
                <p><strong>Docteur:</strong> {doctor_name}</p>
                <p><strong>Service:</strong> {service}</p>
            </div>
            
            <p><strong>📍 Adresse:</strong> Art's Clinic, Casablanca</p>
            <p><strong>📞 Contact:</strong> +212 5 22 22 22 22</p>
            
            <p>Cordialement,<br>L'équipe d'Art's Clinic</p>
        </div>
        
        <div class="footer">
            <p>© 2024 Art's Clinic</p>
        </div>
    </body>
    </html>
    """