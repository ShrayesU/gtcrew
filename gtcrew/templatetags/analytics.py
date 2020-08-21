from django import template
from django.conf import settings

register = template.Library()


class ShowGoogleAnalyticsJS(template.Node):
    def render(self, context):
        code = getattr(settings, "GOOGLE_ANALYTICS_CODE", False)
        if not code:
            return "<!-- Goggle Analytics not included since no settings.GOOGLE_ANALYTICS_CODE variable! -->"

        if 'user' in context and context['user'] and context['user'].is_staff:
            return "<!-- Goggle Analytics not included because you are a staff user! -->"

        if settings.DEBUG:
            return "<!-- Goggle Analytics not included because you are in Debug mode! -->"

        return """
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-176028500-1"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', '""" + str(code) + """');
        </script>
        """


def googleanalyticsjs(parser, token):
    return ShowGoogleAnalyticsJS()


show_common_data = register.tag(googleanalyticsjs)
