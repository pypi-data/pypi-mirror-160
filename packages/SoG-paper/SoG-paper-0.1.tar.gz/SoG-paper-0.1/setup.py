#!/usr/bin/python

#
# Project Librarian: Brandon Piotrzkowski
#              Research Associate
#              UW-Milwaukee Department of Physics
#              Center for Gravitation & Cosmology
#              <alexander.urban@ligo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from setuptools import setup, find_packages


setup(
    name='SoG-paper',
    version='0.1',
    url='http://gracedb.ligo.org',
    author='Brandon Piotrzkowski',
    author_email='brandon.piotrzkowski@ligo.org',
    #maintainer="Brandon Piotrzkowski",
    #maintainer_email="brandon.piotrzkowski@ligo.org",
    description='Low-latency manuscript of speed of gravity measurement',
    license='GNU General Public License Version 3',
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics"
    ),
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['tex/files/*']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    namespace_packages=['SoG'],
    scripts=[
        'bin/SoG_generate_pdf',
        'bin/SoG_upload_pdf',
    ],
    install_requires=[
        'numpy>=1.14.5',
        'healpy!=1.12.0',   # FIXME: https://github.com/healpy/healpy/pull/457
        'ligo-gracedb',
        'gracedb-sdk',
        'matplotlib',
        'astropy',
        'scipy>=0.7.2',
        'ligo.skymap>=0.1.1',
        'lxml',
        'gcn',
        'lalsuite',
        'ligo.skymap'
    ],
    python_requires='>=3.8',
)
