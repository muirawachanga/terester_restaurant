from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on transactions done on specified restaurant'),
		'fieldname': 'restaurant',
		'transactions': [
			{
				'label': _('Setup'),
				'items': ['Restaurant Menu', 'Restaurant Table']
			},
			{
				'label': _('Operations'),
				'items': ['Restaurant Reservation', 'Sales Invoice', 'Customer']
			}
		]
	}