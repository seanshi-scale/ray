#!/usr/bin/env python3
from ci.ray_ci.utils import omit_tests_by_state
from ray_release.configs.global_config import init_global_config
from ray_release.bazel import bazel_runfile
import sys


def main():
    """
    Filter tests based on test targets and test state.
    Read list of test targets from file path.
    Write back into the same file path with tests of specified state removed.

    Args:
        test_targets_file_path: Path to file containing list of test targets.
        test_state: Test state to filter by.
            Use string representation from ray_release.test.TestState class.
    """
    # Initialize global config
    init_global_config(bazel_runfile("release/ray_release/configs/oss_config.yaml"))

    # Process arguments
    test_targets = sys.stdin.read()
    if len(sys.argv) == 2:
        test_state = sys.argv[1]
    else:
        raise ValueError("Invalid number of arguments.")

    filtered_test_targets = omit_tests_by_state(
        test_targets.split("\\n")[:-1], test_state
    )
    filtered_test_targets = [test[2:] for test in filtered_test_targets]  # Remove "//"
    print("\n".join(filtered_test_targets))  # Write back to stdout


if __name__ == "__main__":
    main()