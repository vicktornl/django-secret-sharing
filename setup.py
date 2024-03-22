from setuptools import find_packages, setup

install_requires = [
    "cryptography>=38",
    "django>=3.2",
    "djangorestframework>=3",
]

aws_requires = [
    "boto3>=1.16",
]

test_requires = [
    "black",
    "coverage",
    "flake8",
    "isort",
    "pytest",
    "pytest-cov",
    "pytest-django",
]

setup(
    name="django-secret-sharing",
    version="0.7.0",
    description="",
    author="R. Moorman <rob@vicktor.nl>",
    install_requires=install_requires,
    tests_requires=test_requires,
    extras_require={"aws": aws_requires, "test": test_requires},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: Unix",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
