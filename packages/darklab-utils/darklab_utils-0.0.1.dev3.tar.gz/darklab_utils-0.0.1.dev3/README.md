
# Library of darklab utility programms

contains:

## Scripts:

A package built on top of argparse.
intended usage to be a python version of makefile, for uniform command acceess to run tests/lints in dev env and CI

## code example:

```py
import darklab_utils as utils

class InputDataFactory(utils.AbstractInputDataFactory):

    @staticmethod
    def register_cli_arguments(argpase_reader: utils.ArgparseReader) -> utils.ArgparseReader:
        return argpase_reader \
            .add_argument("--cli_argument", type=str, default="example")

    @staticmethod
    def register_env_arguments(env_reader: utils.EnvReader) -> utils.EnvReader:
        return env_reader.add_arguments(
            env_argument1=env_reader["PWD"],
            env_argument2=env_reader.get("NOT_EXISTING_VAR", "default_value"),
        )

class MyScripts(utils.AbstractScripts):
    input_data_factory = InputDataFactory

    @utils.registered_action
    def build(self):
        self.shell(f"echo {self.globals.cli_argument}")

    @utils.registered_action
    def print(self):
        self.shell(f"echo {self.globals.env_argument1}")

    @utils.registered_action
    def example(self):
        args = self.globals.cli_reader \
            .add_argument("--argument", type=int, default=456) \
            .get_data()
        self.shell(f"echo debug_{args.argument}")

if __name__=="__main__":
    MyScripts().process()

    # run with `python scripts.py build`, `python scripts.py example --argument=123`
```

## Link to Pypi
https://pypi.org/project/darklab-utils/
