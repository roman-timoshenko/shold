from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
import re
from village.models import Village

DISTANCE_REGEX = '(:?(:?(?P<hours>\d+)\:)?(?P<minutes>\d+)\:)?(?P<seconds>\d+)'


class CreateVillageForm(forms.Form):
    name = forms.RegexField(label=_("village name"), max_length=128,
                            regex=r'^[\w.@+-]+$',
                            help_text=_("required, 128 characters or fewer, letters, digits and "
                                        "@/./+/-/_ only."),
                            error_messages={
                                'invalid': _("This value may contain only letters, numbers and "
                                             "@/./+/-/_ characters.")})

    a = forms.ModelChoiceField(queryset=Village.objects.all(), label=_('first village'), required=True)
    b = forms.ModelChoiceField(queryset=Village.objects.all(), label=_('second village'), required=True)
    c = forms.ModelChoiceField(queryset=Village.objects.all(), label=_('third village'), required=True)

    toa = forms.RegexField(label=_('time from first village'), regex=DISTANCE_REGEX,
                           help_text=_('required, format is [[hours:]minutes:]seconds'),
                           initial=0, required=True)
    tob = forms.RegexField(label=_('time from second village'), regex=DISTANCE_REGEX,
                           help_text=_('required, format is [[hours:]minutes:]seconds'),
                           initial=0, required=True)
    toc = forms.RegexField(label=_('time from third village'), regex=DISTANCE_REGEX,
                           help_text=_('required, format is [[hours:]minutes:]seconds'),
                           initial=0, required=True)

    def get_toa(self):
        return parse_value(self, 'toa')

    def get_tob(self):
        return parse_value(self, 'tob')

    def get_toc(self):
        return parse_value(self, 'toc')


class InitVillagesForm(forms.Form):
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
    regex = re.compile(DISTANCE_REGEX)
    data = regex.match(self.cleaned_data[field])
    hours = data.group('hours') or 0
    minutes = data.group('minutes') or 0
    seconds = data.group('seconds')
    result = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return result
