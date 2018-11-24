from django import forms


class ButtonRadio(forms.RadioSelect):
    def __init__(self, **kwargs):
        attrs = kwargs.pop('attrs', {})
        attrs['class'] = 'radio-button'
        kwargs['attrs'] = attrs

        super().__init__(**kwargs)
