import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_geofield',
    version=__import__('django_geofield').__version__,
    packages=['django_geofield'],
    include_package_data=True,
    license='MIT License',
    description='A lightweight Django Geo Field to save and handle Geo Points. '
                'It supports to search the nearby points by their geohash',
    long_description=README,
    url='https://github.com/joway/django-geofield',
    author='Joway Wong',
    author_email='joway.w@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ], requires=['django', 'haversine', 'numpy']
)
