from __future__ import unicode_literals

from frappe import _


def get_data():
    return [
        {
            "label": _("Documents"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Restaurant",
                    "description": _("Create Restaurant")
                },
                {
                    "type": "doctype",
                    "name": "Restaurant Reservation",
                    "description": _("Create Restaurant reservations")
                }
            ]
        },
        {
            "label": _("Setup"),
            "icon": "icon-cog",
            "items": [

                {
                    "type": "doctype",
                    "name": "Restaurant Menu",
                    "description": _("Create Restaurant Menu.")
                },
                {
                    "type": "doctype",
                    "name": "Restaurant Table",
                    "description": _("Create Tables.")
                },
                {
                    "type": "doctype",
                    "name": "Restaurant Order Entry",
                    "description": _("Create Orders.")
                }
            ]
        },
        {
            "label": _("Standard Reports"),
            "icon": "icon-list",
            "items": [
                {
                    "type": "report",
                    "name": "Restaurant Reservation",
                    "is_query_report": True,
                    "doctype": "Restaurant Reservation"
                }
            ]
        },
        {
            "label": _("Help"),
            "icon": "icon-facetime-video",
            "items": [

            ]
        }
    ]
