import os
import connexion

from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver

from elasticsearchsetup.elasticsearch import elasticSearchIndex,elasticSearchFactory
from mappersetup.elasticsearchmapperconf import room_mapping


def configure(binder: Binder) -> Binder:

    binder.bind(
        elasticSearchIndex,
        elasticSearchIndex(
            elasticSearchFactory(
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
    app= connexion.App(__name__, specification_dir='swagger/')
    app.add_api('indexer.yaml',resolver= RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    app.run(host='0.0.0.0',port=9090, debug=True)

