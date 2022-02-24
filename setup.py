from setuptools import find_packages, setup

install_requires = [
    "django>=3",
    "djangorestframework>=3",
    "pycrypto>=2",
]

test_require = [
    "black",
    "coverage",
    "flake8",
    "isort",
    "pytest",
    "pytest-cov",
    "pytest-django",
]

docs_require = []

setup(
    name="django-secret-sharing",
    version="0.1.0",
    description="",
    author="R. Moorman <rob@vicktor.nl>",
    install_requires=install_requires,
    extras_require={"test": test_require},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
    ],
)
