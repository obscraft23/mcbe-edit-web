from django.db import models
#from jsoneditor.fields.django3_jsonfield import JSONField
#from django.db.models.fields.json import JSONField
from jsoneditor.fields.django3_jsonfield import JSONField

from .jsonwidget import JSONField as JSONField2

import json
import os
"""
def loadjson():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'custom.spawner.json')
    with open(file_path,"rt",encoding="utf-8") as f:
        temp =json.load(f)
        
    return [temp[0],temp[0]]#json.dumps(temp, ensure_ascii=False)

# Create your models here.
class BlogPost(models.Model):
    #content = JSONField()

    title = models.CharField(max_length=255)
    #content = JSONField(default=loadjson())
"""