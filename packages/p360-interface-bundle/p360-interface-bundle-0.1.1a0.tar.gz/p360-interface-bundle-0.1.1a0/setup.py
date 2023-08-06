# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['p360_interface_bundle',
 'p360_interface_bundle.featurestore.post_actions.metadata_adjustment']

package_data = \
{'': ['*'], 'p360_interface_bundle': ['_config/*']}

install_requires = \
['daipe-core>=1.4.2,<2.0.0',
 'databricks-bundle>=1.4.5,<2.0.0',
 'feature-store-bundle==2.5.0',
 'pyfony-bundles>=0.4.4,<0.5.0']

entry_points = \
{'pyfony.bundle': ['create = '
                   'p360_interface_bundle.P360InterfaceBundle:P360InterfaceBundle']}

setup_kwargs = {
    'name': 'p360-interface-bundle',
    'version': '0.1.1a0',
    'description': 'Persona360 interface bundle',
    'long_description': '# p360-interface-bundle\n\nInterface between Persona360 app instance and a project with Daipe Feature store.\n\n### Latest Changes\n\n* :building_construction: Default configuration removed. PR [#21](https://github.com/DataSentics/p360-interface-bundle/pull/21) by [@matejoravec](https://github.com/matejoravec).\n* :white_check_mark: `MetadataJsonGetter` test added. PR [#20](https://github.com/DataSentics/p360-interface-bundle/pull/20) by [@matejoravec](https://github.com/matejoravec).\n* :memo: Post-version-bump README update. PR [#19](https://github.com/DataSentics/p360-interface-bundle/pull/19) by [@matejoravec](https://github.com/matejoravec).\n\n### 0.1.0\n\n* :bookmark: Bump version to 0.1.0. PR [#18](https://github.com/DataSentics/p360-interface-bundle/pull/18) by [@matejoravec](https://github.com/matejoravec).\n* :bookmark: Bump version to 0.0.2-alpha.3. PR [#17](https://github.com/DataSentics/p360-interface-bundle/pull/17) by [@matejoravec](https://github.com/matejoravec).\n* :bug: Metadata adjustment fix. PR [#16](https://github.com/DataSentics/p360-interface-bundle/pull/16) by [@matejoravec](https://github.com/matejoravec).\n* :memo: Post-version-bump README update. PR [#15](https://github.com/DataSentics/p360-interface-bundle/pull/15) by [@matejoravec](https://github.com/matejoravec).\n* :bookmark: Bump version to 0.0.2-alpha.2. PR [#13](https://github.com/DataSentics/p360-interface-bundle/pull/13) by [@matejoravec](https://github.com/matejoravec).\n* :arrow_up: `feature-store-bundle` upgraded to 2.5.0. PR [#12](https://github.com/DataSentics/p360-interface-bundle/pull/12) by [@matejoravec](https://github.com/matejoravec).\n* :memo: Post-version-bump README update. PR [#10](https://github.com/DataSentics/p360-interface-bundle/pull/10) by [@matejoravec](https://github.com/matejoravec).\n* :bookmark: Bump version to 0.0.2-alpha.1. PR [#9](https://github.com/DataSentics/p360-interface-bundle/pull/9) by [@matejoravec](https://github.com/matejoravec).\n* :memo: Pre-version-bump README update. PR [#8](https://github.com/DataSentics/p360-interface-bundle/pull/8) by [@matejoravec](https://github.com/matejoravec).\n* :page_facing_up: License fix. PR [#7](https://github.com/DataSentics/p360-interface-bundle/pull/7) by [@matejoravec](https://github.com/matejoravec).\n* :bookmark: Bump version to 0.0.2-alpha.0. PR [#6](https://github.com/DataSentics/p360-interface-bundle/pull/6) by [@matejoravec](https://github.com/matejoravec).\n* :construction_worker: Release pipeline. PR [#5](https://github.com/DataSentics/p360-interface-bundle/pull/5) by [@matejoravec](https://github.com/matejoravec).\n* :sparkles: Metadata adjustment post-action. PR [#4](https://github.com/DataSentics/p360-interface-bundle/pull/4) by [@matejoravec](https://github.com/matejoravec).\n* :bricks: Basic bundle infrastructure. PR [#3](https://github.com/DataSentics/p360-interface-bundle/pull/3) by [@matejoravec](https://github.com/matejoravec).\n* :construction_worker: Wrong main branch name fixed. PR [#2](https://github.com/DataSentics/p360-interface-bundle/pull/2) by [@matejoravec](https://github.com/matejoravec).\n',
    'author': 'Datasentics',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.10,<4.0.0',
}


setup(**setup_kwargs)
