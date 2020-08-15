# class ResultDataTable(BaseDatatableView):
#     model = Result
#     columns = ['event.start_date_string', 'event.name', 'name', 'total_time_string', 'distance']
#
#     def get_initial_queryset(self):
#         return Result.objects.filter(event__isnull=False)
#
#     def filter_queryset(self, qs):
#         search = self.request.GET.get('search[value]', None)
#         qs_params = None
#         if search:
#             parts = search.split(' ')
#             for part in parts:
#                 q = Q(name__istartswith=part) | Q(event__name__istartswith=part)
#                 qs_params = qs_params | q if qs_params else q
#             qs = qs.filter(qs_params)
#
#         return qs

# @login_required
# def view_leaderboard(request):
#     template_name = 'private/leader_board.html'
#     distance = int(request.GET.get('distance', 2000))
#     lightweight = bool(request.GET.get('lightweight', False))
#
#     if lightweight:
#         qs = Profile.objects.filter(results_rowed__personal_record=True,
#                                     results_rowed__distance=distance,
#                                     results_rowed__lightweight=True,
#                                     ).values('first_name',
#                                              'last_name',
#                                              'id',
#                                              'results_rowed__lightweight',
#                                              ).annotate(pace=Min('results_rowed__pace')).order_by('pace')[:10]
#     else:
#         qs = Profile.objects.filter(results_rowed__personal_record=True,
#                                     results_rowed__distance=distance,
#                                     ).values('first_name',
#                                              'last_name',
#                                              'id',
#                                              'results_rowed__lightweight',
#                                              ).annotate(pace=Min('results_rowed__pace')).order_by('pace')[:10]
#
#     for i, result in enumerate(qs):
#         result['name'] = result['first_name'] + ' ' + result['last_name']
#         result['lightweight'] = result['results_rowed__lightweight']
#         result['rank'] = i + 1
#         total = result['pace'] * distance / 500
#         total_minutes, total_seconds = int(total // 60), total % 60
#         result['total_time_string'] = '{:02d}:{:06.3f}'.format(total_minutes, total_seconds)
#         result['distance'] = distance
#         minutes, seconds = int(result['pace'] // 60), result['pace'] % 60
#         result['pace_string'] = '{:02d}:{:06.3f}/500m'.format(minutes, seconds)
#
#     context = {'result_list': qs, }
#     return render(request, template_name, context)
