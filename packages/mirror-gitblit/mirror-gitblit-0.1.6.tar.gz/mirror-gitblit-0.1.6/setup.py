from setuptools import setup, find_packages
import pathlib, codecs, os, re

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string. [{}]".format(file_paths))


setup(
    name="mirror-gitblit",
    version= find_version("src/mirror_gitblit/__version__.py"),
    description="Tool to mirror repositories of a gitblit server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mathcoach.htwsaar.de",
    author="Hong-Phuc Bui",
    author_email="hong-phuc.bui@htwsaar.de",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests"]),
    install_requires=["tomli"],
    tests_require=['pytest', 'pytest-runner', 'pytest-cov'],
    setup_requires=["pytest", "pytest-runner"],
    entry_points = {
        "console_scripts" : [
            "list-gitblit-repos=mirror_gitblit.cli:list_repos"
        ]
    },
    include_package_data=True,
    zip_safe=False
)

