# ---------------------------------------------------------------------------- #

import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------- #

from app import app

# ---------------------------------------------------------------------------- #


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_version = "/api/v1"

    def test_health(self):
        response = self.client.get(f"{self.api_version}/utils/health")
        assert response.status_code == 200
        assert response.json()["health"] == "healthy"


# ---------------------------------------------------------------------------- #
