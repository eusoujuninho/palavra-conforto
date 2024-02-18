import os
from pyairtable.orm import Model, fields as F

class Devotional(Model):
    title = F.TextField("Title")
    content = F.TextField("Content")
    prayer = F.TextField("Prayer")
    image = F.TextField("Image")
    audio = F.TextField("Audio")
    video = F.TextField("Video")
    language = F.TextField("Language")
    created_at = F.DatetimeField("CreatedAt")
    send_at = F.DatetimeField("SendAt")
    status = F.TextField("Status")

    class Meta:
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = "Devotionals"
        api_key = os.getenv("AIRTABLE_TOKEN")