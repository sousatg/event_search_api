import unittest

from flask import current_app
from config.api_config import ApiConfig
from api.create_app import create_app
# from sqlalchemy_utils import database_exists, create_database


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        ApiConfig.DEBUG = False
        ApiConfig.TESTING = True

        self._app = create_app(ApiConfig)
        self._app_context = self._app.app_context()
        self._app_context.push()

        self._client = self._app.test_client()

    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        self._app_context.pop()

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
