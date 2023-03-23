from django import forms
from jsoneditor.forms import JSONEditor
from .editbeworld import beworld
import os
import glob


class NBTeditForm(forms.Form):
    
    """
    worldid = forms.CharField(max_length=255,required=True,label="world uuid",widget=forms.TextInput(attrs={'style': 'width: 300px;'}))
    
    worldidpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data/"+worldid+'/')
    worldfname = glob.glob(worldidpath+"/*/db")[0][:-3]
    obj = beworld(worldfname)
    choice_tuple_entity = obj.getChoiceOfEntity()
    
    choice_entity = forms.ChoiceField(choices=choice_tuple_entity,required=True,label="entity")
    """
    jsondata = forms.CharField(widget=JSONEditor)


class dimentionChoiceForm(forms.Form):

    worldid = forms.CharField(max_length=255,required=True,label="world uuid",widget=forms.TextInput(attrs={'style': 'width: 300px;','id': 'id_worldid'}))#,widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}))

    choice_tuple_dim = (("0","Overworld"),("1","Nether"),("2","End"))
    choice_dim = forms.ChoiceField(choices=choice_tuple_dim,required=False,label="dimention")

    choice_tuple_type = (("0","--category--"),("1","entity"),("2","block entity"),("3","village"),("4","player"))
    choice_type = forms.ChoiceField(choices=choice_tuple_type,required=False,label="category",widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_type'}))

class uploadForm(forms.Form):

    file = forms.FileField(required=True,widget=forms.FileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}))
