#!/usr/bin/python
import os
import ast
import json
import yaml
import jinja2
import argparse
import commands


## Exceptions
class FileNotFound(Exception):
  pass
class CommandFailed(Exception):
  pass


class Utils:
  def update_tree(self,data,function,namespace=None):
    assert not data == None
    assert not function == None
    if namespace == None:
      namespace = data
    if type(data) == type({}):
      for n in data:
        data[n] = self.update_tree(data[n],function,namespace)
    elif type(data) == type([]):
      c = 0
      for i in data:
        data[c] = self.update_tree(i,function,namespace)
        c += 1
    else:
      print data
      print namespace
      data = function(data,namespace)
    return(data)

## Params
class Parameters:

  filepaths      = None
  debug          = None
  ignore_cmd_err = None
  params         = None


  def __init__(self,filepaths,ignore_cmd_err=False,debug=False):
    self.filepaths = filepaths
    self.debug = debug
    self.ignore_cmd_err = ignore_cmd_err
    self.utils = Utils()


  def load(self,filepaths):
    params = {}
    for i in filepaths:
      try:
        assert os.path.isfile(i)
      except Exception as e:
        raise FileNotFound('Cannot find file {}'.format(i))
        print(e)
      with open(i,'r') as f:
        param_text = f.read()
      try:
        p = yaml.load(param_text)
        params = dict(params, **p)
      except:
        p = json.loads(param_text)
        self.params = dict(params, **p)


  def resolve_tree(self,data,namespace):
    print data
    print namespace
    data = str(data)
    data = jinja2.Environment().from_string(data).render(namespace)
    try:
      data = ast.literal_eval(data)
    except:
      pass
    if type(data) == type(u''):
      if data.startswith('<[') and data.endswith(']>'):
        cmd = data.lstrip('<[').rstrip(']>')
        status = commands.getstatusoutput(cmd)
        if not self.ignore_cmd_err:
          try:
            assert status[0] == 0
          except:
            raise CommandFailed('Command "{}" exited with a nonzero value!'.format(cmd))
        data = status[-1]
    return(data)


  def resolveYAMLJinja(self,data,evals=25):
    for i in range(0,evals):
      data = self.utils.update_tree(data,self.resolve_tree)
    return(data)



## Template
class Template:
  template_text  = None
  ignore_cmd_err = None
  debug = None


  def __init__(self,filepath,ignore_cmd_err=False,debug=False):
    self.ignore_cmd_err = ignore_cmd_err
    self.debug          = debug
    self.load(filepath)
    self.utils = Utils()


  def load(self,filepath):
    try:
      assert os.path.isfile(filepath)
    except Exception as e:
      raise FileNotFound('Cannot find file {}'.format(filepath))
      print(e)
    with open(filepath,'r') as f:
      self.template_text = f.read()


  def render_jinja(self,data,namespace):
    data = str(data)
    data = jinja2.Environment().from_string(data).render(namespace)
    try:
      data = ast.literal_eval(data)
    except:
      pass
    if type(data) == type(u''):
      if data.startswith('<[') and data.endswith(']>'):
        cmd = data.lstrip('<[').rstrip(']>')
        status = commands.getstatusoutput(cmd)
        if not self.ignore_cmd_err:
          try:
            assert status[0] == 0
          except:
            raise CommandFailed('Command "{}" exited with a nonzero value!'.format(cmd))
        data = status[-1]
    return(data)


  def resolveYAMLJinja(self,data,evals=25):
    for i in range(0,evals):
      data = self.utils.update_tree(data,self.render_jinja)
    return(data)


  def render(self,params):
    ## Render template
    params = self.resolveYAMLJinja(params)
    render = jinja2.Environment().from_string(self.template_text).render(params)
    if self.debug:
      print('{}'.format(json.dumps(params,indent=2)))
    else:
      print(render)




## Shell
class Shell:
  results = None
  def __init__(self):
    parser = argparse.ArgumentParser(description='Generic file template generator')
    parser.add_argument('--template', '-t',             action="store",      dest="template_path",  default=False, help='Path to template file',                required = True)
    parser.add_argument('--parameters', '-p',           action="store",      dest="param_paths",    default=False, help='Path to parameter file(s)', nargs='*', required = True)
    parser.add_argument('--debug', '-d',                action="store_true", dest="debug",          default=False, help='Show the params')
    parser.add_argument('--ignore-command-error', '-i', action="store_true", dest="ignore_cmd_err", default=False, help='Allows the tool to ignore nonzero exit codes on <[metacommands]>')
    parser.add_argument('--version', action='version',  version='%(prog)s 1.0')
    self.results = parser.parse_args()
    template     = Template(filepath=self.results.template_path,ignore_cmd_err=self.results.ignore_cmd_err)
    params       = Parameters(filepaths=self.results.param_paths,ignore_cmd_err=self.results.ignore_cmd_err)
    print template.render(params=params.params)


def shell_start():
  shell = Shell()


