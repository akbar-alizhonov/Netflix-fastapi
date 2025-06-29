from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends

from src.config.dependencies import get_elastic_client

router = APIRouter(prefix="/elastic", tags=["Elasticsearch"])


async def update_index(
        es_client: Annotated[AsyncElasticsearch, Depends(get_elastic_client)]
):
    await es_client.bulk(

    )
