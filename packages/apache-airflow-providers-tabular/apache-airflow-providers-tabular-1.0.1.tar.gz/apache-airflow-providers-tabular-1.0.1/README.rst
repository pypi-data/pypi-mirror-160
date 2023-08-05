
.. Licensed to the Apache Software Foundation (ASF) under one
   or more contributor license agreements.  See the NOTICE file
   distributed with this work for additional information
   regarding copyright ownership.  The ASF licenses this file
   to you under the Apache License, Version 2.0 (the
   "License"); you may not use this file except in compliance
   with the License.  You may obtain a copy of the License at

..   http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.


Package ``apache-airflow-providers-tabular``

Release: ``1.0.1``


`Tabular <https://tabular.io/>`__


Provider package
----------------

This is a provider package for ``tabular`` provider. All classes for this provider package
are in ``airflow.providers.tabular`` python package.

You can find package information and changelog for the provider
in the `documentation <https://airflow.apache.org/docs/apache-airflow-providers-tabular/1.0.1/>`_.


Installation
------------

You can install this package on top of an existing Airflow 2 installation (see ``Requirements`` below
for the minimum Airflow version supported) via
``pip install apache-airflow-providers-tabular``

The package supports the following python versions: 3.7,3.8,3.9,3.10

Requirements
------------

==================  ==================
PIP package         Version required
==================  ==================
``apache-airflow``  ``>=2.2.0``
==================  ==================

 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

 ..   http://www.apache.org/licenses/LICENSE-2.0

 .. Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

Changelog
---------

1.0.1
.....

Bug Fixes
~~~~~~~~~

* ``Set grant type of the Tabular hook (#25099)``

1.0.0
.....

Initial version of the provider.
