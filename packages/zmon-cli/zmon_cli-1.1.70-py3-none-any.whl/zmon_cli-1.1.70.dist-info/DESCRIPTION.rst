ZMON CLI
========

.. _zmon-cli: https://github.com/zalando-zmon/zmon-cli
.. _PyPI: https://pypi.org/project/zmon-cli/

Command line client for the Zalando Monitoring solution (ZMON).

Installation
============

Requires Python 3.4+

.. code-block:: bash

    $ sudo pip3 install --upgrade zmon-cli

Example
=======

Creating or updating a single check definition from its YAML file:

.. code-block:: bash

    $ zmon check-definitions update examples/check-definitions/zmon-stale-active-alerts.yaml

Release
=======

1. Update zmon_cli/__init__.py in a PR with new version and merge
2. Approve Release step manually in the CDP pipeline


