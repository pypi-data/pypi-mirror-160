import json
import os
from unittest.mock import Mock, mock_open, patch

import click
import pytest

from anyscale.client.openapi_client import CreateProductionService, ProductionJobConfig
from anyscale.controllers.service_controller import ServiceController


@pytest.mark.parametrize("use_default_project", [True, False])
@pytest.mark.parametrize("access", ["public", "private"])
def test_update_service(
    mock_auth_api_client, use_default_project: bool, access: str
) -> None:
    config_dict = {
        "entrypoint": "mock_entrypoint",
        "build_id": "mock_build_id",
        "compute_config_id": "mock_compute_config_id",
        "healthcheck_url": "mock_healthcheck_url",
        "access": access,
    }
    service_controller = ServiceController()
    if use_default_project:
        mock_infer_project_id = Mock(return_value="mock_default_project_id")
    else:
        mock_infer_project_id = Mock(return_value="mock_project_id")

    mock_validate_successful_build = Mock()

    with patch(
        "builtins.open", mock_open(read_data=json.dumps(config_dict))
    ), patch.multiple(
        "anyscale.controllers.service_controller",
        infer_project_id=mock_infer_project_id,
    ), patch.multiple(
        "anyscale.controllers.job_controller",
        validate_successful_build=mock_validate_successful_build,
    ), patch.multiple(
        "os.path", exists=Mock(return_value=True)
    ):
        service_controller.deploy(
            "mock_config_file", name="mock_name", description="mock_description",
        )

    service_controller.api_client.apply_service_api_v2_decorated_ha_jobs_apply_service_put.assert_called_once_with(
        CreateProductionService(
            name="mock_name",
            description="mock_description",
            project_id="mock_default_project_id"
            if use_default_project
            else "mock_project_id",
            config=ProductionJobConfig(
                **{
                    "entrypoint": "mock_entrypoint",
                    "build_id": "mock_build_id",
                    "compute_config_id": "mock_compute_config_id",
                }
            ),
            healthcheck_url="mock_healthcheck_url",
            access=access,
        )
    )


def test_service_submit_parse_logic(mock_auth_api_client) -> None:
    service_controller = ServiceController()
    service_controller.generate_config_from_entrypoint = Mock()  # type: ignore
    service_controller.generate_config_from_file = Mock()  # type: ignore
    service_controller.deploy_from_config = Mock()  # type: ignore

    # We are not in a workspace, so entrypoint should not be allowed
    with pytest.raises(click.ClickException):
        service_controller.deploy(
            "file", None, None, entrypoint=["entrypoint"], is_entrypoint_cmd=False
        )

    with pytest.raises(click.ClickException):
        service_controller.deploy(
            "file", None, None, entrypoint=["entrypoint"], is_entrypoint_cmd=True
        )

    with pytest.raises(click.ClickException):
        service_controller.deploy(
            "file",
            None,
            None,
            entrypoint=["entrypoint", "commands"],
            is_entrypoint_cmd=True,
        )

    # Simulate a workspace
    with patch.dict(
        os.environ, {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "fake_workspace_id"}
    ):
        # Fails due to is_entrypoint_cmd being False
        with pytest.raises(click.ClickException):
            service_controller.deploy(
                "file", None, None, entrypoint=["entrypoint"], is_entrypoint_cmd=False
            )

        mock_config = Mock()
        service_controller.generate_config_from_file.return_value = mock_config
        service_controller.deploy(
            "file", None, None, entrypoint=[], is_entrypoint_cmd=False
        )
        service_controller.generate_config_from_file.assert_called_once_with(
            "file", None, None, healthcheck_url=None
        )
        service_controller.deploy_from_config.assert_called_once_with(mock_config)
        service_controller.generate_config_from_file.reset_mock()
        service_controller.deploy_from_config.reset_mock()

        mock_config = Mock()
        service_controller.generate_config_from_entrypoint.return_value = mock_config
        service_controller.deploy(
            "file", None, None, entrypoint=["entrypoint"], is_entrypoint_cmd=True
        )
        service_controller.generate_config_from_entrypoint.assert_called_once_with(
            ["file", "entrypoint"], None, None, healthcheck_url=None
        )
        service_controller.deploy_from_config.assert_called_once_with(mock_config)
