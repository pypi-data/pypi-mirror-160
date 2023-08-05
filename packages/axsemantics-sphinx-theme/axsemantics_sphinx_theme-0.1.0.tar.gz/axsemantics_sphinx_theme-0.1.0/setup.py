from io import open
from setuptools import setup
from axsemantics_sphinx_theme import __version__


with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="axsemantics_sphinx_theme",
    version=__version__,
    url="https://github.com/axsemantics/sphinx_theme/",
    license="MIT",
    author="AX Semantics",
    author_email="infrastructure@ax-semantics.com",
    description="Sphinx theme used on AX Semantics internal documentation",
    long_description=long_description,
    packages=["axsemantics_sphinx_theme"],
    package_data={
        "axsemantics_sphinx_theme": [
            "theme.conf",
            "*.html",
            "static/css/*.css",
            "static/js/*.js",
            "static/font/*.*",
        ]
    },
    include_package_data=True,
    # See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
    entry_points={
        "sphinx.html_themes": [
            "axsemantics_sphinx_theme = axsemantics_sphinx_theme",
        ]
    },
    python_requires=">=3.9",
    install_requires=["sphinx"],
    classifiers=[
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Theme",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
)
