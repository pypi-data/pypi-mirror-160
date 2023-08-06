from types import NoneType
import click
import os
from typing import Union
from doc_wizard import gitlab_ci


def generateCi(theme, doc_dir):
    ci = gitlab_ci.gitlab_ci(theme, doc_dir)
    ci.addPages()
    ci.save()

    return


def generateDocs(name, autodoc, doc_dir):
    os.makedirs(doc_dir)
    origin = os.getcwd()
    os.chdir(doc_dir)
    os.system('pip install Sphinx')
    if autodoc is None:
        os.system(f'sphinx-quickstart -p {name} --sep -l en')
    else:
        os.system(f'sphinx-quickstart -p {name} --ext-autodoc --sep -l en')
        with open("source/conf.py", "r") as f:
            text = f.readlines()
        text[12] = 'import os'
        text[13] = 'import sys'
        text[14] = f"sys.path.insert(0, os.path.abspath('{origin}/{autodoc}'))"
        with open("source/conf.py", "w") as f:
            f.writelines(text)
    os.system('mv source/* .')
    os.chdir(origin)

    return


@click.command()
@click.option('-t', '--theme', default='alabaster',
              help='Specify the theme to use for the docs. \
                      Must be a pip-installable Sphinx theme. \
                      Defaults to "alabaster"')
@click.option('--no_template', is_flag=True,
              help='Set if you do not want a doc template to be \
                      generated. Set if you already have a Sphinx \
                      docs directory with documentation.')
@click.option('-d', '--doc_dir', default='docs',
              help='Directory in which doc templates will be \
                      generated. Defaults to "docs"')
@click.option('-n', '--name', default=os.path.split(os.getcwd())[1],
              help='The name of the project. It will be used in \
                      the template documentation. Defaults to \
                      the current working directory.')
@click.option('-a', '--autodoc', default=None,
              help='Directory where the modules are, relative to \
                      project base. If provided, autodoc will be \
                      enabled and Sphinx will parse the docstrings \
                      in the modules')
def parseOpts(theme: str,
              no_template: bool,
              doc_dir: str,
              name: str,
              autodoc: Union[str, NoneType]):
    generateCi(theme, doc_dir)
    if no_template:
        pass
    else:
        generateDocs(name, autodoc, doc_dir)

    return


if __name__ == "__main__":
    parseOpts()
