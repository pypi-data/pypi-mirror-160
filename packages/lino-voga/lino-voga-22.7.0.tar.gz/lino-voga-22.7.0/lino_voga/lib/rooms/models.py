# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
The :xfile:`models` module of the :mod:`lino_voga.rooms` app.

"""

from lino.utils.mti import get_child
from lino_xl.lib.rooms.models import *
from lino.api import rt
from lino_xl.lib.invoicing.mixins import InvoiceGenerator

# sales = dd.resolve_app('sales')


class Booking(Booking, InvoiceGenerator):

    # invoiceable_date_field = 'start_date'

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        qs = super(Booking, cls).get_generators_for_plan(plan, partner)
        # qs = cls.objects.all()
        # filter(**{
        #     cls.invoiceable_date_field + '__lte': plan.max_date or plan.today})

        if partner is None:
            partner = plan.partner
        if partner:
            company = get_child(partner, rt.models.contacts.Company)
            if company:
                qs = qs.filter(company=company)
            else:
                return cls.objects.none()
        return qs.order_by('id')

    def get_invoiceable_product(self, max_date=None):
        # max_date = plan.max_date or plan.today
        if max_date and self.start_date > max_date:
            return
        if self.company and self.room:
            # if self.get_invoicings().count() > 0:
            if self.invoicings.count() > 0:
                return
            # if self.company != settings.SITE.site_config.site_company:
            return self.room.fee

    # def get_invoiceable_title(self, invoice=None):
        # if self.organizer:
            # return unicode(self.room)

    def get_invoiceable_qty(self):
        return self.max_events or 1
