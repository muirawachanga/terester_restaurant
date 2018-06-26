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
    data = []
    columns = get_columns()
    reservation_list = get_reservation(filters)
    # msgprint(_(reservation_list))
    for res in reservation_list:
        row = [res.get("creation"), res.get("contact_number"), res.get("restaurant"), res.get("customer"),
               res.get("customer_name"), res.get("no_of_people"), res.get("reservation_time"), res.get("reservation_end_time"),
               res.get("reservation_instructions"), res.get("items")]
        data.append(row)
    return columns, data

def get_reservation(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql("""
		select creation, contact_number, restaurant, customer, 
		customer_name, no_of_people, reservation_time, reservation_end_time,
		reservation_instructions, items
		from `tabRestaurant Reservation` 
		where docstatus = 0 %s order by creation desc""" % conditions, filters, as_dict=1)

def get_columns():
    """return columns based on filters"""
    columns =[
        _("Creation Date") + "::80", _("Contact Number") + "::80", _("Restaurant Name") + "::90", _("Customer") + ":Link/Customer:120",
        _("Customer Name") + "::120", _("Number of Peoples") + ":Int:100", _("Reservation Time") + "::120",
        _("End of Reservation") + "::120", _("Reservation Instructions ") + ":Long Text:180", _("Items") + ":Table/Restaurant Menu Item:120"

    ]
    return columns