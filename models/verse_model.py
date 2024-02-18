import os
from dotenv import load_dotenv
from pyairtable.orm import Model, fields as F   

load_dotenv()

class Verse(Model):
    title = F.TextField("Title")
    content = F.TextField("Content")
    image = F.AttachmentsField("Image")
    video = F.UrlField("Video")
    language = F.SelectField("Language", choices=["pt", "en", "es"])
    created_at = F.DatetimeField("CreatedAt")
    send_at = F.DatetimeField("SendAt")
    status = F.SelectField("Status", choices=["PENDING", "SENT", "ERROR"])

    class Meta:
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = "Customers"
        api_key = os.getenv("AIRTABLE_TOKEN")