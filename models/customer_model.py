import os
from pyairtable.orm import Model, fields as F

class Customer(Model):
    document = F.TextField("Document")
    utm_source = F.TextField("UtmSource")
    utm_medium = F.TextField("UtmMedium")
    utm_campaign = F.TextField("UtmCampaign")
    utm_term = F.TextField("UtmTerm")
    utm_content = F.TextField("UtmContent")
    src = F.TextField("Src")
    lead_link = F.LinkField("Lead", lazy=True)  # Substitua "LeadLink" pelo nome real do campo de link no Airtable

    class Meta:
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = "Customers"
        api_key = os.getenv("AIRTABLE_TOKEN")