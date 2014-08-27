import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from village.models import Village, calculate_villages
from village.utils import get_fourth_point, get_distance


DISTANCE_REGEX = '(:?(:?(?P<hours>\d+)\:)?(?P<minutes>\d+)\:)?(?P<seconds>\d+)'


class CreateVillageForm(forms.Form):
    name = forms.RegexField(label=_("village name"), max_length=128,
                            regex=r'^[\w.@+-]+$',
                            help_text=_("required, 128 characters or fewer, letters, digits and "
                                        "@/./+/-/_ only."),
                            error_messages={
                                'invalid': _("This value may contain only letters, numbers and "
                                             "@/./+/-/_ characters.")})

    id = forms.IntegerField(label=_("village id"),
                            help_text=_("required, 12 characters or fewer, digits only."))

    a = forms.ModelChoiceField(queryset=Village.objects.all(), label=_('first village'), required=True) # , error_messages={'invalid': _('must have')}

    toa = forms.RegexField(label=_('time to first village'), regex=DISTANCE_REGEX,
                           help_text=_('required, format is [[hours:]minutes:]seconds'),
                           initial=0, required=True)

    b = forms.ModelChoiceField(queryset=Village.objects.all(), label=_('second village'), required=True)

    tob = forms.RegexField(label=_('time to second village'), regex=DISTANCE_REGEX,
                           help_text=_('required, format is [[hours:]minutes:]seconds'),
                           initial=0, required=True)

    c = forms.ModelChoiceField(queryset=Village.objects.all(), label=_('third village'), required=True)

    toc = forms.RegexField(label=_('time to third village'), regex=DISTANCE_REGEX,
                           help_text=_('required, format is [[hours:]minutes:]seconds'),
                           initial=0, required=True)

    def clean_toa(self):
        return parse_distance_value(self, 'toa')

    def clean_tob(self):
        return parse_distance_value(self, 'tob')

    def clean_toc(self):
        return parse_distance_value(self, 'toc')

    def clean(self):
        cleaned_data = super(CreateVillageForm, self).clean()
        a = cleaned_data['a']
        b = cleaned_data['b']
        c = cleaned_data['c']
        try:
            point = get_fourth_point((a.x, a.y), (b.x, b.y), (c.x, c.y),
                                     cleaned_data['toa'], cleaned_data['tob'], cleaned_data['toc'])
            cleaned_data['village'] = Village(id=cleaned_data['id'], name=cleaned_data['name'], x=point[0], y=point[1])
        except ValueError:
            raise forms.ValidationError(_('village position cannot be calculated, please, verify source data'))
        return cleaned_data

    def save(self):
        self.cleaned_data['village'].save()


class InitVillagesForm(forms.Form):
    a_id = forms.IntegerField(label=_('first village id'), required=True)
    a = forms.CharField(label=_('first village name'), max_length=128, required=True)
    b_id = forms.IntegerField(label=_('second village id'), required=True)
    b = forms.CharField(label=_('second village name'), max_length=128, required=True)
    c_id = forms.IntegerField(label=_('third village id'), required=True)
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

    def clean_ab(self):
        return parse_distance_value(self, 'ab')

    def clean_bc(self):
        return parse_distance_value(self, 'bc')

    def clean_ca(self):
        return parse_distance_value(self, 'ca')

    def clean(self):
        cleaned_data = super(InitVillagesForm, self).clean()
        try:
            villages = calculate_villages(cleaned_data['a'], cleaned_data['b'], cleaned_data['c'],
                                          cleaned_data['a_id'], cleaned_data['b_id'], cleaned_data['c_id'],
                                          cleaned_data['ab'], cleaned_data['bc'], cleaned_data['ca'], )
            cleaned_data['villages'] = villages
        except ValueError:
            raise forms.ValidationError(_('village positions are impossible, please, verify source data'))
        return cleaned_data

    def save(self):
        Village.objects.all().delete()
        for village in self.cleaned_data['villages']:
            village.save()


class CalculateTimeForm(forms.Form):

    a = forms.ModelChoiceField(queryset=Village.objects.all(), label=_('first village'), required=True)
    b = forms.ModelChoiceField(queryset=Village.objects.all(), label=_('second village'), required=True)

    distance = None
    def clean(self):
        cleaned_data = super(CalculateTimeForm, self).clean()
        a = cleaned_data['a']
        b = cleaned_data['b']
        try:
            distance = get_distance((a.x, a.y), (b.x, b.y))
#            cleaned_data['village'] = Village
#            cleaned_data['a'] = Village(name=cleaned_data['name'], x=distance)

        except ValueError:
            raise forms.ValidationError(_('one or more village have not right coord, please, verify source data'))
        return cleaned_data

#    def save(self):
#        self.cleaned_data['village'].save()


def parse_distance_value(self, field):
    return parse_distance(self.cleaned_data[field])

def parse_distance(value):
    regex = re.compile(DISTANCE_REGEX)
    data = regex.match(value)
    hours = data.group('hours') or 0
    minutes = data.group('minutes') or 0
    seconds = data.group('seconds')
    result = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return result

def format_distance(value):
    hours = int(value / 3600)
    minutes = int((value % 3600) / 60)
    seconds = value % 60
    return u'%02d:%02d:%02d' % (hours, minutes, seconds)

def transfer_time(distance):
    hours = round( distance // 3600)
    minutes = (round(distance) // 60) - hours * 60
    seconds = round(distance - minutes * 60 - hours *3600)
    result = hours+':'+minutes+':'+seconds
    return result