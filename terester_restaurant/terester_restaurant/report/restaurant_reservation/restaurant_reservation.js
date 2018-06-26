// Copyright (c) 2016, Bituls Company Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Restaurant Reservation"] = {
		"filters": [
    		{
    			"fieldname":"reservation_time",
    			"label": __("From Date"),
    			"fieldtype": "Datetime",
    			"default": "",
    			"width": "80"
    		},
    		{
    			"fieldname":"reservation_end_time",
    			"label": __("To Date"),
    			"fieldtype": "Datetime",
    			"default": ""
    		},
    		{
    			"fieldname":"customer",
    			"label": __("Customer"),
    			"fieldtype": "Link",
    			"options": "Customer"
    		},
    		{
    		    "fieldname":"no_of_people",
    		    "label":__("Number of people"),
    		    "fieldtype":"Int"
    		}

	]
}
