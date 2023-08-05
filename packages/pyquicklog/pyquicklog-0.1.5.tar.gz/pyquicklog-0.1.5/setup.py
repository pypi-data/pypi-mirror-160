from setuptools import find_packages, setup

def readme_file(path: str = "README.md"):
    with open(path, "r") as file:
        content = file.read()
    return content

requirements = []

setup(
    name="pyquicklog",
    version="0.1.5",
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
    install_requires=requirements,
    extra_require={"test": ""},
    packages=find_packages("pyquicklog", exclude=["docs", ".github"]),
    # package_dir={"":"pyquicklog"},
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <3.11",
    py_modules=["pyquicklog"],
    license="MIT license",
    zip_safe=False
)
