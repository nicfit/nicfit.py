from collections import namedtuple


def __parse_version(v):                                       # pragma: nocover
    ver, rel = v, "final"
    for c in ("a", "b", "c"):
        parsed = v.split(c)
        if len(parsed) == 2:
            ver, rel = (parsed[0], c + parsed[1])

    v = tuple((int(v) for v in ver.split(".")))
    ver_info = namedtuple("Version", "major, minor, maint, release")(
        *(v + (tuple((0,)) * (3 - len(v))) + tuple((rel,))))
    return ver, rel, ver_info


__version__ = "{{ cookiecutter.version }}"
__release_name__ = ""
__years__ = "{{ cookiecutter.year }}"

_, __release__, __version_info__ = __parse_version(__version__)
__project_name__ = "{{ cookiecutter.project_name }}"
__project_slug__ = "{{ cookiecutter.project_slug }}"
__pypi_name__ = "{{ cookiecutter.pypi_repo_name }}"
__author__ = "{{ cookiecutter.full_name }}"
__author_email__ = "{{ cookiecutter.email }}"
__url__ = "{{ cookiecutter.web }}"
__description__ = "{{ cookiecutter.project_short_description }}"
__long_description__ = "{{ cookiecutter.project_long_description }}"
__license__ = "{{ cookiecutter.license }}"
__github_url__ = "https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}",
__version_txt__ = """
%(__name__)s %(__version__)s (C) Copyright %(__years__)s %(__author__)s
This program comes with ABSOLUTELY NO WARRANTY! See LICENSE for details.
Run with --help/-h for usage information or read the docs at
%(__url__)s
""" % (locals())
