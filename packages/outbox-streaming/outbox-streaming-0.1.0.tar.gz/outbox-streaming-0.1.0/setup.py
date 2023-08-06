# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['outbox_streaming',
 'outbox_streaming.asyncio',
 'outbox_streaming.asyncio.celery',
 'outbox_streaming.asyncio.celery.sqlalchemy',
 'outbox_streaming.asyncio.common',
 'outbox_streaming.asyncio.common.sqlalchemy',
 'outbox_streaming.asyncio.kafka',
 'outbox_streaming.asyncio.kafka.sqlalchemy',
 'outbox_streaming.celery',
 'outbox_streaming.celery.sqlalchemy',
 'outbox_streaming.common',
 'outbox_streaming.common.sqlachemy',
 'outbox_streaming.kafka',
 'outbox_streaming.kafka.sqlalchemy']

package_data = \
{'': ['*']}

extras_require = \
{'test': ['aiokafka>=0.7.2,<0.8.0',
          'SQLAlchemy[asyncio]>=1.4,<2.0',
          'kafka-python>=2.0.2,<3.0.0',
          'celery>=5.2.7,<6.0.0',
          'psycopg2-binary>=2.9.3,<3.0.0']}

setup_kwargs = {
    'name': 'outbox-streaming',
    'version': '0.1.0',
    'description': '',
    'long_description': '# outbox-streaming\n\nReliably send messages to message/task brokers, like Kafka or Celery\n\n## Roadmap\n### Done\n - ✅ Kafka + SQLAlchemy\n - ✅ Kafka + SQLAlchemy + asyncio\n### In progress\n - ⏹ Celery + SQLAlchemy\n - ⏹ Celery + SQLAlchemy + asyncio\n### Planned\n - 🆕 Kafka + Django ORM\n - 🆕 Celery + Django ORM\n - 🆕 Dramatiq + SQLAlchemy\n - 🆕 Dramatiq + SQLAlchemy + asyncio\n - 🆕 Dramatiq + Django\n - 🆕 RabbitMQ + SQLAlchemy\n - 🆕 RabbitMQ + SQLAlchemy + asyncio\n - 🆕 RabbitMQ + Djagno\n\n\n# Example FastAPI + Kafka + SQLAlchemy\n```python\nfrom fastapi import FastAPI\nfrom outbox_streaming.kafka.sqlalchemy import SQLAlchemyKafkaOutbox\nfrom sqlalchemy import orm\n\nfrom app import models, db\nfrom app.config import config\nfrom app.schemas import TodoCreate\n\napp = FastAPI()\n\n# create instance of SQLAlchemyKafkaOutbox\noutbox = SQLAlchemyKafkaOutbox(\n    engine=db.engine,\n    kafka_servers=config.KAFKA_SERVERS,\n)\n\n# Run separate tread that monitor outbox table and publish messages to Kafka. It\'s not recommended for production,\n# but it\'s handy for development\noutbox.publisher.run_daemon()\n\nSession = orm.sessionmaker(bind=db.engine)\n\n# create outbox tables \noutbox.storage.create_tables(engine=db.engine)\n\n\n@app.post(\'/todos\')\ndef create_todo(create: TodoCreate) -> str:\n\n    with Session() as session:\n\n        # create new object\n        todo = models.Todo(text=create.text)\n\n        session.add(todo)\n\n        # create kafka event in outbox table\n        outbox.save(\n            session=session,\n            topic=\'todo_created\',\n            value=todo.to_dict(),\n        )\n\n        # commit changes in database\n        session.commit()\n        \n    # publisher will pick up kafka message from outbox table and will send it kafka topic\n\n    return "OK"\n\n```\n',
    'author': 'Yevhenii Hyzyla',
    'author_email': 'hyzyla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
