import os
from dotenv import load_dotenv
from pyairtable.orm import Model, fields as F

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Lead(Model):
    name = F.TextField("Name")
    email = F.EmailField("Email")
    mobile_phone = F.TextField("MobilePhone")
    city = F.TextField("City")
    country = F.TextField("Country")
    document = F.TextField("Document")
    utm_source = F.TextField("UtmSource")
    utm_medium = F.TextField("UtmMedium")
    utm_campaign = F.TextField("UtmCampaign")
    utm_term = F.TextField("UtmTerm")
    utm_content = F.TextField("UtmContent")
    src = F.TextField("Src")

    class Meta:
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = "Leads"
        api_key = os.getenv("AIRTABLE_TOKEN")
