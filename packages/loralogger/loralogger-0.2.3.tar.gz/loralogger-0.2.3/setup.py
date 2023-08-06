# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loralogger',
 'loralogger.filters',
 'loralogger.handlers',
 'loralogger.loggers']

package_data = \
{'': ['*']}

install_requires = \
['WorkerConnector>=0.0.7,<0.0.8',
 'python-dotenv>=0.20.0,<0.21.0',
 'redis>=4.3.4,<5.0.0']

setup_kwargs = {
    'name': 'loralogger',
    'version': '0.2.3',
    'description': 'Custom logging handler for AskLora projects',
    'long_description': '# LORA Logger\n\nThis package contains both the customised handler for saving the logs into a elasticsearch database, and a factory for creating customised loggers that can use that handler.\n\nThe customised handler will forward the logs to an existing logging service through our own celery service. This logging service will handle the logs and input them into the database. This is done to unionise the logs into a single database.\n\n## Diagram\n\n```mermaid\nflowchart LR\n\n    services["Services\\n<small>All backend projects\\nthat need the logging\\nsystem</small>"]-->producer[[Producer]]\n    subgraph "LoraLogger package"\n    producer-->queue[Queue]\n    end\n    queue-->consumer[[Consumer]]\n    subgraph "AskLora logger service"\n    consumer-->database[(<small>ElasticSearch\\nDatabase</small>)]\n    end\n\n```\n\n## How to use\n\nCurrently, this package exports a logging handler. Loggers with this handler will be automatically send the records to the elasticsearch server set using the environment variable.\n\n### Package installation\n\nthere are two ways to install this pacakge\n\n- install the package locally. first, build the project:\n  ```bash\n  poetry build\n  ```\n  then you can install using pip\n  ```bash\n  pip install /path/to/logger/dist/loralogger-0.2.2-py3-none-any.whl\n  ```\n- Install the package from pip\n  ```bash\n  pip install loralogger\n  ```\n\n### Using this package\n\nFirst, set these environment variables:\n\n```\n# Set amqp backend\nAMQP_BROKER=localhost\nAMQP_PORT=5672\nAMQP_USER=rabbitmq\nAMQP_PASSWORD=rabbitmq\n\n# set results backend\nREDIS_HOST=localhost\nREDIS_PORT=6379\n```\n\nThen you can use the logger in two different ways:\n\n1. Use the logger factory\n\n   - import the logger factory\n\n     ```python\n     from loralogger import LoraLogger\n     ```\n\n   - create a logger instance, the logger name should point to the Elasticsearch index name you want to send the logs into, with the word "-logs" appended to it (this, for instance, will send the logs to `backend-logs` index)\n\n     ```python\n     test_logger = LoraLogger.get_logger(\'backend\',  log_to_es=True)  # We need to set this on or it wont send to Elasticsearch\n     ```\n\n   - use the logger\n     ```python\n     test_logger.warning("Careful!")\n     ```\n\n2. Use the handler directly to your own logger instance:\n\n   - import the handler\n\n     ```python\n     from loralogger import LogToESHandler\n     ```\n\n   - initialise logging instance\n\n     ```python\n     backend_logger = logging.getLogger("backend")\n     ```\n\n   - Create the handler instance, same as the above, the label should point to an existing Elasticsearch index\n\n     ```python\n     handler = LogToESHandler(label="backend")\n     ```\n\n   - add the handler instance to the logger\n\n     ```python\n     backend_logger.addHandler(handler)\n     ```\n\n   - Use the logger\n\n     ```python\n     backend_logger.info("This is an info")\n     ```\n\n# Notes\n\n- if the pip installation fails, check this link https://github.com/celery/librabbitmq/issues/131#issuecomment-661884151\n',
    'author': 'LORA Technologies',
    'author_email': 'asklora@loratechai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
