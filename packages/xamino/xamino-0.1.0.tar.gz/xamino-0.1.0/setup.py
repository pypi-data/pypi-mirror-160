from setuptools import setup, find_packages

requirements = [
    "httpx", 
    "ujson",
    "typing",
    "colored", 
    "setuptools"
]

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name="xamino",
    license='MIT',
    author="forevercynical",
    version="0.1.0",
    author_email="me@cynical.gg",
    description="A library to communicate with aminoapps api",
    url="https://github.com/forevercynical/xamino",
    packages=find_packages(),
    long_description=long_description,
    install_requires=requirements,
    keywords=[
        'aminoapps', 'amino', 'amino-bots', 'amino-bot', 'amino-bot-api', 'amino-bot-api-python', 'amino-bot-api-python3', 'amino-bot-api-python3-library'
    ],
    python_requires='>=3.6',
)
