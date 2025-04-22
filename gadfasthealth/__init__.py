import http
import inspect
import typing

import fastapi


class Health:
    def __init__(self, *endpoints: typing.Tuple[str, typing.Callable, ...]):
        self.router = fastapi.APIRouter(tags=["Health Probes"])
        self.setup(endpoints)

    def setup(self, endpoints: typing.Tuple[typing.Tuple[str, typing.Callable, ...], ...]) -> None:
        for endpoint in endpoints:
            if not isinstance(endpoint, tuple):
                path, depends = endpoint, []
            else:
                path, depends = endpoint[0], list(endpoint[1:])

            name = path.strip("/").split("/")[-1]

            self.router.add_api_route(
                path,
                self.endpoint(depends),
                summary=f"Kubernetes {name} probe",
                operation_id=f"{name}_probe",
            )

    @staticmethod
    def endpoint(depends: typing.List[typing.Callable]) -> typing.Callable[..., fastapi.Response]:
        async def _endpoint(**dependencies: typing.Dict[str, typing.Any]) -> fastapi.Response:
            return fastapi.Response(
                status_code=http.HTTPStatus.OK
                if all(result is True for result in dependencies.values())
                else http.HTTPStatus.SERVICE_UNAVAILABLE
            )

        params = [
            inspect.Parameter(
                name=depend.__name__,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=bool,
                default=fastapi.Depends(depend),
            )
            for depend in depends
        ]

        _endpoint.__signature__ = inspect.Signature(params)

        return _endpoint


__all__ = ["Health"]
