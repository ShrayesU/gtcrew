from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, UpdateView
from django.views.generic.base import ContextMixin

from team.models import Profile


class RequireProfileExistsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(RequireProfileExistsMixin, self).get_context_data(**kwargs)

        # permissions
        allowed_to_edit = False
        if self.request.user.is_staff:
            allowed_to_edit = True
        elif Profile.objects.filter(owner=self.request.user).exists():
            # user_owns_profile = self.request.user.profile == self.object.created_by
            # profile_approved = self.object.created_by.status == APPROVED
            allowed_to_edit = True  # user_owns_profile and profile_approved

        context.update({'allowed_to_edit': allowed_to_edit})

        return context


class RequireProfileExistsUpdateView(RequireProfileExistsMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(RequireProfileExistsUpdateView, self).get_context_data(**kwargs)

        allowed_to_edit = context.get('allowed_to_edit', '')
        if not allowed_to_edit:
            messages.warning(self.request, 'You do not have permission to edit %s' % self.object)
            raise PermissionDenied


class PagesListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(PagesListView, self).get_context_data(**kwargs)

        # custom pagination numbers/pages
        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number
        max_shown = 7  # odd number

        if num_pages <= max_shown or page_no <= (max_shown // 2 + 1):
            pages = [x for x in range(1, min(num_pages + 1, max_shown + 1))]
        elif page_no > num_pages - (max_shown // 2 + 1):
            pages = [x for x in range(num_pages - max_shown + 1, num_pages + 1)]
        else:
            pages = [x for x in range(page_no - max_shown // 2, page_no + max_shown // 2 + 1)]

        context.update({'pages': pages})
        return context
