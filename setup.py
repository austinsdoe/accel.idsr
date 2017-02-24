from setuptools import setup

setup(
    name='accelidsr',
    packages=['accelidsr'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-login',
        'flask-wtf',
        'flask-pymongo',
    ],
)
