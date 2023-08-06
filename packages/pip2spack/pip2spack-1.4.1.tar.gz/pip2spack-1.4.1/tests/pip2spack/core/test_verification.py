from collections import namedtuple
from http import HTTPStatus
from json import dumps

import pytest
from pytest_mock import MockFixture

from pip2spack.core.verification import Verification
from tests.pip2spack.core.mocks import PYPI_RESPONSES

Response = namedtuple("Response", "status_code content")


@pytest.fixture
def mock_requests_get_response_from_pypi_for_jsl(mocker: MockFixture) -> None:
    mocker.patch(
        "pip2spack.core.verification.requests.get",
        return_value=Response(
            status_code=HTTPStatus.OK, content=dumps(PYPI_RESPONSES["jsl"])
        ),
    )


@pytest.fixture
def mock_requests_get_404_response_from_pypi(mocker: MockFixture) -> None:
    mocker.patch(
        "pip2spack.core.verification.requests.get",
        return_value=Response(
            status_code=HTTPStatus.NOT_FOUND, content={"message": "Not Found"}
        ),
    )


class TestVerification:
    def test_verification__creation_of_object_success_story(
        self, mock_requests_get_response_from_pypi_for_jsl: None
    ) -> None:
        assert (
            Verification(
                [
                    "jsl",
                ]
            ).available_packages
            == PYPI_RESPONSES
        )

    def test_verification__negative__provide_not_existing_package_name(
        self, mock_requests_get_404_response_from_pypi
    ) -> None:
        assert not Verification(
            [
                "qwertyuiop_not_existing_package",
            ]
        ).available_packages, "Package should not exists"
