# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oarepo_model_builder',
 'oarepo_model_builder.builders',
 'oarepo_model_builder.builtin_models',
 'oarepo_model_builder.invenio',
 'oarepo_model_builder.loaders',
 'oarepo_model_builder.model_preprocessors',
 'oarepo_model_builder.outputs',
 'oarepo_model_builder.property_preprocessors',
 'oarepo_model_builder.stack',
 'oarepo_model_builder.templates',
 'oarepo_model_builder.utils',
 'oarepo_model_builder.utils.cst',
 'oarepo_model_builder.validation',
 'oarepo_model_builder.validation.schemas']

package_data = \
{'': ['*'], 'oarepo_model_builder.invenio': ['templates/*']}

install_requires = \
['Faker>11.3.0',
 'Jinja2>=3.0.3,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'black>21.11b1',
 'click>=7.1',
 'cookiecutter>=1.7.3,<2.0.0',
 'deepdiff>=5.6.0,<6.0.0',
 'invenio-cli>=1.0.4,<2.0.0',
 'isort>=5.10.1,<6.0.0',
 'json5>=0.9.6,<0.10.0',
 'jsonpointer>=2.2,<3.0',
 'jsonschema[format]>=4.4.0,<5.0.0',
 'lazy-object-proxy>=1.7.1,<2.0.0',
 'libcst>=0.3.19',
 'munch>=2.5.0,<3.0.0',
 'tomlkit>=0.7.2']

