"""
quart_cmark
-----------

Add cmark processing filter to your Quart app.

"""
import setuptools

try:
    from sphinx.setup_command import BuildDoc

    cmdclass = {"build_sphinx": BuildDoc}
except ModuleNotFoundError:
    pass


def read_text(path):
    """
    Read you some text
    """
    with open(path, "r", encoding="utf-8") as _fh:
        return _fh.read()


setuptools.setup(
    name="Quart-Cmark",
    version="0.1.2",
    url="https://gitlab.com/doug.shawhan/quart-cmark",
    project_urls={
        "Bug Tracker": "https://gitlab.com/doug.shawhan/quart-cmark/issues",
        "Source Code": "https://gitlab.com/doug.shawhan/quart-cmark/tree/master",
        "Development Version": "https://gitlab.com/doug.shawhan/quart-cmark/tree/dev",
        "Documentation": "https://quart-cmark.readthedocs.io",
    },
    license=read_text("LICENSE"),
    author="Doug Shawhan",
    author_email="doug.shawhan@gmail.com",
    maintainer="Doug Shawhan",
    maintainer_email="doug.shawhan@gmail.com",
    description="Add commonmark processing filter to your Quart app.",
    long_description=read_text("README.md"),
    long_description_content_type="text/markdown",  # use mimetype for pretty!
    include_package_data=True,
    py_modules=["quart_cmark"],
    platforms="any",
    install_requires=[
        "Quart",
        "paka.cmark>=2.3.0",
        "jinja2>=3",
        "markupsafe>=2",
    ],
    test_suite="tests",
    tests_require=["pytest", "pytest-asyncio",],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
