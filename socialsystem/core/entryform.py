import os
import yaml
from operator import attrgetter


from django.conf import settings
from django import forms

from ..forms.widgets import ButtonRadio


ENTRY_FORM_CONFIG_FILE = os.path.join(settings.BASE_DIR, 'socialsystem', 'config', 'entry-form.yaml')


def build_question_flag(question):
    return 'bit_%d' % question['id']


class EntryFormConfig(object):
    def __init__(self, config_path):
        with open(os.path.join(settings.BASE_DIR, 'socialsystem', 'config', 'entry-form.yaml'), 'r') as entry_form_stream:
            self.raw_config = yaml.load(entry_form_stream)

    def __iter__(self):
        """
        Provides nice iterator API over entry form questions.
        """
        return (question for question in self.raw_config)

    def get_bitfield_flags(self):
        """
        Generate BitField flags from given questions and choices.
        """
        return list((build_question_flag(question), question['question']) for question in sorted(self.raw_config, key=lambda i: i['ord']))


entry_form_config = EntryFormConfig(ENTRY_FORM_CONFIG_FILE)


class EntryForm(forms.Form):
    def __init__(self, entry_form_config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for question in entry_form_config:
            kwargs = {
                # 'widget': ButtonRadio(choices=((True, 'Ano'), (False, 'Ne'))),
                'widget': forms.RadioSelect(choices=((True, 'Ano'), (False, 'Ne'))),
                'required': False,
                'label': question['question'],
                'initial': False,
            }

            if 'description' in question:
                kwargs['help_text'] = question['description']

            self.fields[str(question['id'])] = forms.BooleanField(**kwargs)

