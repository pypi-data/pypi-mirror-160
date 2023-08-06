# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnus_extension_datastore_db']

package_data = \
{'': ['*']}

install_requires = \
['magnus', 'psycopg2-binary>=2.9.3,<3.0.0', 'sqlalchemy']

entry_points = \
{'magnus.datastore.BaseRunLogStore': ['db = '
                                      'magnus_extension_datastore_db.db:DBStore'],
 'magnus.integration.BaseIntegration': ['local-container-run_log_store-db = '
                                        'magnus_extension_datastore_db.integration:LocalContainerComputeDBStore']}

setup_kwargs = {
    'name': 'magnus-extension-datastore-db',
    'version': '0.1.1',
    'description': 'Magnus extension for DB as run log store',
    'long_description': '# DB Run log store provider\n\nThis package is an extension to [magnus](https://github.com/AstraZeneca/magnus-core).\n\n## Provides \nProvides capability to have a database as a run log store.\n\nThis run log store is concurrent safe.\n\n## Installation instructions\n\n```pip install magnus_extension_datastore_db```\n\n## Set up required to use the extension\n\nA database schema and a role with read/write privileges.\n\nThe DB model used by this extension is:\n\n```python\nclass DBLog(Base):\n    """\n    Base table for storing run logs in database.\n\n    In this model, we fragment the run log into logical units that are concurrent safe.\n    """\n    __tablename__ = \'db_log\'\n    pk = Column(Integer, Sequence(\'id_seq\'), primary_key=True)\n    run_id = Column(Text)\n    attribute_key = Column(Text)  # run_log, step_internal_name, parameter_key etc\n    attribute_type = Column(Text)  # RunLog, Step, Branch, Parameter\n    attribute_value = Column(Text)  # The JSON string\n    created_at = Column(DateTime, default=datetime.datetime.utcnow)\n```\n\nPlease note that ```created_at``` is important for ordering of the steps and events and should be always increasing for\nnew instances (records).\n\nYou can either create this schema using your own mechanisms or can use the handy script provided as part of this\npackage.\n\n```python\nfrom magnus_extension_datastore_db import db\ndb.create_tables(<connection_string>)\n```\n\n## Config parameters\n\nThe full configuration of this run log store is:\n\n```yaml\nrun_log:\n  type: db\n  config:\n    connection_string: The connection string to use in SQLAlchemy. Secret placeholders are fine.\n```\n\n### **connection_string**:\n\nPlease provide the connection string of the database using this variable.\n\nYou can use placeholders for sensitive details and provide it by the secrets manager. Internally, we use \n[python template strings](https://docs.python.org/3/library/string.html#template-strings) \nto create a template and \n[safe substitute](https://docs.python.org/3/library/string.html#string.Template.safe_substitute) with secrets \nkey value pairs.\n\nFor example, a connection string ```\'postgresql://scott:${password}@localhost:5432/mydatabase\'``` and secrets having\na key value pair of ```password=tiger``` would result in a connection string of\n```\'postgresql://scott:tiger@localhost:5432/mydatabase\'```',
    'author': 'Vijay Vammi',
    'author_email': 'vijay.vammi@astrazeneca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AstraZeneca/magnus-extensions/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
