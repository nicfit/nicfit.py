import re
import sys


MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
module_name = "{{ cookiecutter.py_module }}"

if not re.match(MODULE_REGEX, module_name):
    print("ERROR: The project slug (%s) is not a valid." % module_name)
    # Exit to cancel project
    sys.exit(1)

user_config = """
default_context:
    add_docs: "{{ cookiecutter.add_docs }}"
    bitbucket_repo: "{{ cookiecutter.bitbucket_repo }}"
    bitbucket_url: "{{ cookiecutter.bitbucket_url }}"
    bitbucket_username: "{{ cookiecutter.bitbucket_username }}"
    default_locale: "{{ cookiecutter.default_locale }}"
    email: "{{ cookiecutter.email }}"
    full_name: "{{ cookiecutter.full_name }}"
    gettext_domain: "{{ cookiecutter.gettext_domain }}"
    github_repo: "{{ cookiecutter.github_repo }}"
    github_url: "{{ cookiecutter.github_url }}"
    github_username: "{{ cookiecutter.github_username }}"
    intended_audience: "{{ cookiecutter.intended_audience }}"
    license: "{{ cookiecutter.license }}"
    project_long_description: "{{ cookiecutter.project_long_description }}"
    project_name: "{{ cookiecutter.project_name }}"
    project_short_description: "{{ cookiecutter.project_short_description }}"
    project_slug: "{{ cookiecutter.project_slug }}"
    py26: "{{ cookiecutter.py26 }}"
    py27: "{{ cookiecutter.py27 }}"
    py33: "{{ cookiecutter.py33 }}"
    py34: "{{ cookiecutter.py34 }}"
    py35: "{{ cookiecutter.py35 }}"
    py36: "{{ cookiecutter.py36 }}"
    py37: "{{ cookiecutter.py37 }}"
    py_module: "{{ cookiecutter.py_module }}"
    pyapp_type: "{{ cookiecutter.pyapp_type }}"
    pypi_repo_name: "{{ cookiecutter.pypi_repo_name }}"
    pypi_username: "{{ cookiecutter.pypi_username }}"
    pypy: "{{ cookiecutter.pypy }}"
    pypy3: "{{ cookiecutter.pypy3 }}"
    release_date: "{{ cookiecutter.release_date }}"
    requirements_yaml: "{{ cookiecutter.requirements_yaml }}"
    src_dir: "{{ cookiecutter.src_dir }}"
    use_bitbucket: "{{ cookiecutter.use_bitbucket }}"
    use_github: "{{ cookiecutter.use_github }}"
    use_make: "{{ cookiecutter.use_make }}"
    use_paver: "{{ cookiecutter.use_paver }}"
    use_pypi_deployment_with_travis: "{{ cookiecutter.use_pypi_deployment_with_travis }}"
    use_pytest: "{{ cookiecutter.use_pytest }}"
    use_rtd: "{{ cookiecutter.use_rtd }}"
    use_travis_ci: "{{ cookiecutter.use_travis_ci }}"
    version: "{{ cookiecutter.version }}"
    web: "{{ cookiecutter.web }}"
    year: "{{ cookiecutter.year }}"
"""

with open(".cookiecutter.yml", "w") as fp:
    fp.write(user_config)
