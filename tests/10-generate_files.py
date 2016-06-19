#!/usr/bin/python
parameters = {
  'list':[
    1,
    2,
    3
  ]
}
template = '''
This is a test.
{% for l in list %}
{{ l }}
{% endfor %}
'''