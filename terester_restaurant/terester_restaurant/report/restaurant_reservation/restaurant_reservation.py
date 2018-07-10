# Copyright (c) 2013, Bituls Company Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _

def execute(filters=None):
	return _execute(filters)


def get_conditions(filters):
    conditions = ""
    if filters.get("no_of_people"): conditions += " and no_of_people=%(no_of_people)s"
    # if filters.get("reservation_instructions"): conditions += " and reservation_instructions = %(reservation_instructions)s"

    if filters.get("reservation_time"): conditions += " and creation >= %(reservation_time)s"
    if filters.get("reservation_end_time"): conditions += " and creation <= %(reservation_end_time)s"

    if filters.get("customer"): conditions += " and customer = %(customer)s"

    return conditions

def _execute(filters):
    if not filters: filters = frappe._dict({})
    data = []
    columns = get_columns()
    reservation_list = get_reservation(filters)
    # msgprint(_(reservation_list))
    if not reservation_list:
        msgprint(_("No record found"))
        return columns, reservation_list
    extra_it_rate_map = get_extra_it_rate_map(reservation_list)
    for res in reservation_list:
        # msgprint(_(res.name))
        item = list(set(extra_it_rate_map.get(res.name, {}).get("item", [])))
        # rate = list(set(extra_it_rate_map.get(res.name, {}).get("rate", [])))
        row = [res.get("name"), res.get("contact_number"), res.get("restaurant"), res.get("customer"),
               res.get("customer_name"), res.get("no_of_people"), res.get("reservation_time"), res.get("reservation_end_time"),
               res.get("reservation_instructions")]

        row +=[ ", ".join(item)]
        data.append(row)
    return columns, data

def get_reservation(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql("""
		select name, contact_number, restaurant, customer, 
		customer_name, no_of_people, reservation_time, reservation_end_time,
		reservation_instructions
		from `tabRestaurant Reservation` 
		where docstatus = 0 %s order by creation desc""" % conditions, filters, as_dict=1)

def get_columns():
    """return columns based on filters"""
    columns =[
        _("Name") + ":Link/Restaurant Reservation:80", _("Contact Number") + "::80", _("Restaurant Name") + "::90", _("Customer") + ":Link/Customer:120",
        _("Customer Name") + "::120", _("Number of Peoples") + ":Int:100", _("Reservation Time") + "::120",
        _("End of Reservation") + "::120", _("Reservation Instructions ") + ":Long Text:180", _("Items") + "::130"
    ]
    return columns

def get_extra_it_rate_map(reservation_list):
    # msgprint(_(reservation_list))
    si_items = frappe.db.sql("""select parent, item
		from `tabRestaurant Order Entry Item` where parent in (%s)
		and (ifnull(item, '') != '')""" %
        ', '.join(['%s']*len(reservation_list)), tuple([res.name for res in reservation_list]), as_dict=1)

    extra_it_rate_map = {}
    for d in si_items:
        if d.item:
            extra_it_rate_map.setdefault(d.parent, frappe._dict()).setdefault(
                "item", []).append(d.item)
    # msgprint(_(extra_it_rate_map))
    return extra_it_rate_map
