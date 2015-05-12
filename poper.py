#-*- coding: utf-8 -*-

"""
Poper

Tool to compare in deep two data structures.


Typical use:

	import poper

	book_model = {
		'title': 'The Legend of Zelda',
		'pages': 334,
		'editions': [
			{
				'name': 'Gold',
				'year': 1999,
			},
		],
	}

	book_to_check = {
		'title': 'Exit the Matrix',
		'pages': 333,
		'year': 2001,     # Notice: field `year` does not match the model
	}

	c = poper.Checker()
	valid = c.check(book_model, book_to_check)
	print c.error  # will print: `YOUR_DICT.year` is not allowed


Asterisk keys:

Poper also works with asterisk keys. The following example force `editions.year`
to be integer AND for example `editions.custom_comment` to be string.

	book_model = {
		'title': 'The Legend of Zelda',
		'pages': 334,
		'editions': {
			'*': 'custom field',
			'year': 1999,
		}
	}


Run tests:

	python poper_test.py

"""

import types


class Checker:

	def check(self, model, test):
		self.error = None

		return self.check_item(model, test, 'YOUR_DICT')

	def check_type(self, model, test, trace):
		model_type = type(model)
		test_type = type(test)

		if model_type != test_type:
			self.error = "`%s` should be type `%s` instead of `%s`" % (trace, model_type.__name__, test_type.__name__)
			return False

		return True

	def check_dict(self, model, test, trace):
		for k,v in test.iteritems():
			item_check = False
			if k in model:
				item_check = self.check_item(model[k], test[k], trace + '.' + k)
			elif '*' in model:
				item_check = self.check_item(model['*'], test[k], trace + '.' + k)
			else:
				self.error = "`%s.%s` is not allowed" % (trace, k)

			if item_check is False:
				return False

		return True

	def check_list(self, model, test, trace):
		for k,v in enumerate(test):
			if self.check_item(model[0], test[k], '%s[%s]' %(trace, k)) is False:
				return False

		return True

	def check_item(self, model, test, trace):
		if self.check_type(model, test, trace) is False:
			return False

		t = type(model).__name__
		if 'dict' == t:
			return self.check_dict(model, test, trace)
		elif 'list' == t:
			return self.check_list(model, test, trace)

		return True

