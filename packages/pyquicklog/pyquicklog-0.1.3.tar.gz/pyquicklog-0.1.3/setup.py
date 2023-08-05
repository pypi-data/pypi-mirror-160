from setuptools import find_packages, setup

def readme_file(path: str = "README.md"):
    with open(path, "r") as file:
        content = file.read()
    return content

setup(
    name="pyquicklog",
    version="0.1.3",
    description="A simple logger for python",
    long_description=readme_file(),
    long_description_content_type="text/markdown",
    url="https://github.com/bbenouarets/quicklog.py",
    author="Björn Benouarets",
    author_email="kontakt@bbenouarets.site",
    keywords="quicklog quick log logger logme logging",
    classifiers=[
        "Natural Language :: English"
    ],
    include_package_data=True,
    install_requires=[],
    extra_require={"test": ""},
    packages=find_packages("pyquicklog", exclude=["docs", ".github"]),
    # package_dir={"":"pyquicklog"},
    py_modules=["pyquicklog"],
    license="MIT license",
    zip_safe=False
)
