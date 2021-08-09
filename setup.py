from setuptools import setup

exec(open("useful/logs/version.py").read())

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="velebit-useful-logs",
    version=__version__,  # noqa
    description="Module for standardized logs across services",
    classifiers=[
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    url="https://github.com/velebit-ai/useful-logs",
    author="Velebit AI",
    author_email="contact@velebit.ai",
    packages=["useful.logs"],
    install_requires=requirements,
    include_package_data=True
)
