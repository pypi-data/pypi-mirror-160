from typing import Optional

import click

from anyscale.cli_logger import BlockLogger
from anyscale.cloud import get_cloud_id_and_name
from anyscale.controllers.base_controller import BaseController


class ExperimentalIntegrationsController(BaseController):
    def __init__(
        self, log: BlockLogger = BlockLogger(), initialize_auth_api_client: bool = True
    ):
        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.log.open_block("Output")

    # TODO(nikita): Use discriminated union types for cloud_id/cloud_name
    def enable_wandb_integration(
        self, cloud_id: Optional[str], cloud_name: Optional[str]
    ):
        """
        Enables W&B integration for the current user for the provided cloud. This
        is currently only implemented for AWS clouds.
        """
        # Assumes only one of cloud_id and cloud_name is passed. This should be checked with
        # a user friendly error message at the command layer.
        assert (
            bool(cloud_id) + bool(cloud_name) == 1
        ), "Must provide only one of --cloud_id or --cloud_name."

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(
            cloud_id=cloud_id
        ).result
        if cloud.provider != "AWS":
            raise click.ClickException(
                "W&B integration is currently only supported for AWS clouds."
            )

        user_id = self.api_client.get_user_info_api_v2_userinfo_get().result.id

        self.api_client.enable_wandb_integration_api_v2_experimental_integrations_enable_wandb_integration_cloud_id_post(
            cloud_id=cloud_id
        )

        steps = f"""
            1. Place your W&B API key in the AWS secrets manager associated with your Anyscale cloud account. The secret key should be `wandb_api_key_{user_id}`.
            2. Allow Anyscale clusters started in {cloud_name} to access your secret store for the cloud by running `anyscale cloud secrets --cloud-name {cloud_name}`.
            3. Run a production job using ray.air.callbacks.wandb.WandbLoggerCallback in your code. No parameters need to be passed to WandbLoggerCallback to use this integration.
            """
        self.log.info(
            f"Enabled W&B integration for cloud {cloud_name}. Please follow the steps below to use the integration:\n{steps}"
        )

        # TODO(nikita): Link to documentation here
        # docs_url = "N/A"
        # self.log.info(f"Please find more detailed instructions on using this integration at {docs_url}")
