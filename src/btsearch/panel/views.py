# -*- coding: utf-8 -*-
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from ..bts import models
from . import forms


class IndexView(generic.TemplateView):
    template_name = 'panel/index.html'


class LocationView(generic.UpdateView):
    template_name = 'panel/location.html'
    model = models.Location
    form_class = forms.LocationEditForm
    context_object_name = 'location'

    def get_object(self, queryset=None):
        """
        When creating a new object, return None which tells generic Django
        the view should emulate generic.CreateView.
        Inspiration taken from:
        https://github.com/tangentlabs/django-oscar/blob/master/oscar/apps/dashboard/catalogue/views.py#L188
        """
        self.creating = not 'pk' in self.kwargs
        if self.creating:
            return None
        return super(LocationView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        ctx = super(LocationView, self).get_context_data(**kwargs)
        if not self.creating:
            ctx['base_stations'] = self.object.get_associated_objects()
        return ctx

    def form_invalid(self, form):
        messages.warning(self.request, 'Formularz zawiera błędy')
        return super(LocationView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, 'Rekord zachowano poprawnie')
        return reverse('panel:location-edit-view', kwargs={'pk': self.object.id})


class BaseStationView(generic.UpdateView):
    template_name = 'panel/basestation.html'
    model = models.BaseStation
    form_class = forms.BaseStationEditForm
    context_object_name = 'base_station'

    def get_form_kwargs(self):
        kwargs = super(BaseStationView, self).get_form_kwargs()
        if self.creating and self.request.GET.get('location'):
            kwargs.update({
                'initial': {
                    'location': self.request.GET.get('location')
                }
            })
        return kwargs

    def get_object(self, queryset=None):
        """
        When creating a new object, return None which tells generic Django
        the view should emulate generic.CreateView.
        Inspiration taken from:
        https://github.com/tangentlabs/django-oscar/blob/master/oscar/apps/dashboard/catalogue/views.py#L188
        """
        self.creating = not 'pk' in self.kwargs
        if self.creating:
            return None
        return super(BaseStationView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        ctx = super(BaseStationView, self).get_context_data(**kwargs)
        if not self.creating:
            ctx['cell_formset'] = forms.BaseStationCellsFormSet(
                instance=self.object,
                queryset=models.Cell.objects.order_by('standard', '-band', 'ua_freq', 'cid')
            )
        return ctx

    def form_valid(self, form):
        if not self.creating:
            # If not creating a new BaseStation record, validate the formset
            cell_formset = forms.BaseStationCellsFormSet(self.request.POST,
                                                         instance=self.object)
            if not cell_formset.is_valid():
                return self.form_invalid(form)
            cell_formset.save()

        return super(BaseStationView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Formularz zawiera błędy')
        return super(BaseStationView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, 'Rekord zachowano poprawnie')
        return reverse('panel:basestation-edit-view', kwargs={'pk': self.object.id})
