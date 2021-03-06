""" Tests for pcf run command """

import pytest
from mock import patch
from pcf.cli.commands.run import run
from pcf.core.particle import Particle
from pcf.particle.aws.ec2.ec2_instance import EC2Instance
from pcf.quasiparticle.aws.ecs_instance_quasi.ecs_instance_quasi import ECSInstanceQuasi


class TestRun:
    """ Test 'pcf run' command against a particle and a quasiparticle from files """

    particle_pcf_name = "test_ec2"
    quasiparticle_pcf_name = "test_ecs_instance"

    @patch.object(EC2Instance, "apply", return_value=None)
    @pytest.mark.parametrize("config_file", ["pcf.json", "pcf.yml", "pcf.yaml"])
    def test_run_from_default_config_file(
        self, apply_mock, config_file, cli_runner, copy_pcf_config_file
    ):
        """ Ensure the run command will set the desired state to running for the
            particle loaded from each default PCF config file and apply changes
        """

        with cli_runner.isolated_filesystem():
            copy_pcf_config_file(config_file)
            result = cli_runner.invoke(run, [self.particle_pcf_name])

            expected = "Setting desired state of {0} to {1}".format(
                self.particle_pcf_name, "running"
            )
            assert expected in result.output
            assert result.exit_code == 0
            assert apply_mock.called

    @patch.object(EC2Instance, "apply", return_value=None)
    @pytest.mark.parametrize(
        "config_file", ["custom.json", "custom.yml", "custom.yaml"]
    )
    def test_run_with_custom_config_file(
        self, apply_mock, config_file, cli_runner, copy_pcf_config_file
    ):
        """ Ensure the run command will respect custom PCF config files specified with
            the --file or -f option
        """

        with cli_runner.isolated_filesystem():
            copy_pcf_config_file(config_file)
            result = cli_runner.invoke(run, [self.particle_pcf_name, "-f", config_file])

            expected = "Setting desired state of {0} to {1}".format(
                self.particle_pcf_name, "running"
            )
            assert expected in result.output
            assert result.exit_code == 0
            assert apply_mock.called
