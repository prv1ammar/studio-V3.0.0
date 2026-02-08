# utils/airtable_client.py - VERSION COMPLÈTE CORRIGÉE

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "applKB5Q9LlgtJdIi")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "pat...")
AIRTABLE_PATIENTS_TABLE = os.getenv("AIRTABLE_PATIENTS_TABLE", "tblW4LetJ1YeijS4i")
AIRTABLE_APPOINTMENTS_TABLE = os.getenv("AIRTABLE_APPOINTMENTS_TABLE", "tbleZ3nzvr5VmQrAd")

print(f"""[AIRTABLE] Configuration:
  - BASE_ID: {'✓' if AIRTABLE_BASE_ID else '✗'}
  - API_KEY: {'✓' if AIRTABLE_API_KEY else '✗'}
  - Table Patients: {AIRTABLE_PATIENTS_TABLE}
  - Table Appointments: {AIRTABLE_APPOINTMENTS_TABLE}
""")

class AirtableBase:
    def __init__(self, table_name: str):
        self.base_id = AIRTABLE_BASE_ID
        self.api_key = AIRTABLE_API_KEY
        self.table_name = table_name
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str = "", data: dict = None, params: dict = None):
        """Fait une requête à l'API Airtable"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            print(f"[AIRTABLE] Requête {method} vers: {url}")
            if params:
                print(f"[AIRTABLE] Params: {params}")
            
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                return None
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"[AIRTABLE] ❌ Erreur {method} {url}: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"[AIRTABLE] Détails: {e.response.text}")
            return None

class AirtablePatients(AirtableBase):
    def __init__(self):
        super().__init__(AIRTABLE_PATIENTS_TABLE)
        print(f"[AIRTABLE PATIENTS] ✅ Connecté à la table: {self.table_name}")
    
    def get_patient_by_email(self, email: str):
        """Trouve un patient par email"""
        try:
            print(f"[PATIENTS] 🔍 Recherche par email: {email}")
            
            formula = f"{{email}} = '{email}'"
            params = {
                "filterByFormula": formula,
                "maxRecords": 1
            }
            
            response = self._make_request("GET", params=params)
            
            if response and "records" in response and len(response["records"]) > 0:
                record = response["records"][0]
                fields = record.get("fields", {})
                print(f"[PATIENTS] ✅ Patient trouvé: {fields.get('full_name')}")
                return {
                    "id": record.get("id"),
                    "name": fields.get("full_name"),
                    "email": fields.get("email"),
                    "phone": fields.get("phone", "")
                }
            else:
                print(f"[PATIENTS] ℹ️  Aucun patient pour email: {email}")
                return None
                
        except Exception as e:
            print(f"[PATIENTS] ❌ Erreur recherche: {e}")
            return None
    
    def get_patient_by_phone(self, phone: str):
        """Trouve un patient par numéro de téléphone"""
        try:
            # Nettoyer le numéro (enlever espaces, +, etc.)
            clean_phone = ''.join(filter(str.isdigit, phone))
            print(f"[PATIENTS] 🔍 Recherche par téléphone: {clean_phone}")
            
            formula = f"{{phone}} = '{clean_phone}'"
            params = {
                "filterByFormula": formula,
                "maxRecords": 1
            }
            
            response = self._make_request("GET", params=params)
            
            if response and "records" in response and len(response["records"]) > 0:
                record = response["records"][0]
                fields = record.get("fields", {})
                print(f"[PATIENTS] ✅ Patient trouvé par téléphone: {fields.get('full_name')}")
                return {
                    "id": record.get("id"),
                    "name": fields.get("full_name"),
                    "email": fields.get("email"),
                    "phone": fields.get("phone", "")
                }
            else:
                print(f"[PATIENTS] ℹ️  Aucun patient pour téléphone: {clean_phone}")
                return None
                
        except Exception as e:
            print(f"[PATIENTS] ❌ Erreur recherche téléphone: {e}")
            return None
    
    def create_patient(self, patient_data: dict):
        """Crée un nouveau patient"""
        try:
            print(f"[PATIENTS] 📝 Création: {patient_data.get('name')}")
            
            # Nettoyer le téléphone
            phone = patient_data.get("phone", "")
            clean_phone = ''.join(filter(str.isdigit, phone)) if phone else ""
            
            fields = {
                "full_name": patient_data.get("name"),
                "email": patient_data.get("email"),
                "phone": clean_phone
            }
            
            print(f"[PATIENTS] 📊 Champs envoyés: {fields}")
            
            data = {"fields": fields}
            response = self._make_request("POST", data=data)
            
            if response:
                print(f"[PATIENTS] ✅ Patient créé: {response.get('id')}")
                fields = response.get("fields", {})
                return {
                    "id": response.get("id"),
                    "name": fields.get("full_name"),
                    "email": fields.get("email"),
                    "phone": fields.get("phone", "")
                }
            else:
                print(f"[PATIENTS] ❌ Échec création")
                return None
                
        except Exception as e:
            print(f"[PATIENTS] ❌ Erreur création: {e}")
            return None

class AirtableAppointments(AirtableBase):
    def __init__(self):
        super().__init__(AIRTABLE_APPOINTMENTS_TABLE)
        print(f"[AIRTABLE APPOINTMENTS] ✅ Connecté à la table: {self.table_name}")
    
    def create_appointment(self, data: dict):
        """Crée un nouveau rendez-vous"""
        try:
            print(f"[APPOINTMENTS] 📝 Création RDV: {data.get('patient_name')}")
            
            # STRUCTURE SIMPLE
            fields = {
                "Patient Name": data["patient_name"],
                "email": data["patient_email"],
                "date": data["date"],
                "time": data["time"]
            }
            
            # Ajouter conditionnellement
            if "patient_id" in data:
                fields["patient_id"] = [data["patient_id"]]
            
            if "service" in data:
                fields["Service"] = data["service"]
            
            if "doctor" in data:
                fields["Doctor"] = data["doctor"]
            
            if "status" in data:
                fields["status"] = data["status"]
            else:
                fields["status"] = "confirmed"
            
            print(f"[APPOINTMENTS] 📊 Données envoyées: {fields}")
            
            response = self._make_request("POST", data={"fields": fields})
            
            if response:
                appointment_id = response.get("id")
                print(f"[APPOINTMENTS] ✅ Rendez-vous créé: {appointment_id}")
                return {
                    "id": appointment_id,
                    "fields": response.get("fields", {})
                }
            else:
                print(f"[APPOINTMENTS] ❌ Échec création")
                return None
                
        except Exception as e:
            print(f"[APPOINTMENTS] ❌ Erreur création: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_all_appointments(self, max_records: int = 100):
        """Récupère tous les rendez-vous (pour filtrage local)"""
        try:
            print(f"[APPOINTMENTS] 🔍 Récupération de tous les RDV (max: {max_records})")
            
            params = {
                "maxRecords": max_records
            }
            
            response = self._make_request("GET", params=params)
            
            if response and "records" in response:
                appointments = []
                for record in response["records"]:
                    fields = record.get("fields", {})
                    appointments.append({
                        "record": record,
                        "id": record.get("id"),
                        "date": fields.get("date"),
                        "time": fields.get("time"),
                        "service": fields.get("Service", "Consultation"),
                        "doctor": fields.get("Doctor", "Dr. Ahmed"),
                        "status": fields.get("status", "confirmed"),
                        "patient_name": fields.get("Patient Name", ""),
                        "phone": fields.get("phone", ""),
                        "email": fields.get("email") or fields.get("Email", "")
                    })
                
                print(f"[APPOINTMENTS] ✅ {len(appointments)} RDV récupérés")
                return appointments
            else:
                print(f"[APPOINTMENTS] ℹ️  Aucun RDV trouvé")
                return []
                
        except Exception as e:
            print(f"[APPOINTMENTS] ❌ Erreur récupération: {e}")
            return []
    
    def get_appointments_by_email(self, email: str):
        """Récupère les rendez-vous par email - VERSION SIMPLE"""
        try:
            print(f"[APPOINTMENTS] 🔍 Recherche RDV pour email: {email}")
            
            # Récupérer tous les RDV et filtrer localement
            all_appointments = self.get_all_appointments()
            
            if not all_appointments:
                return []
            
            # Filtrer par email
            matching_appointments = []
            for appt in all_appointments:
                appt_email = appt.get("email", "")
                if email.lower() == appt_email.lower():
                    matching_appointments.append({
                        "id": appt.get("id"),
                        "date": appt.get("date"),
                        "time": appt.get("time"),
                        "service": appt.get("service"),
                        "doctor": appt.get("doctor"),
                        "status": appt.get("status"),
                        "patient_name": appt.get("patient_name"),
                        "phone": appt.get("phone")
                    })
            
            print(f"[APPOINTMENTS] ✅ {len(matching_appointments)} RDV trouvés pour {email}")
            return matching_appointments
            
        except Exception as e:
            print(f"[APPOINTMENTS] ❌ Erreur recherche email: {e}")
            return []
    
    def get_appointments_by_phone(self, phone: str):
        """Récupère les rendez-vous par téléphone"""
        try:
            # Nettoyer le téléphone
            clean_phone = ''.join(filter(str.isdigit, phone))
            print(f"[APPOINTMENTS] 🔍 Recherche RDV pour téléphone: {clean_phone}")
            
            # Récupérer tous les RDV et filtrer localement
            all_appointments = self.get_all_appointments()
            
            if not all_appointments:
                return []
            
            # Filtrer par téléphone
            matching_appointments = []
            for appt in all_appointments:
                appt_phone = appt.get("phone", "")
                appt_phone_clean = ''.join(filter(str.isdigit, appt_phone)) if appt_phone else ""
                
                if clean_phone == appt_phone_clean:
                    matching_appointments.append({
                        "id": appt.get("id"),
                        "date": appt.get("date"),
                        "time": appt.get("time"),
                        "service": appt.get("service"),
                        "doctor": appt.get("doctor"),
                        "status": appt.get("status"),
                        "patient_name": appt.get("patient_name"),
                        "phone": appt.get("phone"),
                        "email": appt.get("email", "")
                    })
            
            print(f"[APPOINTMENTS] ✅ {len(matching_appointments)} RDV trouvés par téléphone")
            return matching_appointments
            
        except Exception as e:
            print(f"[APPOINTMENTS] ❌ Erreur recherche téléphone: {e}")
            return []
    
    def update_appointment(self, appointment_id: str, data: dict):
        """Met à jour un rendez-vous"""
        try:
            print(f"[APPOINTMENTS] 🔄 Mise à jour RDV: {appointment_id}")
            print(f"[APPOINTMENTS] 📊 Données reçues: {data}")
            
            fields = {}
            
            if "date" in data:
                fields["date"] = data["date"]
            
            if "time" in data:
                fields["time"] = data["time"]
            
            if "service" in data:
                fields["Service"] = data["service"]
            
            if "doctor" in data:
                fields["Doctor"] = data["doctor"]
            
            if "status" in data:
                fields["status"] = data["status"]
            
            if "cancellation_reason" in data:
                fields["Cancellation Reason"] = data["cancellation_reason"]
            
            if "google_event_id" in data:
                fields["google_event_id"] = data["google_event_id"]
            
            if "phone" in data:
                clean_phone = ''.join(filter(str.isdigit, data["phone"])) if data["phone"] else ""
                fields["phone"] = clean_phone
            
            if not fields:
                print(f"[APPOINTMENTS] ⚠️ Aucun champ à mettre à jour")
                return False
            
            print(f"[APPOINTMENTS] 📊 Mise à jour avec: {fields}")
            
            # Utiliser la méthode _make_request pour PATCH
            response = self._make_request("PATCH", 
                                         endpoint=f"/{appointment_id}",
                                         data={"fields": fields})
            
            if response:
                print(f"[APPOINTMENTS] ✅ RDV mis à jour")
                return True
            else:
                print(f"[APPOINTMENTS] ❌ Échec mise à jour")
                return False
                
        except Exception as e:
            print(f"[APPOINTMENTS] ❌ Erreur mise à jour: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def find_appointment_by_phone_and_date(self, phone: str, date: str = None):
        """Trouve un RDV par téléphone et optionnellement date"""
        try:
            clean_phone = ''.join(filter(str.isdigit, phone))
            
            # Récupérer tous les RDV
            all_appointments = self.get_all_appointments()
            
            if not all_appointments:
                return None
            
            # Chercher les correspondances
            matching_appointments = []
            for appt in all_appointments:
                appt_phone = appt.get("phone", "")
                appt_phone_clean = ''.join(filter(str.isdigit, appt_phone)) if appt_phone else ""
                
                if clean_phone == appt_phone_clean:
                    if date:
                        appt_date = appt.get("date", "")
                        if appt_date == date:
                            print(f"[APPOINTMENTS] ✅ RDV trouvé pour {date}")
                            return {
                                "id": appt.get("id"),
                                "fields": appt.get("record", {}).get("fields", {})
                            }
                    else:
                        matching_appointments.append(appt.get("record"))
            
            if not date and matching_appointments:
                return matching_appointments
            
            print(f"[APPOINTMENTS] ℹ️  Aucun RDV pour téléphone: {clean_phone}")
            return None
            
        except Exception as e:
            print(f"[APPOINTMENTS] ❌ Erreur recherche: {e}")
            return None

# Instances globales
airtable_patients = AirtablePatients()
airtable_appointments = AirtableAppointments()