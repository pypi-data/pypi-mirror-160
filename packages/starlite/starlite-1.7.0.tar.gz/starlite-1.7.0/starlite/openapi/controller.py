from typing import TYPE_CHECKING

from orjson import OPT_INDENT_2, dumps

from starlite.connection import Request
from starlite.controller import Controller
from starlite.enums import MediaType, OpenAPIMediaType
from starlite.exceptions import ImproperlyConfiguredException
from starlite.handlers import get

if TYPE_CHECKING:
    from openapi_schema_pydantic.v3.v3_1_0.open_api import OpenAPI


class OpenAPIController(Controller):
    path = "/schema"
    styles = """
        body { margin: 0; padding: 0 }
    """
    redoc_version = "next"
    dumped_schema = ""

    @staticmethod
    def schema_from_request(request: Request) -> "OpenAPI":
        """Returns the openapi schema"""
        if not request.app.openapi_schema:  # pragma: no cover
            raise ImproperlyConfiguredException("Starlite has not been instantiated with OpenAPIConfig")
        return request.app.openapi_schema

    @get(path="/openapi.yaml", media_type=OpenAPIMediaType.OPENAPI_YAML, include_in_schema=False)
    def retrieve_schema_yaml(self, request: Request) -> "OpenAPI":
        """Returns the openapi schema"""
        return self.schema_from_request(request)

    @get(path="/openapi.json", media_type=OpenAPIMediaType.OPENAPI_JSON, include_in_schema=False)
    def retrieve_schema_json(self, request: Request) -> "OpenAPI":
        """Returns the openapi schema"""
        return self.schema_from_request(request)

    @get(media_type=MediaType.HTML, include_in_schema=False)
    def redoc(self, request: Request) -> str:  # pragma: no cover
        """Endpoint that serves Redoc"""
        schema = self.schema_from_request(request)
        if self.dumped_schema == "":
            self.dumped_schema = dumps(schema.json(by_alias=True, exclude_none=True), option=OPT_INDENT_2).decode(
                "utf-8"
            )
        head = f"""
          <head>
            <title>{schema.info.title}</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/redoc@{self.redoc_version}/bundles/redoc.standalone.js"></script>
            <style>
                {self.styles}
            </style>
          </head>
        """
        body = f"""
          <body>
            <div id='redoc-container'/>
            <script type="text/javascript">
                Redoc.init(
                    JSON.parse({self.dumped_schema}),
                    undefined,
                    document.getElementById('redoc-container')
                )
            </script>
          </body>
        """
        return f"""
        <!DOCTYPE html>
            <html>
                {head}
                {body}
            </html>
        """
