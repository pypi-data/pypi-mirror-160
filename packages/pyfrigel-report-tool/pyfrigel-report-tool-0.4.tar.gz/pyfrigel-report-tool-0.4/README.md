Python package to create report for Frigel machines

# Table of Contents
1. [Package creation](README.md#package-creation)
2. [Usage](README.md#usage)
3. [Machines supported](README.md#machines-supported)
4. [Licensing](LICENSE.txt)

# Package creation
How to create python package and upload it to [pypi](https://pypi.org/)
<pre><code>
pip install --upgrade twine
python setup.py sdist
python setup.py bdist_wheel
python setup.py build
python setup.py install
twine upload --repository pypi dist/*
</code></pre>


# Usage
Instantiate report class
<pre><code>
creator = SyncroReportWeeklyCreator(operation_hours=[10, 2, 4, 6, 20, 1, 0],
                                    operation_hours_prev=[8, 10, 5, 7, 10, 1, 0],
                                    working_modes_hours={'standard': [1, 0, 2, 3, 1, 0, 0],
                                                         'production': [8, 2, 2, 3, 10, 1, 0],
                                                         'maintenance': [1, 0, 0, 0, 9, 0, 0]},
                                    working_modes_hours_prev={'standard': [5, 0, 2, 3, 1, 0, 0],
                                                         'production': [2, 1, 2, 3, 10, 1, 0],
                                                         'maintenance': [6, 22, 0, 0, 9, 0, 0]},
                                    start_date=datetime. strptime('18/07/22', '%d/%m/%y'))
</code></pre>

Save PDF to a file
<pre><code>
creator.savePDF("/path/to/file", 'en')
</code></pre>

Get PDF as a BytesIO object
<pre><code>
buffer = creator.getPDFAsBuffer('en')
</code></pre>

# Machines supported
At this moment only Syncro RS machines are supported
