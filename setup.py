#from distutils.core import setup
import setuptools

def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setuptools.setup(
    name='Openman',
    version='0.1.1',
    license="MIT",
    zip_safe=False,
    python_requires=">=3.5",
    url = 'https://github.com/codeasashu/openman',
    keywords = ['api', 'openapi','rest', 'specification', 'oas', 'documentation'],
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'apispec==3.1.0',
        'Click==7.0',
        'jsonpath-rw==1.4.0',
        'connexion==2.4.0',
        'swagger-ui-bundle==0.0.6',
        'Faker==2.0.4',
    ],
    tests_require=[
        'pytest==5.2.2',
        'coverage==4.5.4',
        'tox==3.14.1',
        'pytest-cov==2.8.1',
    ],
    test_suite='tests',
    description='A Postman to OpenAPI spec converter with mocking facilities',
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    entry_points= {
        'console_scripts': ['openman=openman.cli:cli']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)