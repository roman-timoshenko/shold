from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
import re


class CreateVillageForm(forms.BaseForm):
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})


class InitVillagesForm(forms.Form):

    DISTANCE_REGEX = '(:?(:?(?P<hours>\d+)\:)?(?P<minutes>\d+)\:)?(?P<seconds>\d+)'

    a = forms.CharField(label=_('first village name'), max_length=128, required=True)
    b = forms.CharField(label=_('second village name'), max_length=128, required=True)
    c = forms.CharField(label=_('third village name'), max_length=128, required=True)

    ab = forms.RegexField(label=_('time from first to second village'), regex=DISTANCE_REGEX,
                          help_text=_('required, format is [[hours:]minutes:]seconds'),
                          initial=0, required=True)
    bc = forms.RegexField(label=_('time from second to third village'), regex=DISTANCE_REGEX,
                          help_text=_('required, format is [[hours:]minutes:]seconds'),
                          initial=0, required=True)
    ca = forms.RegexField(label=_('time from third to first village'), regex=DISTANCE_REGEX,
                          help_text=_('required, format is [[hours:]minutes:]seconds'),
                          initial=0, required=True)

    def get_ab(self):
        return parse_value(self, 'ab')

    def get_bc(self):
        return parse_value(self, 'bc')

    def get_ca(self):
        return parse_value(self, 'ca')


def parse_value(self, field):
    regex = re.compile(self.DISTANCE_REGEX)
    data = regex.match(self.cleaned_data[field])
    hours = data.group('hours') or 0
    minutes = data.group('minutes') or 0
    seconds = data.group('seconds')
    result = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return result
