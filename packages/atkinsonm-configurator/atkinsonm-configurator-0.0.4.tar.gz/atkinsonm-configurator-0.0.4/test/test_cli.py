from click.testing import CliRunner
from configurator.cli import cli


def test_hello():
    runner = CliRunner()
    result = runner.invoke(cli, ["hello"])
    assert result.exit_code == 0
    assert result.output == "Hello from Configurator!\n"