entry_points = \
{'console_scripts': ['oarepo-compile-model = oarepo_model_builder.cli:run'],
 'oarepo.model_schemas': ['date = '
                          'oarepo_model_builder.validation.schemas:date.json5',
                          'elasticsearch = '
                          'oarepo_model_builder.validation.schemas:elasticsearch.json5',
                          'es-strings = '
                          'oarepo_model_builder.validation.schemas:es_strings.json5',
                          'facets = '
                          'oarepo_model_builder.validation.schemas:facets.json5',
                          'faker = '
                          'oarepo_model_builder.validation.schemas:faker.json5',
                          'mapping = '
                          'oarepo_model_builder.validation.schemas:mapping.json5',
                          'marshmallow = '
                          'oarepo_model_builder.validation.schemas:marshmallow.json5',
                          'modelschema = '
                          'oarepo_model_builder.validation.schemas:modelschema.json5',
                          'plugins = '
                          'oarepo_model_builder.validation.schemas:plugins.json5',
                          'settings = '
                          'oarepo_model_builder.validation.schemas:settings.json5',
                          'sort = '
                          'oarepo_model_builder.validation.schemas:sort.json5'],
 'oarepo.models': ['invenio = '
                   'oarepo_model_builder.builtin_models:invenio.json'],
 'oarepo_model_builder.builders': ['0020-jsonschema = '
                                   'oarepo_model_builder.builders.jsonschema:JSONSchemaBuilder',
                                   '0030-mapping = '
                                   'oarepo_model_builder.builders.mapping:MappingBuilder',
                                   '0050-poetry = '
                                   'oarepo_model_builder.builders.poetry:PoetryBuilder',
                                   '0100-python_structure = '
                                   'oarepo_model_builder.builders.python_structure:PythonStructureBuilder',
                                   '0110-invenio_record = '
                                   'oarepo_model_builder.invenio.invenio_record:InvenioRecordBuilder',
                                   '0120-invenio_record_metadata = '
                                   'oarepo_model_builder.invenio.invenio_record_metadata:InvenioRecordMetadataBuilder',
                                   '0130-invenio_record_schema = '
                                   'oarepo_model_builder.invenio.invenio_record_schema:InvenioRecordSchemaBuilder',
                                   '0200-invenio_record_permissions = '
                                   'oarepo_model_builder.invenio.invenio_record_permissions:InvenioRecordPermissionsBuilder',
                                   '0300-invenio_record_search_options = '
                                   'oarepo_model_builder.invenio.invenio_record_search:InvenioRecordSearchOptionsBuilder',
                                   '0310-invenio_record_service_config = '
                                   'oarepo_model_builder.invenio.invenio_record_service_config:InvenioRecordServiceConfigBuilder',
                                   '0320-invenio_record_service = '
                                   'oarepo_model_builder.invenio.invenio_record_service:InvenioRecordServiceBuilder',
                                   '0340-invenio_record_dumper = '
                                   'oarepo_model_builder.invenio.invenio_record_dumper:InvenioRecordDumperBuilder',
                                   '0400-invenio_record_resource_config = '
                                   'oarepo_model_builder.invenio.invenio_record_resource_config:InvenioRecordResourceConfigBuilder',
                                   '0410-invenio_record_resource = '
                                   'oarepo_model_builder.invenio.invenio_record_resource:InvenioRecordResourceBuilder',
                                   '0420-invenio_views = '
                                   'oarepo_model_builder.invenio.invenio_views:InvenioViewsBuilder',
                                   '0500-invenio_config = '
                                   'oarepo_model_builder.invenio.invenio_config:InvenioConfigBuilder',
                                   '0600-invenio_ext = '
                                   'oarepo_model_builder.invenio.invenio_ext:InvenioExtBuilder',
                                   '0610-invenio_ext_poetry = '
                                   'oarepo_model_builder.invenio.invenio_ext_poetry:InvenioExtPoetryBuilder',
                                   '0700-invenio_ext = '
                                   'oarepo_model_builder.invenio.invenio_proxies:InvenioProxiesBuilder',
                                   '0900-invenio_sample_app_poetry = '
                                   'oarepo_model_builder.invenio.invenio_sample_app_poetry:InvenioSampleAppPoetryBuilder',
                                   '0910-invenio_record_metadata_alembic_poetry '
                                   '= '
                                   'oarepo_model_builder.invenio.invenio_record_metadata_alembic_poetry:InvenioRecordMetadataAlembicPoetryBuilder',
                                   '0920-invenio_record_metadata_models_poetry '
                                   '= '
                                   'oarepo_model_builder.invenio.invenio_record_metadata_models_poetry:InvenioRecordMetadataModelsPoetryBuilder',
                                   '0930-invenio_resource_poetry = '
                                   'oarepo_model_builder.invenio.invenio_record_resource_poetry:InvenioRecordResourcePoetryBuilder',
                                   '0940-invenio_record_search_poetry = '
                                   'oarepo_model_builder.invenio.invenio_record_search_poetry:InvenioRecordSearchPoetryBuilder',
                                   '0950-invenio_record_jsonschemas_poetry = '
                                   'oarepo_model_builder.invenio.invenio_record_jsonschemas_poetry:InvenioRecordJSONSchemasPoetryBuilder',
                                   '1000-invenio_script_bootstrap = '
                                   'oarepo_model_builder.invenio.invenio_script_bootstrap:InvenioScriptBootstrapBuilder',
                                   '1010-invenio_script_runserver = '
                                   'oarepo_model_builder.invenio.invenio_script_runserver:InvenioScriptRunServerBuilder',
                                   '1020-invenio_script_import_sample_data = '
                                   'oarepo_model_builder.invenio.invenio_script_import_sample_data:InvenioScriptImportSampleDataBuilder',
                                   '1030-invenio_script_sample_data = '
                                   'oarepo_model_builder.invenio.invenio_script_sample_data:InvenioScriptSampleDataBuilder',
                                   '1040-invenio_script_sample_data_shell = '
                                   'oarepo_model_builder.invenio.invenio_script_sample_data:InvenioScriptSampleDataShellBuilder',
                                   '1100-cookiecutter_config = '
                                   'oarepo_model_builder.builders.cookiecutter:CookiecutterBuilder'],
 'oarepo_model_builder.loaders': ['json = '
                                  'oarepo_model_builder.loaders:json_loader',
                                  'json5 = '
                                  'oarepo_model_builder.loaders:json_loader',
                                  'yaml = '
                                  'oarepo_model_builder.loaders:yaml_loader',
                                  'yml = '
                                  'oarepo_model_builder.loaders:yaml_loader'],
 'oarepo_model_builder.model_preprocessors': ['01-default = '
                                              'oarepo_model_builder.model_preprocessors.default_values:DefaultValuesModelPreprocessor',
                                              '10-invenio = '
                                              'oarepo_model_builder.model_preprocessors.invenio:InvenioModelPreprocessor',
                                              '20-elasticsearch = '
                                              'oarepo_model_builder.model_preprocessors.elasticsearch:ElasticsearchModelPreprocessor'],
 'oarepo_model_builder.outputs': ['diff = '
                                  'oarepo_model_builder.outputs.diff:DiffOutput',
                                  'json = '
                                  'oarepo_model_builder.outputs.json:JSONOutput',
                                  'jsonschema = '
                                  'oarepo_model_builder.outputs.jsonschema:JSONSchemaOutput',
                                  'mapping = '
                                  'oarepo_model_builder.outputs.mapping:MappingOutput',
                                  'python = '
                                  'oarepo_model_builder.outputs.python:PythonOutput',
                                  'text = '
                                  'oarepo_model_builder.outputs.text:TextOutput',
                                  'toml = '
                                  'oarepo_model_builder.outputs.toml:TOMLOutput',
                                  'yaml = '
                                  'oarepo_model_builder.outputs.yaml:YAMLOutput'],
 'oarepo_model_builder.property_preprocessors': ['100-type_shortcuts = '
                                                 'oarepo_model_builder.property_preprocessors.type_shortcuts:TypeShortcutsPreprocessor',
                                                 '200-enum = '
                                                 'oarepo_model_builder.property_preprocessors.enum:EnumPreprocessor',
                                                 '500-text_keyword = '
                                                 'oarepo_model_builder.property_preprocessors.text_keyword:TextKeywordPreprocessor',
                                                 '600-date = '
                                                 'oarepo_model_builder.property_preprocessors.date:DatePreprocessor',
                                                 '700-marshmallow-class = '
                                                 'oarepo_model_builder.property_preprocessors.marshmallow_class_generator:MarshmallowClassGeneratorPreprocessor',
                                                 '700-number = '
                                                 'oarepo_model_builder.property_preprocessors.number:NumberPreprocessor',
                                                 '800-raw = '
                                                 'oarepo_model_builder.property_preprocessors.raw:RawPreprocessor',
                                                 '900-validators = '
                                                 'oarepo_model_builder.property_preprocessors.marshmallow_validators_generator:ValidatorsPreprocessor'],
 'oarepo_model_builder.templates': ['99-base_templates = '
                                    'oarepo_model_builder.invenio']}

