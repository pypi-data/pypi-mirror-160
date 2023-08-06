from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from djangoldp.models import Model
from djangoldp_community.models import Community
from djangoldp_esa.permissions import EsaCommunityProfilePermissions


class EsaCommunityRole(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('ESA Role')
        verbose_name_plural = _("ESA Roles")
        anonymous_perms = ['view']
        container_path = "esa-roles/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "sib:EsaRole"


class EsaBicPosition(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('ESA-BIC Position')
        verbose_name_plural = _("ESA-BIC Positions")
        anonymous_perms = ['view']
        container_path = "esa-positions/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "sib:EsaBicPosition"


class EsaBicLocation(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('ESA-BIC Location')
        verbose_name_plural = _("ESA-BIC Locations")
        anonymous_perms = ['view']
        container_path = "esa-locations/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "sib:EsaBicLocation"


STATUS_CHOICES = [
    ('Incubation', 'Incubation'),
    ('Alumni', 'Alumni'),
    ('Other', 'Other')
]


class EsaCommunity(Model):
    community = models.OneToOneField(
        Community, on_delete=models.CASCADE, related_name='esa_profile', null=True, blank=True)
    main_contact_first_name = models.CharField(
        max_length=255, blank=True, null=True, default='')
    main_contact_last_name = models.CharField(
        max_length=255, blank=True, null=True, default='')
    role = models.ForeignKey(EsaCommunityRole, on_delete=models.DO_NOTHING,
                             related_name='tags', blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Other', null=True, blank=True)
    graduation_year = models.CharField(
        max_length=255, blank=True, null=True, default='')
    position_esa_bic = models.ForeignKey(
        EsaBicPosition, on_delete=models.DO_NOTHING, related_name='position_bic', blank=True, null=True)
    location_esa_bic = models.ForeignKey(
        EsaBicLocation, on_delete=models.DO_NOTHING, related_name='location_bic', blank=True, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('ESA Profile')
        verbose_name_plural = _("ESA Profiles")
        permission_classes = [EsaCommunityProfilePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        ordering = ['community']
        container_path = "/esaprofiles/"
        serializer_fields = ['@id', 'main_contact_first_name', 'main_contact_last_name', 'tags',
                             'role', 'sectors', 'spaces', 'status', 'graduation_year', 'position_esa_bic', 'location_esa_bic']
        rdf_type = "sib:CommunityEsaProfile"
        depth = 1


class EsaCommunityTag(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    esacommunity = models.ManyToManyField(
        EsaCommunity, related_name='tags', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('ESA Tag')
        verbose_name_plural = _("ESA Tags")
        anonymous_perms = ['view']
        container_path = "esa-tags/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "sib:EsaTag"


class EsaCommunitySector(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    esacommunity = models.ManyToManyField(
        EsaCommunity, related_name='sectors', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('ESA Sector')
        verbose_name_plural = _("ESA Sectors")
        anonymous_perms = ['view']
        container_path = "esa-sectors/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "sib:EsaSector"


class EsaCommunitySpace(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default='')
    esacommunity = models.ManyToManyField(
        EsaCommunity, related_name='spaces', blank=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('ESA Space')
        verbose_name_plural = _("ESA Spaces")
        anonymous_perms = ['view']
        container_path = "esa-spaces/"
        serializer_fields = ['@id', 'name']
        nested_fields = []
        rdf_type = "sib:EsaSpace"


@receiver(post_save, sender=Community)
def create_community_esa_profile(instance, created, **kwargs):
    if not Model.is_external(instance):
        EsaCommunity.objects.get_or_create(community=instance)
