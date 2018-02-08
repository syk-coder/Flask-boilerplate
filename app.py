import connexion

from connexion.resolver import RestyResolver
from flask_injector import FlaskInjector
from injector import Binder

from services.provider import ItemsProvider


def configure(binder: Binder) -> Binder:
    binder.bind(
        ItemsProvider,
        ItemsProvider([{"Name": "Test1"}])
    )


if __name__ == '__main__':
    app = connexion.App(__name__, port=9090, specification_dir="swagger/")
    app.add_api('sample_app.yaml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    app.run()
