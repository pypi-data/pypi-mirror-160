import os

import httpx

from .request import BaseRequest


class Client:
    def __init__(
        self,
        token: str = None,
        endpoint: str = "https://api.captcha.run",
        use_async: bool = False,
        timeout: int = 10,
    ):
        self.endpoint = endpoint
        self.token = token or os.environ.get("CAPTCHARUN_TOKEN")

        params = dict(
            base_url=self.endpoint,
            headers={
                "User-Agent": "captcharun/client",
                "Authorization": f"Bearer {self.token}",
            },
            timeout=timeout,
        )

        self.use_async = use_async
        self.async_client = httpx.AsyncClient(**params)
        self.sync_client = httpx.Client(**params)

    def invoke(self, request: BaseRequest):
        return (
            self.invoke_async(request) if self.use_async else self.invoke_sync(request)
        )

    def invoke_sync(self, request: BaseRequest):
        resp = self.sync_client.request(
            request.method, request.path, params=request.params, json=request.data
        )
        resp.raise_for_status()
        return resp.json()

    async def invoke_async(self, request: BaseRequest):
        resp = await self.async_client.request(
            request.method, request.path, params=request.params, json=request.data
        )
        resp.raise_for_status()
        return resp.json()
