#-*- coding: utf-8 -*-

import poper

tests = []

def test(f):
	tests.append(f)

def result(model, test, expected_result, expected_error=None, print_error=False):
	c = poper.Checker()
	result = c.check(model, test)
	if print_error:
		print c.error
	return result == expected_result and c.error == expected_error

@test
def test_unexisting_dict_keys():
	model = {}
	test = {'not exists': None}
	return result(model, test, False, '`YOUR_DICT.not exists` is not allowed')

@test
def test_existing_dict_keys():
	model = {'name': 'fulano'}
	test = {'name': 'fulana'}
	return result(model, test, True)

@test
def test_type_should_be_bool():
	model = {'key': True}
	test = {'key': 1}
	return result(model, test, False, '`YOUR_DICT.key` should be type `bool` instead of `int`')

@test
def test_nested_dict():
	model = {'key': {'one': 1, 'two': 2}}
	test = {'key': {'one': 2}}
	return result(model, test, True)

@test
def test_nested_list_ok():
	model = {'key': [{'name': 'fulano'}]}
	test = {'key': [ {'name': 'a'}, {'name': 'b'} ]}
	return result(model, test, True)

@test
def test_nested_list_fail():
	model = {'key': [{'name': 'fulano'}]}
	test = {'key': [ {'name': 'a'}, {'name': 'b', 'age': 77} ]}
	return result(model, test, False, '`YOUR_DICT.key[1].age` is not allowed')

@test
def test_asterisk_key_ok():
	model = {
		'clients': {
			'*': {
				'enabled': False,
				'name': 'fulanito',
			}
		}
	}

	test = {
		'clients': {
			'Asdf5a19sdf': {
				'enabled': False,
			}
		}
	}
	return result(model, test, True)

@test
def test_asterisk_key_nok():
	model = {
		'clients': {
			'*': {
				'enabled': False,
				'name': 'fulanito',
			}
		}
	}

	test = {
		'clients': {
			'Asdf5a19sdf': {
				'enabled': 'green',
			}
		}
	}
	return result(model, test, False, '`YOUR_DICT.clients.Asdf5a19sdf.enabled` should be type `bool` instead of `str`')


@test
def test_combine_asterisk_and_literals_nok():
	model = {
		'enabled': True,
		'*': 'my string value'
	}

	test = {
		'enabled': 'Green'
	}
	return result(model, test, False, '`YOUR_DICT.enabled` should be type `bool` instead of `str`')

@test
def test_combine_asterisk_and_literals_ok():
	model = {
		'enabled': True,
		'*': 'my string value'
	}

	test = {
		'enabled': True,
		'my-custom-key': 'the string thing',
	}
	return result(model, test, True)

@test
def test_documentation_example():
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
	error = c.error

	return result(book_model, book_to_check, False, '`YOUR_DICT.year` is not allowed')



def test_runner(test_list):
	for test in test_list:
		print '#', test.__name__
		if test() is False:
			return False
	return True


if test_runner(tests):
	print 'PASS'
else:
	print 'FAIL'