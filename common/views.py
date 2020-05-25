from django.views.generic import ListView


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
