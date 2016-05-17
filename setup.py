from setuptools import setup

requires = [
    "click",
    "jinja2",
    "PyYAML",
]

setup(
    name='py-swagger-apigen',
    version='0.0.1',
    description='Generate APIs from Swagger documentation',
    url='https://github.com/ChristianWitts/py-swagger-apigen',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        ],
    author='Christian Witts',
    author_email='cwitts@gmail.com',
    keywords='swagger code-generator',
    packages=['py_swagger_apigen'],
    package_data={
        'templates': ['py_swagger_apigen/templates/*']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'py-swagger-apigen=py_swagger_apigen:generate'
        ]
    },
    zip_safe=False,
    test_suite=None,
    install_requires=requires,
)