from django import forms
from jsoneditor.forms import JSONEditor
import os
import glob


class NBTeditForm(forms.Form):
    
    jsondata = forms.CharField(widget=JSONEditor)


class dimentionChoiceForm(forms.Form):

    worldid = forms.CharField(max_length=255,required=True,label="world uuid",widget=forms.TextInput(attrs={'style': 'width: 400px;','id': 'id_worldid','readonly': 'readonly'}))#,widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}))
    key = forms.CharField(max_length=255,required=True,label="key",widget=forms.TextInput(attrs={'style': 'width: 400px;','id': 'id_key','readonly': 'readonly'}))#,widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}))

    #choice_tuple_dim = (("0","Overworld"),("1","Nether"),("2","End"))
    #choice_dim = forms.ChoiceField(choices=choice_tuple_dim,required=False,label="dimention")

    #choice_tuple_type = (("0","--category--"),("1","entity"),("2","block entity"),("3","village"),("4","player"))
    #choice_type = forms.ChoiceField(choices=choice_tuple_type,required=False,label="category",widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_type'}))

class uploadForm(forms.Form):

    file = forms.FileField(required=True,widget=forms.FileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}))