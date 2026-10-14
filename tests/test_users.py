from typing import Optional

import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_GROUP,
    TEST_ROLE,
    TEST_USER,
)
from pytest import FixtureRequest

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

# User Groups


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "service,group",
    [
        (None, None),
        ("default", None),
        (None, TEST_GROUP),
    ],
)
def test_get_users(
    test_geoserver: GeoServer,
    service: Optional[str],
    group: Optional[str],
    request: FixtureRequest,
) -> None:
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)

    data = test_geoserver.get_users(service=service, group=group)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_users_invalid(test_geoserver: GeoServer) -> None:
    with pytest.raises(ValueError):
        test_geoserver.get_users(service="not-both", group="not-both")


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("username,service", [("test", None), ("test2", "default")])
def test_create_user(test_geoserver: GeoServer, username: str, service: Optional[str]) -> None:
    body = {
        "user": {
            "userName": username,
            "password": "password",
            "enabled": True,
        }
    }

    msg = test_geoserver.create_user(body=body, service=service)
    assert isinstance(msg, str)


# Add parameters


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("username,service", [("test", None), ("test2", "default")])
def test_update_user(test_geoserver: GeoServer, username: str, service: Optional[str]) -> None:
    data = test_geoserver.get_users()
    user = next((u for u in data["users"] if u["userName"] == username), None)
    assert user is not None

    user["enabled"] = False
    msg = test_geoserver.update_user(username, body={"user": user}, service=service)
    assert isinstance(msg, str)

    data = test_geoserver.get_users()
    user = next((u for u in data["users"] if u["userName"] == username), None)
    assert user is not None
    assert user["enabled"] is False


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("username,service", [("test", None), ("test2", "default")])
def test_delete_user(test_geoserver: GeoServer, username: str, service: Optional[str]) -> None:
    msg = test_geoserver.delete_user(username, service=service)
    assert isinstance(msg, str)

    # GeoServer 2.x answers 404 for a missing user, 3.x answers 400.
    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_user("not-found")
    assert e_info.value.status_code in (400, 404)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("service", [None, "default"])
def test_get_user_groups(test_geoserver: GeoServer, test_user: str, service: Optional[str]) -> None:
    data = test_geoserver.get_user_groups(user=test_user, service=service)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("group,service", [("tmp-group", None), ("tmp-group-default", "default")])
def test_create_group(test_geoserver: GeoServer, group: str, service: Optional[str]) -> None:
    msg = test_geoserver.create_user_group(group, service=service)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.create_user_group(group, service=service)
    status_code = e_info.value.status_code
    assert status_code >= 400 and status_code < 500


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("service", [None, "default"])
def test_create_user_to_group(
    test_geoserver: GeoServer,
    test_user: str,
    test_group: str,
    service: Optional[str],
) -> None:
    msg = test_geoserver.associate_user(user=test_user, group=test_group, service=service)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("service", [None, "default"])
def test_delete_user_from_group(
    test_geoserver: GeoServer,
    test_user: str,
    test_group: str,
    service: Optional[str],
) -> None:
    msg = test_geoserver.disassociate_user(user=test_user, group=test_group, service=service)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("group,service", [("tmp-group", None), ("tmp-group-default", "default")])
def test_delete_group(test_geoserver: GeoServer, group: str, service: Optional[str]) -> None:
    msg = test_geoserver.delete_user_group(group, service=service)
    assert isinstance(msg, str)

    # GeoServer 2.x answers 404 for a missing group, 3.x answers 400.
    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_user_group(group, service=service)
    assert e_info.value.status_code in (400, 404)


# Roles


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "service,group,user",
    [
        (None, None, None),
        ("default", None, None),
        (None, TEST_GROUP, None),
        ("default", TEST_GROUP, None),
        ("default", None, TEST_USER),
    ],
)
def test_get_roles(
    test_geoserver: GeoServer,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    data = test_geoserver.get_roles(service=service, group=group, user=user)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "service,group,user",
    [
        (None, None, TEST_USER),
        (None, TEST_GROUP, TEST_USER),
        ("default", TEST_GROUP, TEST_USER),
    ],
)
def test_get_roles_invalid(
    test_geoserver: GeoServer,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    with pytest.raises(ValueError):
        test_geoserver.get_roles(service=service, user=user, group=group)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("role", ["tmp-role"])
def test_create_role(test_geoserver: GeoServer, role: str) -> None:
    msg = test_geoserver.create_role(role)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("role", ["tmp-role"])
def test_delete_role(test_geoserver: GeoServer, role: str) -> None:
    msg = test_geoserver.delete_role(role)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "role,service,group,user",
    [
        ("role-service", "default", None, None),
        (TEST_ROLE, None, None, TEST_USER),
        (TEST_ROLE, "default", None, TEST_USER),
        (TEST_ROLE, None, TEST_GROUP, None),
        (TEST_ROLE, "default", TEST_GROUP, None),
    ],
)
def test_associate_role(
    test_geoserver: GeoServer,
    role: str,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if role == TEST_ROLE:
        role = request.getfixturevalue(role)
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    msg = test_geoserver.associate_role(role=role, service=service, group=group, user=user)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "role,service,group,user",
    [
        (TEST_ROLE, None, TEST_USER, TEST_GROUP),
        (TEST_ROLE, "default", TEST_USER, TEST_GROUP),
    ],
)
def test_associate_role_invalid(
    test_geoserver: GeoServer,
    role: str,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if role == TEST_ROLE:
        role = request.getfixturevalue(role)
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    with pytest.raises(ValueError):
        test_geoserver.associate_role(role=role, user=user, group=group, service=service)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "role,service,group,user",
    [
        ("role-service", "default", None, None),
        (TEST_ROLE, None, None, TEST_USER),
        (TEST_ROLE, "default", None, TEST_USER),
        (TEST_ROLE, None, TEST_GROUP, None),
        (TEST_ROLE, "default", TEST_GROUP, None),
    ],
)
def test_disassociate_role(
    test_geoserver: GeoServer,
    role: str,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if role == TEST_ROLE:
        role = request.getfixturevalue(role)
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    msg = test_geoserver.disassociate_role(role=role, service=service, group=group, user=user)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "role,service,group,user",
    [
        (TEST_ROLE, None, TEST_USER, TEST_GROUP),
        (TEST_ROLE, "default", TEST_USER, TEST_GROUP),
    ],
)
def test_disassociate_role_invalid(
    test_geoserver: GeoServer,
    role: str,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if role == TEST_ROLE:
        role = request.getfixturevalue(role)
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    with pytest.raises(ValueError):
        test_geoserver.disassociate_role(role=role, user=user, group=group, service=service)
