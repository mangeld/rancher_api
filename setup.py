from setuptools import setup


setup(
    name="rancher",
    version="0.3.9",
    author="Miguel Ángel Durán González",
    author_email="hi@mangel.me",
    description="Python wrapper for rancher api",
    url="https://github.com/mangeld/rancher_api",
    packages=['rancher',],
    install_requires=[
        'requests==2.20.0',
        'websocket-client==0.40.0',
    ],
)
