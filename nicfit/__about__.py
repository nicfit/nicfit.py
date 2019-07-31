import dataclasses

project_name = "nicfit.py"
version      = "0.8.4"
release_name = ""
author       = "Travis Shirk"
author_email = "travis@pobox.com"
years        = "2016-2019"

@dataclasses.dataclass
class Version:
    major: int
    minor: int
    maint: int
    release: str
    release_name: str

version_info = Version(0, 8, 4, "final", "")