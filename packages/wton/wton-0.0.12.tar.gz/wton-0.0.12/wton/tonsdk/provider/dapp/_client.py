import json
import codecs
from typing import Any, Dict, List, Optional
import asyncio
import aiohttp

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode
from pydantic import BaseModel


class ErrorMsg(BaseModel):
    message: str
    code: int


class DAppWrongResult(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return ". ".join([f"{error.message}, Code: {error.code}" for
                          error in self.errors])


class BroadcastQuery(BaseModel):
    boc: str
    timeout: int


class DAppClient:
    def __init__(self, graphql_url: str, broadcast_url: str, api_key: str):
        self.api_key = api_key
        self.broadcast_url = broadcast_url
        self.transport = AIOHTTPTransport(
            url=graphql_url, headers=self.__headers(is_json=False))

    async def query(self, queries: List[DocumentNode]) -> List[Any]:
        results = []

        async with Client(
            transport=self.transport,
            fetch_schema_from_transport=False,
        ) as session:
            for query in queries:
                result = await session.execute(query)
                results.append(result)

        return results

    async def broadcast(self, queries: List[BroadcastQuery], timeout=31) -> List[Any]:
        results = []
        timeout = aiohttp.ClientTimeout(total=timeout)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            for query in queries:
                async with session.post(self.broadcast_url, json=query.dict(), headers=self.__headers(is_json=True)) as resp:
                    results.append(await self.__parse_response(resp))

        return results

    def __headers(self, is_json):
        headers = {}

        if is_json:
            headers = {
                'Content-Type': 'application/json',
            }

        if self.api_key:
            headers['API-KEY'] = self.api_key

        return headers

    async def __parse_response(self, resp):
        try:
            resp = await resp.json()
        except Exception:  # TODO: catch correct exceptions
            raise DAppWrongResult(
                [ErrorMsg(message=resp.reason, code=resp.status)])

        if "errors" in resp and resp['errors']:
            errors = [ErrorMsg.parse_obj(error) for error in resp['errors']]
            raise DAppWrongResult(errors)

        return resp['data']
