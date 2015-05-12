# Poper

Python structures validator based on example

## Typical use

```
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
```

## Asterisk keys

Poper also works with asterisk keys. The following example force `editions.year`
to be integer AND for example `editions.custom_comment` to be string.

```
book_model = {
	'title': 'The Legend of Zelda',
	'pages': 334,
	'editions': {
		'*': 'custom field',
		'year': 1999,
	}
}
```

## Run tests

```
python poper_test.py
```
