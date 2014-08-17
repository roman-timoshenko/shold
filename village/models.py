from django.db import models
from django.db.models import Model
from django.db.models.fields import BigIntegerField, CharField, DateTimeField
from django.utils.translation import ugettext, ugettext_lazy as _


class Village(Model):
    name = CharField(max_length=128, verbose_name=_('village name'), unique=True, blank=False, db_index=True)
    x = BigIntegerField(verbose_name=_('coordinate x'))
    y = BigIntegerField(verbose_name=_('coordinate y'))
    created = DateTimeField(verbose_name=_('created'), auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('village')
        verbose_name_plural = _('villages')
        unique_together = (('x', 'y'),)
        index_together = (('x', 'y'),)
