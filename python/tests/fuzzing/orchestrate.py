import argparse
import itertools
import subprocess
import os
import os.path

# For some reason atheris cannot run fuzzing more than once per
# process, hence the subprocess dance we do here.

# For some reason the first run of this script will fail to build the
# C extension. Trying to debug this usually causes the script to begin
# working; maybe try running `uv build`?

DIVIDER = """

##### Fuzzing with {} sanitizer/{} #####

"""


def fuzz_package(repo_directory, target_directory, sanitizer, test_method, runs, clang):
    sanitizer_cflag, sanitizer_library = sanitizer
    # Build base92.
    subprocess.run(
        [
            os.path.join(args.target_directory, "venv/bin/pip"),
            "install",
            repo_directory,
        ],
        env={
            "CC": clang,
            "CFLAGS": f"-fsanitize={sanitizer_cflag},fuzzer-no-link",
            "LDSHARED": f"{clang} -shared",
        },
        check=True,
    )

    # Get atheris path to link.
    process = subprocess.run(
        [
            os.path.join(args.target_directory, "venv/bin/python3"),
            "-c",
            "import atheris; print(atheris.path())",
        ],
        capture_output=True,
        check=True,
    )
    atheris_path = process.stdout.decode("utf8").strip()

    # Run fuzzer.
    subprocess.run(
        [
            os.path.join(args.target_directory, "venv/bin/python3"),
            os.path.join(repo_directory, f"tests/fuzzing/{test_method}.py"),
            f"-runs={runs}",
        ],
        env={"LD_PRELOAD": f"{atheris_path}/{sanitizer_library}_with_fuzzer.so"},
    )


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "target_directory", help="Target directory to place the test venv in."
    )
    argparser.add_argument("-r", "--runs", type=int, default=100000)
    argparser.add_argument("--clang", default="/usr/bin/clang-19")

    args = argparser.parse_args()

    # Make sure the directory exists.
    os.makedirs(args.target_directory, exist_ok=True)

    # Create a venv.
    subprocess.run(
        ["python3", "-m", "venv", os.path.join(args.target_directory, "venv")],
        check=True,
    )

    # Install atheris.
    subprocess.run(
        [os.path.join(args.target_directory, "venv/bin/pip"), "install", "atheris"]
    )

    # This file lives in /tests/fuzzing/
    repo_directory = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    )

    sanitizers = [("address", "asan"), ("undefined", "ubsan")]
    functions = ["pyencode", "pydecode", "cencode", "cdecode"]
    for sanitizer, function in itertools.product(sanitizers, functions):
        print(DIVIDER.format(sanitizer[0], function))
        fuzz_package(
            repo_directory,
            args.target_directory,
            sanitizer,
            function,
            args.runs,
            args.clang,
        )
