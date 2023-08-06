# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ebike_dl']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ebike-dl = ebike_dl.main:app',
                     'rick-portal-gun = rick_portal_gun.main:app']}

setup_kwargs = {
    'name': 'ebike-dl',
    'version': '0.3.3',
    'description': 'Bosch eBike Connect Activity Downloader',
    'long_description': "[![PyPI version](https://badge.fury.io/py/ebike-dl.svg)](https://badge.fury.io/py/ebike-dl)\n\n# ebike-downloader\n\nBosch eBike Connect Activity Downloader (https://www.ebike-connect.com/dashboard)\nFetch activities by dates and download a copy of the rides.\n\n## Install\n\nebike-downloader uses [poetry](https://python-poetry.org/).\n\nYou can easily run it using\n\n```bash\npipx install ebike-dl\n```\n\n## Run\n\n```\nebike-dl fetch --since 2022-06-15 --out-dir out --login=foo --password=bar\n```\n\nwhere login passwords are from the ebike-connect.com portal.\n\nYou'll then get the downloaded files (1per ride) in the folder ./out\n(you can also use env variable to provide login, password, ... see --help)\n\n## To GPX\n\nYou have the ability to download GPX on Bosch's portal, but those do not contain any additional info like power, cadence or heart_rate.\nby using `to-gpx` you can get a gpx with all those things (in gpx extension it might not be supported by the average gpx reader...)\n\n```\nebike-dl to-gpx --file out/myid.json\n# output out/myid.pgx\n```\n\nUsed extensions:\n\n    gpxtpx http://www.garmin.com/xmlschemas/TrackPointExtension/v2\n    pwr http://www.garmin.com/xmlschemas/PowerExtension/v1\n\n## To KML 2.2\n\nthere is also the ability to transform those to KML (ofc some info will be lost)\n\n```\nebike-dl to-kml --file out/myid.json\n# output out/myid.kml\n```\n\n## Acknowledgements\n\n- [Cycliste Urbain](https://gitlab.com/cycliste-urbain/resources)\n\n## Authors\n\n- [@eMerzh](https://www.github.com/eMerzh)\n",
    'author': 'Brice Maron',
    'author_email': 'bmaron@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eMerzh/ebike-dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
