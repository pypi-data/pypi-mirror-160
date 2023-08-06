import json
import os
from abc import ABC

from flask import request, Response, copy_current_request_context, Flask
from flask_api import status
from flask_caching import Cache
from prometheus_flask_exporter import PrometheusMetrics

from aylien_model_serving.app_factory import FlaskAppWrapper, InvalidRequest


def cache_key():
    @copy_current_request_context
    def my_key():
        return json.dumps(request.get_json())

    return my_key()


class CachedFlaskWrapper(FlaskAppWrapper):
    """specify a new app here -
    it gives the option to override app config specifically for cached apps"""

    app = Flask(__name__)
    cache = Cache(
        config={
            "CACHE_TYPE": os.environ.get(
                "CACHE_TYPE", os.environ.get("CACHE_TYPE", "SimpleCache")
            ),
            "CACHE_THRESHOLD": int(os.environ.get("CACHE_THRESHOLD", 100000)),
        }
    )
    metrics = PrometheusMetrics(app, group_by="endpoint", path="/__metrics")
    cache.init_app(app)

    @staticmethod
    @cache.cached(key_prefix=cache_key)
    def process_json(callable_handler):
        return FlaskAppWrapper.process_json(callable_handler)

    @staticmethod
    def create_app(routes=None):
        if routes is None:
            routes = []
        CachedFlaskWrapper.app.add_url_rule(
            "/__ping", view_func=FlaskAppWrapper.ping, methods=["GET"]
        )
        for route in routes:
            CachedFlaskWrapper.app.add_url_rule(
                route["endpoint"], view_func=route["callable"],
                methods=route["methods"]
            )  # is a list
        return CachedFlaskWrapper.app
