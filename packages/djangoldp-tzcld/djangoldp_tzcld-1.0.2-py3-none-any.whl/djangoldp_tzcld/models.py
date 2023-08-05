from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from djangoldp.models import Model
from djangoldp_community.models import Community
from djangoldp_tzcld.permissions import TzcldCommunityProfilePermissions


# DjangoLDP User Extension

class TzcldProfile(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tzcld_profile")
    description = models.CharField(max_length=255, blank=True, null=True, default='')
    postal_code = models.CharField(max_length=255, blank=True, null=True, default='')
    address = models.CharField(max_length=255, blank=True, null=True, default='')
    phone = models.CharField(max_length=255, blank=True, null=True, default='')
    position = models.CharField(max_length=255, blank=True, null=True, default='')
    membership = models.BooleanField(default=False)
    last_contribution_year = models.CharField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.user.get_full_name(), self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Profile')
        verbose_name_plural = _("TZCLD Profiles")
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['inherit', 'change']
        ordering = ['user']
        serializer_fields = ['@id', 'description', 'regions', 'postal_code', 'address', 'events', 'phone', 'orgs', 'position', 'membership', 'last_contribution_year']
        rdf_type = "tzcld:profile"
        auto_author = 'user'
        depth = 3


class TzcldProfileEvent(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    tzcldprofile = models.ManyToManyField(TzcldProfile, related_name='events', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Event')
        verbose_name_plural = _("TZCLD Events")
        anonymous_perms = ['view']
        container_path = "tzcld-events/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:event"


class TzcldProfileOrganisation(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    tzcldprofile = models.ManyToManyField(TzcldProfile, related_name='orgs', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Organisation or Territory')
        verbose_name_plural = _("TZCLD Organisations or Territories")
        anonymous_perms = ['view']
        container_path = "tzcld-orgs/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:org"


class TzcldProfileRegion(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    tzcldprofile = models.ManyToManyField(TzcldProfile, related_name='regions', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Region or departement')
        verbose_name_plural = _("TZCLD Regions or departements")
        anonymous_perms = ['view']
        container_path = "tzcld-regions/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:regions"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_tzcld_profile(sender, instance, created, **kwargs):
    if not Model.is_external(instance):
        TzcldProfile.objects.get_or_create(user=instance)


# DjangoLDP Community Extension

class TzcldTerritoriesKind(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Territory Kind')
        verbose_name_plural = _("TZCLD Territories Kind")
        anonymous_perms = ['view']
        container_path = "tzcld-kinds/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "tzcld:territoryKind"

class TzcldCommunity(Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='tzcld_profile', null=True, blank=True)
    features = models.CharField(max_length=255, blank=True, null=True, default='')
    region = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_mail_1 = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_mail_2 = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_mail_3 = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_last_name = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_first_name = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_job = models.CharField(max_length=255, blank=True, null=True, default='')
    kind = models.ForeignKey(TzcldTerritoriesKind, on_delete=models.DO_NOTHING,related_name='kind', blank=True, null=True)
    membership = models.BooleanField(default=False)
    last_contribution_year = models.CharField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('TZCLD Community Profile')
        verbose_name_plural = _("TZCLD Communities Profiles")
        permission_classes = [TzcldCommunityProfilePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        ordering = ['community']
        container_path = "/tzcld-communities/"
        serializer_fields = ['@id', 'contact_first_name', 'contact_last_name', 'contact_job', 'kind', 'features', 'region', 'contact_mail_1', 'contact_mail_2', 'contact_mail_3', 'membership', 'last_contribution_year']
        rdf_type = "tzcld:communityProfile"
        depth = 3


@receiver(post_save, sender=Community)
def create_community_esa_profile(instance, created, **kwargs):
    if not Model.is_external(instance):
        TzcldCommunity.objects.get_or_create(community=instance)
