from setuptools import setup, find_packages

setup(name='pyfrigel-report-tool',
      version='0.2',
      description='Package for the creation of Frigel reports',
      packages=find_packages(),
      # packages=['pyfrigel_report_tool'],
      package_data={'pyfrigel_report_tool': ['assets/*']},
      include_package_data=True,
      license='LICENSE.txt',
   # TODO
    url='http://pypi.python.org/pypi/pyfrigel-report-tool/',
    install_requires=[
       "reportlab",
       'numpy'
   ],
      zip_safe=False)