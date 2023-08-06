from dataclasses import dataclass

from elma.models.util import JsonSerializable


@dataclass
class AuthResponse(JsonSerializable):
    AuthToken: str
    SessionToken: str
    CurrentUserId: str
    CurrentUserName: str
    Lang: str

    @staticmethod
    def from_json(obj: dict):
        return AuthResponse(**obj)


@dataclass
class CheckPermissionsRequest(JsonSerializable):
    @dataclass
    class CheckPermission(JsonSerializable):
        Id: str
        ObjectId: str
        TypeUid: str

        @staticmethod
        def from_json(obj: dict):
            return CheckPermissionsRequest.CheckPermission(**obj)

    check_permissions: list

    @staticmethod
    def from_json(obj: dict):
        return CheckPermissionsResponse(**obj)


@dataclass
class CheckPermissionsResponse(JsonSerializable):
    Id: str
    ObjectId: str
    TypeUid: str

    @staticmethod
    def from_json(obj: dict):
        return CheckPermissionsResponse(**obj)


@dataclass
class ApiVersionResponse(JsonSerializable):
    Version: str
    Services: []

    @staticmethod
    def from_json(obj: dict):
        return ApiVersionResponse(**obj)
