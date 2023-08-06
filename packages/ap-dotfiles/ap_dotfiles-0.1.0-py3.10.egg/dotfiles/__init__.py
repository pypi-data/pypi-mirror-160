"""Shortcut functions."""

import argparse
import os
import re
import shutil
import sys

parent = os.path.dirname(os.path.abspath(__file__))
METADIR = os.path.join(parent, "metafiles")
CWD = os.path.abspath(os.getcwd())


def populate_metafiles():
    """Copy all metafiles to current working directory."""
    files = [
        ".prospector.yml",
        ".markdownlint.json",
        ".editorconfig",
        ".gitignore",
        ".gitattributes",
        ".pylintrc",
        ".setup.cfg",
        ".vscodeignore",
        "altREADME.md",
        "CHANGELOG.md",
        "Makefile",
        "mkdocs.yml",
        "MANIFEST.in",
        "pyproject.toml",
        "README.md",
        "setup.py",
        "tox.ini",
        "workflow.yml",
    ]
    for item in files:
        full = os.path.join(METADIR, item)
        shutil.copy(full, CWD)


def main():
    """Parse command line arguments."""
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(
        sys.argv[0], description="populate meta files"
    )
    subparsers = parser.add_subparsers()
    populate = subparsers.add_parser("populate")
    populate.set_defaults(func=populate_metafiles)
    namespace = parser.parse_args(args)
    namespace.func()
