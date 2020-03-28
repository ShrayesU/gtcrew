from tastypie.resources import ModelResource

from team.models import Profile


class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        excludes = ['email', 'birthday']
        allowed_methods = ['get']

# could add below to settings.py
# TASTYPIE_DEFAULT_FORMATS = ['json', 'xml']
