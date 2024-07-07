from setuptools import setup

setup(name='xlschema',
      version='0.3.15',
      description='Generate relational model code from yaml/xlsx/db_uri',
      url='https://github.com/rezayat/xlschema',
      author='Shakeeb Alireza',
      license='MIT',
      packages=['xlschema'],
      install_requires=[
        'colorlog',
        'mako',
        'openpyxl',
        'SQLAlchemy==1.4.31',
        'PyYAML',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False,
      include_package_data=True)