setup_kwargs = {
    'name': 'oarepo-model-builder',
    'version': '1.0.0.dev9',
    'description': 'An utility library that generates OARepo required data model files from a JSON specification file',
    'long_description': '# OARepo model builder\n\n## Work in progress\n\nA library and command-line tool to generate invenio model project from a single model file.\n\n<!--TOC-->\n\n- [OARepo model builder](#oarepo-model-builder)\n  - [Work in progress](#work-in-progress)\n  - [CLI Usage](#cli-usage)\n    - [Installing model builder as dev dependency](#installing-model-builder-as-dev-dependency)\n    - [Installing model builder in a separate virtualenv](#installing-model-builder-in-a-separate-virtualenv)\n    - [Running model builder](#running-model-builder)\n  - [Model file](#model-file)\n    - [Model file structure](#model-file-structure)\n    - ["model" section](#model-section)\n    - ["settings" section](#settings-section)\n    - ["plugins" section](#plugins-section)\n  - [Builder as a library (using via API)](#builder-as-a-library-using-via-api)\n  - [Writing custom plugins](#writing-custom-plugins)\n\n<!--TOC-->\n\n## CLI Usage\n\nTo use the model builder client, you first have to install the model builder somewhere.\n\n### Installing model builder as dev dependency\n\nInitialize your new project with ``poetry create`` and then add model builder\nwith ``poetry add --dev oarepo-model-builder``. This is the simplest solution but has a disadvantage - as poetry always\ninstalls dev dependencies in build & test, but not in production, in your development environment you will have extra\npackages installed. If you happen to use them, you will break your production build.\n\n### Installing model builder in a separate virtualenv\n\nCreate a separate virtualenv and install model builder into it:\n\n```bash\npython3.10 -m venv .venv-builder\n(source .venv-builder/bin/activate; pip install -U pip setuptools wheel; pip install oarepo-model-builder)\n```\n\nThen for ease of use add the following aliases\n\n```bash\nalias oarepo-compile-model="$PWD/.venv-builder/bin/oarepo-compile-model"\nalias oarepo-model-builder-pip="$PWD/.venv-builder/bin/pip"\n```\n\nUse the ``oarepo-model-builder-pip`` if you need to install plugins to the model builder.\n\n### Running model builder\n\n```bash\noarepo-compile-model model.yaml\n```\n\nwill compile the model.yaml into the current directory. Options:\n\n```bash\n  --output-directory <dir> Output directory where the generated files will be\n                           placed. Defaults to "."\n  --package <name>         Package into which the model is generated. If not\n                           passed, the name of the current directory,\n                           converted into python package name, is used.\n  --set <name=value>       Overwrite option in the model file. \n                           Example --set settings.elasticsearch.keyword-ignore-above=20\n  -v                       Increase the verbosity. This option can be used\n                           multiple times.\n  --config <filename>      Load a config file and replace parts of the model\n                           with it. The config file can be a json, yaml or a\n                           python file. If it is a python file, it is\n                           evaluated with the current model stored in the\n                           "oarepo_model" global variable and after the\n                           evaluation all globals are set on the model.\n  --isort / --skip-isort   Call isort on generated sources (default: yes)\n  --black / --skip-black   Call black on generated sources (default: yes)\n```\n\n## Model file\n\nA model is a json/yaml file including description of the model and processing settings. Example:\n\n```yaml\nversion: 1.0.0\noarepo:use: invenio\nmodel:\n  properties:\n    metadata:\n      properties:\n        title:\n          type: fulltext+keyword\n          oarepo:ui:\n            label: Title\n          oarepo:mapping:\n          # anything in here will be put into the mapping file\n          # fulltext+keyword type automatically creates "type: text" \n          # with subfield \'keyword\' of type keyword\nsettings:\n  package: uct.titled_model \n```\n\n### Model file structure\n\nA model is a json/yaml file with the following structure:\n\n```yaml\nversion: 1.0.0\nmodel:\n  properties:\n    title:\n      type: fulltext+keyword\nsettings:\n  <generic settings here>\n  python: ...\n  elasticsearch: ...\nplugins: ...\n```\n\nThere might be more sections (documentation etc.), but only the ``settings``, ``model`` and ``plugins``\nare currently processed.\n\n### "model" section\n\nThis section is described in [model.md](docs/model.md)\n\n### "settings" section\n\nThe settings section contains various configuration settings. In most cases you want to set only the `package` option as\nin above because all other settings are derived from it. Even the `package`\noption might be omitted - in this case the package name will be the last component of the output directory (with dashes\nconverted to underscores).\n\nThe rest of the settings are described in [model-generic-settings.md](docs/model-generic-settings.md)\n\nAdvanced use cases might require to modify [the python settings](docs/model-python-settings.md) or\n[elasticsearch settings](docs/model-elasticsearch-settings.md) (for example, to define custom analyzers).\n\n### "plugins" section\n\nSee [plugins and the processing order](docs/model-plugins.md) for details.\n\n## Builder as a library (using via API)\n\nTo invoke the builder programmatically, see [using the API](docs/using-api.md).\n\n## Writing custom plugins\n\nSee [writing plugins](docs/extending-api.md) if you want to extend the building process with your own plugins.\n',
    'author': 'Miroslav Bauer',
    'author_email': 'bauer@cesnet.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
