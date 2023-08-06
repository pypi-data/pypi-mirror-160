# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup script for oauth2client.

Also installs included versions of third party libraries, if those libraries
are not already installed.
"""

from setuptools import find_packages, setup

import oauth2client

long_description = """
oauth2client is a client library for OAuth 2.0.

Note: oauth2client is now deprecated. No more features will be added to the
    libraries and the core team is turning down support. We recommend you use
    `google-auth <https://google-auth.readthedocs.io>`__ and
    `oauthlib <http://oauthlib.readthedocs.io/>`__.
"""

version = oauth2client.__version__

setup(
    name="internationaltouch-oauth2client",
    version=version,
    description="OAuth 2.0 client library",
    long_description=long_description,
    author="Google Inc.",
    author_email="jonwayne+oauth2client@google.com",
    url="http://github.com/google/oauth2client/",
    python_requires=">=3.6",
    install_requires=[
        "httplib2>=0.9.1",
        "pyasn1>=0.1.7",
        "pyasn1-modules>=0.0.5",
        "rsa>=3.1.4",
        "six>=1.6.1",
    ],
    packages=find_packages(exclude=("tests*",)),
    license="Apache 2.0",
    keywords="google oauth 2.0 http client",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
