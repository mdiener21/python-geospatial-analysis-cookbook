#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django import forms


class MapEditForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(required=False)
    projection = forms.CharField(max_length=32, required=False)
    zoom = forms.IntegerField(required=False)
    selected_layers = forms.CharField(required=False)

    def clean_jsonfield(self):
         jdata = self.cleaned_data['selected_layers']
         try:
             json_data = json.loads(jdata) #loads string as json
         except:
             raise forms.ValidationError("Invalid data in jsonfield")
         return jdata
