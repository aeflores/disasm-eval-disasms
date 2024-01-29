# Disassembler Evaluation - Disassemblers
The extractors and capnp encoders that extract and output disassemblers' results into a capnp file, formatted using [pangineDSM-import/capnp-rst](https://github.com/pangine/pangineDSM-import/tree/main/capnp-rst)

Presently support:
 - BAP
 - ddisasm
 - Ghidra
 - Radare2
 - ROSE

The data needs to be given in the format of the output of [disasm-eval-sources](https://github.com/pangine/disasm-eval-sources).

It is highly recommend to use docker images for execution.

------------------------------
You need to install the docker image [llvmmc-resolver](https://github.com/pangine/llvmmc-resolver) before running this.
To install the docker images:
```bash
docker build -t pangine/disasms-base -f dockerfiles/Dockerfile.disasms-base .
docker build -t pangine/ghidra -f dockerfiles/Dockerfile.ghidra .
docker build -t pangine/bap -f dockerfiles/Dockerfile.bap .
docker build -t pangine/ddisasm -f dockerfiles/Dockerfile.ddisasm .
docker build -t pangine/radare2 -f dockerfiles/Dockerfile.r2 .
docker build -t pangine/rose -f dockerfiles/Dockerfile.rose .
```

------------------------------
To execute a disassembler and the extractor

Here we use Ghidra as an example, the other disassemblers are the same except that you need to change the `ghidra` in the executable names to other disassemblers.

Assume that you have results from the [disasm-eval-sources](https://github.com/pangine/disasm-eval-sources) project for x64 gnu-gcc-7.5.0 under */path_to_test_cases/x86_64-pc-linux-gnu-gcc-7.5.0/%2dO3/*, and you want the disassembly result for **openssh-7.1p2** (there should be a *bin/openssh-7.1p2* subdirectory inside the compiled projects folder).

The llvm triple for this test case should be **x86_64-pc-linux-gnu-elf**

Here are the commands that you want to execute:
```bash
OUTPUTDIR="/path_to_test_cases"
TESTCASE="x86_64-pc-linux-gnu-gcc-7.5.0/%2dO3"
LLVMTRIPLE="x86_64-pc-linux-gnu-elf"
PROJECTNAME="openssh-7.1p2"

docker run --rm -it -v ${OUTPUTDIR}:/output \
-e LLVMTRIPLE="${LLVMTRIPLE}" \
-e TESTCASE="${TESTCASE}" \
-e PROJECTNAME="${PROJECTNAME}" \
pangine/ghidra /bin/bash -i -c \
'/bin/time -v pgndsm-eval-ghidra -sd "${PROJECTNAME}" /output/"${TESTCASE}" && pgndsm-eval-ghidra-cvt -sd "${PROJECTNAME}" -l ${LLVMTRIPLE} /output/"${TESTCASE}"'
```

You will find the both the capnp output at */path_to_test_cases/x86_64-pc-linux-gnu-gcc-7.5.0/%2dO3/ghidra/openssh-7.1p2/\*_ghidra.out*.

You can choose not to use the **-sd** argument, and the disassembler will run for all the test cases in projects folder.
