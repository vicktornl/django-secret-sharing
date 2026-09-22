from setuptools import find_packages, setup

install_requires = [
    "cryptography>=50",
    "django>=5.2",
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
    version="0.8.0",
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
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "Framework :: Django :: 6.1",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
    ],
)
