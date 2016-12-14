from setuptools import setup


setup(
    name="rancher",
    version="0.1.3",
    author="Miguel Ángel Durán González",
    author_email="hi@mangel.me",
    url="https://github.com/mangeld/rancher_api",
    packages=['rancher',],
    install_requires=[
        'requests==2.12.1',
    ],
)
