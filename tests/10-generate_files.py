#!/usr/bin/python


def test_generateTemplate():
  parameters = {
    'list':[
      1,
      2,
      3
    ]
  }
  template_text = '''This is a test.
{% for l in list %}{{ l }}
{% endfor %}'''
  import FileGen
  import yaml
  import os
  with open('test.jn2','w') as f:
    f.write(template_text)
  with open('test.yml','w') as f:
    f.write(yaml.dump(parameters))
  template = FileGen.Template(filepath='test.jn2')
  params   = FileGen.Parameters(filepaths=['test.yml'])
  result   = template.render(params=params.params)
  os.remove('test.yml')
  os.remove('test.jn2')
  return(result)


def test_generateTemplateConfirmOutput():
  generated = test_generateTemplate()
  test_string = '''This is a test.
1
2
3
'''
  assert generated == test_string


print test_generateTemplateConfirmOutput()