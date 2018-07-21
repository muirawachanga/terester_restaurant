# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import _
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate

class RestaurantOrderEntry(Document):
	pass

@frappe.whitelist()
def get_invoice(table):
	'''returns the active invoice linked to the given table'''
	invoice_name = frappe.get_value('Sales Invoice', dict(restaurant_table = table, docstatus=0))
	restaurant, menu_name = get_restaurant_and_menu_name(table)
	if invoice_name:
		invoice = frappe.get_doc('Sales Invoice', invoice_name)
	else:
		invoice = frappe.new_doc('Sales Invoice')
		invoice.naming_series = frappe.db.get_value('Restaurant', restaurant, 'invoice_series_prefix')
		invoice.is_pos = 1
		default_customer = frappe.db.get_value('Restaurant', restaurant, 'default_customer')
		if not default_customer:
			frappe.throw(_('Please set default customer in Restaurant Settings'))
		invoice.customer = default_customer

	invoice.taxes_and_charges = frappe.db.get_value('Restaurant', restaurant, 'default_tax_template')
	invoice.selling_price_list = frappe.db.get_value('Price List', dict(restaurant_menu=menu_name, enabled=1))

	return invoice

@frappe.whitelist()
def sync(table, items):
	'''Sync the sales order related to the table'''
	invoice = get_invoice(table)
	items = json.loads(items)

	invoice.items = []
	invoice.restaurant_table = table
	for d in items:
		invoice.append('items', dict(
			item_code = d.get('item'),
			qty = d.get('qty')
		))
	# msgprint(_(invoice))
	invoice.save()
	return invoice.as_dict()

@frappe.whitelist()
def make_invoice(table, customer, mode_of_payment, money):
	'''Make table based on Sales Order'''
	restaurant, menu = get_restaurant_and_menu_name(table)
	invoice = get_invoice(table)
	invoice.customer = customer
	invoice.restaurant = restaurant
	invoice.calculate_taxes_and_totals()
	invoice.append('payments', dict(mode_of_payment=mode_of_payment, amount=money))
	invoice.save()
	invoice.submit()

	frappe.msgprint(_('Invoice Created'), indicator='green', alert=True)

	return invoice.name

def item_query_restaurant(doctype='Item', txt='', searchfield='name', start=0, page_len=20, filters=None, as_dict=False):
	'''Return items that are selected in active menu of the restaurant'''
	restaurant, menu = get_restaurant_and_menu_name(filters['table'])
	# frappe.msgprint(_(menu))
	items = frappe.db.get_all('Restaurant Menu Item', ['item'], dict(parent = menu))
	# frappe.msgprint(_(items))
	del filters['table']
	filters['name'] = ('in', [d.item for d in items])

	return item_query('Item', txt, searchfield, start, page_len, filters, as_dict)

def get_restaurant_and_menu_name(table):
	if not table:
		frappe.throw(_('Please select a table'))

	restaurant = frappe.db.get_value('Restaurant Table', table, 'restaurant')
	menu = frappe.db.get_value('Restaurant', restaurant, 'active_menu')

	if not menu:
		frappe.throw(_('Please set an active menu for Restaurant {0}').format(restaurant))

	return restaurant, menu

def item_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	conditions = []

	description_cond = ''
	if frappe.db.count('Item') < 50000:
		# scan description only if items are less than 50000
		description_cond = 'or tabItem.description LIKE %(txt)s'

	return frappe.db.sql("""select tabItem.name,
		if(length(tabItem.item_name) > 40,
			concat(substr(tabItem.item_name, 1, 40), "..."), item_name) as item_name,
		tabItem.item_group,
		if(length(tabItem.description) > 40, \
			concat(substr(tabItem.description, 1, 40), "..."), description) as decription
		from tabItem
		where tabItem.docstatus < 2
			and tabItem.has_variants=0
			and tabItem.disabled=0
			and (tabItem.end_of_life > %(today)s or ifnull(tabItem.end_of_life, '0000-00-00')='0000-00-00')
			and (tabItem.`{key}` LIKE %(txt)s
				or tabItem.item_group LIKE %(txt)s
				or tabItem.item_name LIKE %(txt)s
				or tabItem.barcode LIKE %(txt)s
				{description_cond})
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, item_name), locate(%(_txt)s, item_name), 99999),
			idx desc,
			name, item_name
		limit %(start)s, %(page_len)s """.format(
		key=searchfield,
		fcond=get_filters_cond(doctype, filters, conditions).replace('%', '%%'),
		mcond=get_match_cond(doctype).replace('%', '%%'),
		description_cond = description_cond),
		{
			"today": nowdate(),
			"txt": "%%%s%%" % txt,
			"_txt": txt.replace("%", ""),
			"start": start,
			"page_len": page_len
		}, as_dict=as_dict)
