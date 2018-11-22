import os
import yaml

from django.conf import settings



ENTRY_FORM_CONFIG_FILE = os.path.join(settings.BASE_DIR, 'socialsystem', 'config', 'entry-form.yaml')


class EntryFormConfig(object):
    def __init__(self, config_path):
        with open(os.path.join(settings.BASE_DIR, 'socialsystem', 'config', 'entry-form.yaml'), 'r') as entry_form_stream:
            self.raw_config = yaml.load(entry_form_stream)

    def get_bitfield_flags(self):
        """
        Generate BitField flags from given questions and choices.
        """
        return list((
            ('%s__%s' % (question['id'], option['value']), '%s : %s' % (question['question'], option['label']))
            for question in self.raw_config for option in question['options']
        ))


entry_form_config = EntryFormConfig(ENTRY_FORM_CONFIG_FILE)
