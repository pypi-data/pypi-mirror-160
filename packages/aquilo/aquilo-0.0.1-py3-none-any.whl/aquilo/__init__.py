from pathlib import Path

from aquilo.browser.elements.containers import *
from aquilo.browser.elements.typography import *
from aquilo.html import *
from aquilo.main import *
from aquilo.utils import has_special_char


def startproject(project_name: str):
    if has_special_char(project_name):
        raise ValueError("Project name cannot contain special characters.")

    if project_name == "aquilo":
        raise ValueError("Aquilo is a reserved name.")

    if " " in project_name:
        raise ValueError("Project name cannot contain spaces.")

    new_app_directory = Path(os.getcwd() + os.sep + project_name)

    if os.path.exists(new_app_directory):
        raise ValueError("Project %s already exists." % project_name)

    os.makedirs(new_app_directory)

    with open(f"{os.getcwd()}/manage.py", "w") as manage_file:
        manage_file.write(
            f"""#!/usr/bin/env python
\"\"\"Aquilo's command-line utility for administrative tasks.\"\"\"
import os
import sys


def main():
    \"\"\"Run administrative tasks.\"\"\"
    os.environ.setdefault(\"AQUILO_SETTINGS_MODULE\", \"{project_name}.config.settings\")
    os.environ.setdefault(\"AQUILO_APPS_MODULE\", \"{project_name}.apps\")

    try:
        from aquilo.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            \"Couldn't import Aquilo. Are you sure it's installed and \"
            \"available on your PYTHONPATH environment variable? Did you \"
            \"forget to activate a virtual environment?\"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == \"__main__\":
    main()
"""
        )

    with open(f"{os.getcwd()}/.gitignore", "w") as gitignore_file:
        gitignore_file.write(
            """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
build/

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
        """
        )

    with open(f"{os.getcwd()}/README.md", "w") as readme_file:
        readme_file.write(
            f"""# {project_name.capitalize()}

This is a new Aquilo project.
        """
        )

    with open(f"{os.getcwd()}/requirements.txt", "w") as requirements_file:
        requirements_file.write("aquilo")

    with open(f"{os.getcwd()}/{project_name}/__init__.py", "w") as init_file:
        init_file.write("")

    os.makedirs(f"{os.getcwd()}/{project_name}/apps")

    with open(f"{os.getcwd()}/{project_name}/apps/__init__.py", "w") as init_file:
        init_file.write("")

    os.makedirs(f"{os.getcwd()}/{project_name}/apps/home")
    with open(f"{os.getcwd()}/{project_name}/apps/home/__init__.py", "w") as init_file:
        init_file.write("")

    with open(f"{os.getcwd()}/{project_name}/apps/home/pages.py", "w") as pages:
        pages.write("""from aquilo import build, div, h1


def page_home():
    root = div(h1(\"Hello World!\"))
    return build(root, title=\"Hello World!\")
""")

    os.makedirs(f"{os.getcwd()}/{project_name}/config")

    with open(f"{os.getcwd()}/{project_name}/config/__init__.py", "w") as init_file:
        init_file.write("")

    with open(f"{os.getcwd()}/{project_name}/config/settings.py", "w") as settings_file:
        settings_file.write(
            f"""from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True

APPS = [
    "home",
]

ROOT_URLCONF = "{project_name}.config.urls"\n
"""
        )

    os.makedirs(f"{os.getcwd()}/{project_name}/libs")

    with open(f"{os.getcwd()}/{project_name}/libs/__init__.py", "w") as init_file:
        init_file.write("")

    try:
        os.system(f"git init")
    except:
        pass


def main():
    import sys

    if len(sys.argv) == 1:
        raise ValueError("No command specified.")

    command: str = sys.argv[1]
    if command == "startproject":
        try:
            startproject(sys.argv[2].lower())
        except IndexError:
            raise ValueError("No project name specified.")
    else:
        raise ValueError("Invalid command.")


if __name__ == "__main__":
    main()
