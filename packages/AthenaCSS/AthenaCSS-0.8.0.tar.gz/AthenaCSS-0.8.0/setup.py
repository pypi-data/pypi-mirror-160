# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
import setuptools

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def readme_handler() -> str:
    with open("README.md", "r") as readme_file:
        return readme_file.read()

def version_handler() -> str:
    # ------------------------------------------------------------------------------------------------------------------
    version = 0,8,0 # <-- DEFINE THE VERSION IN A TUPLE FORMAT HERE
    # ------------------------------------------------------------------------------------------------------------------
    return ".".join(str(i) for i in version)

# ----------------------------------------------------------------------------------------------------------------------
# - Actual Setup -
# ----------------------------------------------------------------------------------------------------------------------
setuptools.setup(
    name="AthenaCSS",
    version=version_handler(),
    author="Andreas Sas",
    author_email="",
    description="CSS generator for Python",
    long_description=readme_handler(),
    long_description_content_type="text/markdown",
    url="https://github.com/DirectiveAthena/VerSC-AthenaCSS",
    project_urls={
        "Bug Tracker": "https://github.com/DirectiveAthena/VerSC-AthenaCSS/issues",
    },
    license="GPLv3",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "AthenaColor>=6.2.0",
        "AthenaLib>=1.4.0"
    ]
)