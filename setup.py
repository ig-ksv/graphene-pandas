import ast
import re

from setuptools import find_packages, setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("graphene_pandas/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "graphene == 2.1.8",
    "numpy == 1.19.5",
    "pandas == 1.2.0",
]
try:
    import enum
except ImportError:  # Python < 2.7 and Python 3.3
    requirements.append("enum34 >= 1.1.6")

tests_require = [
    "pytest==6.2.1",
    "mock==2.0.0",
    "pytest-cov==2.6.1",
    "pytest-benchmark==3.2.1",
]

setup(
    name="graphene-pandas",
    version=version,
    description="Graphene Pandas integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ig-ksv/graphene-pandas",
    author="Igor Kozintsev",
    author_email="ig.kozintsev@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="api graphql protocol graphene, pandas",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    extras_require={
        "dev": [
            "tox==3.7.0",  # Should be kept in sync with tox.ini
            "coveralls==1.10.0",
        ],
        "test": tests_require,
    },
    tests_require=tests_require,
)