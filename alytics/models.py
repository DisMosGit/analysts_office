from django.db import models
from django.utils.translation import gettext as _


class Graph(models.Model):
    func = models.CharField(verbose_name=_("functions"), max_length=255)
    points = models.JSONField(verbose_name=_("points"), null=True)
    interval = models.IntegerField(verbose_name=_("interval"), default=7)
    step = models.IntegerField(verbose_name=_("step"), default=2)
    date_created = models.DateTimeField(verbose_name=_("crated"),
                                        auto_now_add=True)
    date_processed = models.DateTimeField(verbose_name=_("processed"),
                                          null=True)
