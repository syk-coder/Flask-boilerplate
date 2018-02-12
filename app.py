import os

import connexion

from connexion.resolver import RestyResolver
from flask_injector import FlaskInjector
from injector import Binder

from configuration.es_mapper import room_mapping
from services.elasticsearch import ElasticSearchIndex, ElasticSearchFactory
from services.provider import ItemsProvider


def configure(binder: Binder) -> Binder:
    binder.bind(
        ItemsProvider,
        ItemsProvider([{"Name": "Test1"}]),
        ElasticSearchIndex,
        ElasticSearchIndex(
            ElasticSearchFactory(
                os.environ['ELASTICSEARCH_HOST'],
                os.environ['ELASTICSEARCH_PORT']
            ),
            'rooms',
            'room',
            room_mapping
        )
    )

    return binder


if __name__ == '__main__':
    app = connexion.App(__name__, port=9090, specification_dir="swagger/")
    app.add_api('sample_app.yaml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    app.run()
