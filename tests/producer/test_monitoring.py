import unittest
from unittest.mock import Mock

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop, TestServer

from kwebmon.producer.utils import get_sites
from kwebmon.producer.monitoring import Monitor

from tests import fixture_path

sites = get_sites(fixture_path("sites_localhost.json"))
mock_cb = Mock()
monitor = Monitor(sites, mock_cb)


class TestMonitoring(AioHTTPTestCase):
    @staticmethod
    async def get_application():
        async def ok(request):
            return web.Response(text="Example Domain")

        async def bad_content(request):
            return web.Response(text="Wrong text")

        async def not_found(request):
            return web.Response(status=404)

        app = web.Application()
        app.router.add_get("/", ok)
        app.router.add_get("/bad_content", bad_content)
        app.router.add_get("/404", not_found)
        return app

    @staticmethod
    async def get_server(app):
        return TestServer(app, scheme="http", host="127.0.0.1", port=8080)

    @unittest_run_loop
    async def test_check(self):
        await monitor.check()

        self.assertEqual(mock_cb.call_count, 6)

        calls = mock_cb.call_args_list

        # call({"url": str, "pattern": Optional[str], {
        #     "response_time": Optional[float], - if response.ok
        #     "status_code": Optional[int], - if no errors
        #     "is_content_valid": Optional[bool], - if pattern specified
        #     "error": Optional[str] - only key in case of errors
        # })
        self.assertEqual(calls[0].args[0]["url"], "http://127.0.0.1:8080")
        self.assertEqual(calls[0].args[1]["status_code"], 200)
        self.assertIsInstance(calls[0].args[1]["response_time"], float)
        self.assertEqual(calls[0].args[1]["is_content_valid"], True)
        self.assertEqual(len(calls[0].args[1]), 4)

        self.assertEqual(calls[1].args[0]["url"], "http://127.0.0.1:8080/404")
        self.assertIsInstance(calls[1].args[1]["response_time"], float)
        self.assertEqual(calls[1].args[1]["status_code"], 404)
        self.assertEqual(len(calls[1].args[1]), 3)

        self.assertEqual(
            calls[2].args[0]["url"], "http://127.0.0.1:8080/bad_content"
        )
        self.assertEqual(calls[2].args[1]["is_content_valid"], False)
        self.assertEqual(calls[2].args[1]["status_code"], 200)
        self.assertEqual(len(calls[2].args[1]), 4)

        self.assertEqual(
            calls[3].args[0]["url"], "http://127.0.0.1:8080/?q=test"
        )
        self.assertEqual(calls[3].args[1]["is_content_valid"], True)
        self.assertEqual(len(calls[3].args[1]), 4)

        self.assertEqual(
            calls[4].args[0]["url"], "http://127.0.0.1:8080/?query"
        )
        self.assertIsInstance(calls[4].args[1]["response_time"], float)
        self.assertEqual(calls[4].args[1]["status_code"], 200)
        self.assertEqual(len(calls[4].args[1]), 3)

        self.assertEqual(
            calls[5].args[0]["url"], "http://bad_domain.shouldnotexist"
        )
        self.assertEqual(calls[5].args[1]["error"], "Invalid domain")
        self.assertEqual(len(calls[5].args[1]), 2)


if __name__ == "__main__":
    unittest.main()
