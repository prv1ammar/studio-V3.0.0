# utils/google_calendar.py

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os, pickle
from datetime import datetime, timedelta
import logging

# Configuration du logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# AJOUTE "calendar.events" aux SCOPES pour pouvoir créer des événements
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"  # <-- AJOUTÉ pour créer/modifier
]
CALENDAR_ID = "primary"

class GoogleCalendarClient:
    def __init__(self):
        self.service = None
        self.connected = False
        
        try:
            creds = None
            token_path = "token.pickle"
            credentials_path = "credentials.json"

            # Vérifier si les fichiers existent
            if not os.path.exists(credentials_path):
                logger.warning(f"Fichier credentials.json introuvable: {credentials_path}")
                print("[GOOGLE CALENDAR] ⚠️  Fichier credentials.json introuvable")
                return

            if os.path.exists(token_path):
                try:
                    with open(token_path, "rb") as f:
                        creds = pickle.load(f)
                except Exception as e:
                    logger.warning(f"Erreur lecture token.pickle: {e}")
                    creds = None

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception as e:
                        logger.warning(f"Erreur refresh token: {e}")
                        creds = None
                
                if not creds:
                    try:
                        print("[GOOGLE CALENDAR] 🔐 Authentification requise...")
                        flow = InstalledAppFlow.from_client_secrets_file(
                            credentials_path, SCOPES
                        )
                        creds = flow.run_local_server(port=0)
                    except Exception as e:
                        logger.error(f"Erreur authentification Google: {e}")
                        print(f"[GOOGLE CALENDAR] ❌ Erreur d'authentification: {e}")
                        return

                try:
                    with open(token_path, "wb") as f:
                        pickle.dump(creds, f)
                except Exception as e:
                    logger.warning(f"Erreur sauvegarde token: {e}")

            self.service = build("calendar", "v3", credentials=creds)
            self.connected = True
            print("[GOOGLE CALENDAR] ✅ Connecté avec succès (lecture + écriture)")
            
        except Exception as e:
            logger.error(f"Erreur initialisation Google Calendar: {e}")
            print(f"[GOOGLE CALENDAR] ❌ Erreur d'initialisation: {e}")
            self.service = None
            self.connected = False

    def is_slot_available(self, date: str, time: str) -> bool:
        """
        Vérifie si un créneau est disponible dans Google Calendar
        Retourne True si disponible (pas d'événements)
        """
        # Si pas connecté, on considère le créneau comme disponible
        if not self.connected or not self.service:
            print(f"[GOOGLE CALENDAR] ⚠️  Non connecté, on suppose disponible: {date} {time}")
            return True
        
        try:
            # Parse la date et heure
            start_str = f"{date}T{time}"
            try:
                start = datetime.fromisoformat(start_str)
            except ValueError:
                # Si format incorrect, essayer avec parsing manuel
                try:
                    start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                except:
                    print(f"[GOOGLE CALENDAR] ❌ Format date/heure invalide: {date} {time}")
                    return True  # On assume disponible en cas d'erreur
            
            end = start + timedelta(minutes=30)  # Créneau de 30 minutes
            
            # Convertir en format ISO avec timezone
            time_min = start.isoformat() + "Z"
            time_max = end.isoformat() + "Z"
            
            print(f"[GOOGLE CALENDAR] 🔍 Vérification: {time_min} à {time_max}")
            
            # Requête à Google Calendar
            events_result = self.service.events().list(
                calendarId=CALENDAR_ID,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            
            events = events_result.get("items", [])
            
            if events:
                print(f"[GOOGLE CALENDAR] ❌ Occupé: {len(events)} événement(s) trouvé(s)")
                for event in events:
                    print(f"  - {event.get('summary', 'Sans titre')} ({event.get('start', {}).get('dateTime', 'N/A')})")
                return False
            
            print(f"[GOOGLE CALENDAR] ✅ Disponible: {date} à {time}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur vérification créneau {date} {time}: {e}")
            print(f"[GOOGLE CALENDAR] ⚠️  Erreur, on assume disponible: {e}")
            return True  # En cas d'erreur, on assume disponible

    # AJOUTE CES MÉTHODES POUR CRÉER/MODIFIER/SUPPRIMER DES ÉVÉNEMENTS:

    def create_event(self, event_data: dict):
        """
        Crée un événement dans Google Calendar
        """
        if not self.connected or not self.service:
            print(f"[GOOGLE CALENDAR] ⚠️  Non connecté, impossible de créer l'événement")
            return None
        
        try:
            print(f"[GOOGLE CALENDAR] 🗓️  Création événement...")
            print(f"[GOOGLE CALENDAR] 📋 Données: {event_data.get('summary', 'Sans titre')}")
            
            event = self.service.events().insert(
                calendarId=CALENDAR_ID,
                body=event_data
            ).execute()
            
            print(f"[GOOGLE CALENDAR] ✅ Événement créé: {event.get('id')}")
            print(f"[GOOGLE CALENDAR] 🔗 Lien: {event.get('htmlLink')}")
            
            return {
                'id': event.get('id'),
                'htmlLink': event.get('htmlLink'),
                'summary': event.get('summary'),
                'start': event.get('start'),
                'end': event.get('end')
            }
            
        except Exception as e:
            logger.error(f"Erreur création événement: {e}")
            print(f"[GOOGLE CALENDAR] ❌ Erreur création: {e}")
            return None

    def update_event(self, event_id: str, event_data: dict):
        """
        Met à jour un événement existant
        """
        if not self.connected or not self.service:
            print(f"[GOOGLE CALENDAR] ⚠️  Non connecté, impossible de mettre à jour")
            return None
        
        try:
            print(f"[GOOGLE CALENDAR] 🔄 Mise à jour événement: {event_id}")
            
            event = self.service.events().update(
                calendarId=CALENDAR_ID,
                eventId=event_id,
                body=event_data
            ).execute()
            
            print(f"[GOOGLE CALENDAR] ✅ Événement mis à jour: {event_id}")
            return event
            
        except Exception as e:
            logger.error(f"Erreur mise à jour événement {event_id}: {e}")
            print(f"[GOOGLE CALENDAR] ❌ Erreur mise à jour: {e}")
            return None

    def delete_event(self, event_id: str):
        """
        Supprime un événement
        """
        if not self.connected or not self.service:
            print(f"[GOOGLE CALENDAR] ⚠️  Non connecté, impossible de supprimer")
            return False
        
        try:
            print(f"[GOOGLE CALENDAR] ❌ Suppression événement: {event_id}")
            
            self.service.events().delete(
                calendarId=CALENDAR_ID,
                eventId=event_id
            ).execute()
            
            print(f"[GOOGLE CALENDAR] ✅ Événement supprimé: {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur suppression événement {event_id}: {e}")
            print(f"[GOOGLE CALENDAR] ❌ Erreur suppression: {e}")
            return False

# Instance globale avec gestion d'erreur
try:
    google_calendar = GoogleCalendarClient()
except Exception as e:
    print(f"[GOOGLE CALENDAR] ❌ Impossible de créer l'instance: {e}")
    # Créer une instance vide avec les méthodes nécessaires
    class DummyCalendar:
        def __init__(self):
            self.connected = False
            
        def is_slot_available(self, date, time):
            print(f"[GOOGLE CALENDAR DUMMY] ⚠️  Mode simulation: {date} {time} supposé disponible")
            return True
            
        def create_event(self, event_data):
            print(f"[GOOGLE CALENDAR DUMMY] 🗓️  Simulation création: {event_data.get('summary', 'Sans titre')}")
            return {'id': 'dummy_event_id', 'htmlLink': '#'}
            
        def update_event(self, event_id, event_data):
            print(f"[GOOGLE CALENDAR DUMMY] 🔄 Simulation mise à jour: {event_id}")
            return {'id': event_id}
            
        def delete_event(self, event_id):
            print(f"[GOOGLE CALENDAR DUMMY] ❌ Simulation suppression: {event_id}")
            return True
    
    google_calendar = DummyCalendar()