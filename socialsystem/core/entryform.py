import os
import yaml

from django.conf import settings
from django import forms

from ..forms.widgets import ButtonRadio


ENTRY_FORM_CONFIG_FILE = os.path.join(settings.BASE_DIR, 'socialsystem', 'config', 'entry-form.yaml')


class EntryFormConfig(object):
    def __init__(self, config_path):
        with open(os.path.join(settings.BASE_DIR, 'socialsystem', 'config', 'entry-form.yaml'), 'r') as entry_form_stream:
            self.raw_config = yaml.load(entry_form_stream)

    def __iter__(self):
        """
        Provides nice iterator API over entry form questions.
        """
        return ((question, question['options']) for question in self.raw_config)

    def get_bitfield_flags(self):
        """
        Generate BitField flags from given questions and choices.
        """
        return list((
            ('%s__%s' % (question['id'], option['value']), '%s : %s' % (question['question'], option['label']))
            for question in self.raw_config for option in question['options']
        ))


entry_form_config = EntryFormConfig(ENTRY_FORM_CONFIG_FILE)


class EntryForm(forms.Form):
    def __init__(self, entry_form_config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for question, options in entry_form_config:
            choices = ((opt['value'], opt['label']) for opt in options)
            self.fields[question['id']] = forms.ChoiceField(choices=choices, widget=ButtonRadio())

