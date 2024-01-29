from genericpath import isdir
from typing import Optional
import docker
from pathlib import Path
import argparse


def get_llvm_triple(path_name: str):
    """
    Get llvm triple depending on the name
    """
    if path_name.startswith("x86_64"):
        first_half = "x86_64"
    else:
        first_half = "x86"
    if "msvc" in path_name:
        second_half = "-PC-Win32-MSVC-COFF"
    else:
        second_half = "-PC-Linux-GNU-ELF"
    return first_half + second_half


def run_disassembler(
    disassembler: str, path: Path, skip: Optional[str], only: Optional[str]
):
    """
    Run disassembler on all the testcases found in path.
    Optionaly the testcases that contain the keyword `skip`
    will be skipped.
    """
    client = docker.from_env()
    for compiler in path.iterdir():
        if not compiler.is_dir():
            continue
        if skip is not None and skip in compiler.name:
            print(f"skipping {compiler}")
            continue
        if only is not None and only not in compiler.name:
            print(f"skipping {compiler}")
            continue
        for test_case in compiler.iterdir():
            print(f"Running {disassembler} on {test_case}")
            llvm_triple = get_llvm_triple(compiler.name)
            internal_test_case = compiler.name + "/" + test_case.name
            docker_command = (
                f"pgndsm-eval-{disassembler} /output/{internal_test_case} &&"
                f" pgndsm-eval-{disassembler}-cvt -l {llvm_triple}"
                f" /output/{internal_test_case}"
            )
            container = client.containers.run(
                image=f"pangine/{disassembler}",
                remove=True,
                detach=False,
                tty=True,
                volumes={path: {"bind": "/output", "mode": "rw"}},
                command=["/bin/bash", "-i", "-c", docker_command],
            )
            print(container.decode())


def main():
    parser = argparse.ArgumentParser(
        description="Run disassembler on the entire database"
    )
    parser.add_argument(
        "disassembler", help="disassembler", choices=["ddisasm", "ghidra", "radare2", "bap"]
    )
    parser.add_argument("dataset", type=Path, help="disassembler")
    parser.add_argument("--skip", type=str, help="directory pattern to skip")
    parser.add_argument("--only", type=str, help="directory pattern to analyze")
    args = parser.parse_args()
    run_disassembler(args.disassembler, args.dataset, args.skip, args.only)


if __name__ == "__main__":
    main()
