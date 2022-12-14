#!/usr/bin/python3

import re
import os
import json


def compile():
    print("Compiling Standard...")
    os.system(
        "gcc -o ./bin/matMulStd matrixMultiplication.c -O1 -fopt-info-vec-optimized")
    print("Compiling Vectorized...")
    os.system("gcc -o ./bin/matMulVec matrixMultiplication.c -ftree-vectorize -ffast-math -O1 -fopt-info-vec-optimized")
    print("Compiling With Intrinsics...")
    os.system(
        "gcc -o ./bin/matMulIntr matrixMultiplicationIntrinsics.c -mavx -O1 -fopt-info-vec-optimized")
    print("Finished compiling.")


def run(binary, runArg):

    print(f"Running {binary} with {runArg}x{runArg}...")
    os.system(
        f'perf stat -o ./perfOut -e L1-dcache-load,L1-dcache-load-misses,cache-references,cache-misses ./bin/{binary} {runArg}')
    print("Finished running.")

    with open("perfOut", 'r') as f:
        perfOut = f.read()
        l1CacheLoads = re.search(
            r'\s*((?:\d*\.)*\d*)\s*L1-dcache-load:u\s*', perfOut).group(1)
        l1CacheLoadMisses = re.search(
            r'\s*((?:\d*\.)*\d*)\s*L1-dcache-load-misses:u\s*', perfOut).group(1)
        cacheReferences = re.search(
            r'\s*((?:\d*\.)*\d*)\s*cache-references:u\s*', perfOut).group(1)
        cacheMisses = re.search(
            r'\s*((?:\d*\.)*\d*)\s*cache-misses:u\s*', perfOut).group(1)
        time = re.search(
            r'((?:\d*\.)*\d*,\d*)\s+seconds time elapsed\s*', perfOut).group(1)

        time = float(time.replace('.', '').replace(',', '.'))
        l1CacheLoadMisses = float(l1CacheLoadMisses.replace('.', ''))
        l1CacheLoads = float(l1CacheLoads.replace('.', ''))
        cacheMisses = float(cacheMisses.replace('.', ''))
        cacheReferences = float(cacheReferences.replace('.', ''))

    os.remove("perfOut")

    return {
        "binary": binary,
        "runArg": runArg,
        "l1CacheLoadMisses": l1CacheLoadMisses,
        "l1CacheLoads": l1CacheLoads,
        "cacheMisses": cacheMisses,
        "cacheReferences": cacheReferences,
        "l1CacheLoadMissRate": l1CacheLoadMisses / l1CacheLoads,
        "cacheMissRate": cacheMisses / cacheReferences,
        "time": time,
    }


runs = []

runArgs = [10, 25, 50,  100, 250, 500, 1000, 2500, 5000, 7500]

binaries = ["matMulStd", "matMulVec", "matMulIntr"]

compile()

for runArg in runArgs:
    for binary in binaries:

        currSample = {
            "binary": binary,
            "runArg": runArg,
            "times": [],
            "l1CacheLoadMisses": [],
            "l1CacheLoads": [],
            "cacheMisses": [],
            "cacheReferences": [],
            "l1CacheLoadMissRate": [],
            "cacheMissRate": [],
        }

        for i in range(10):
            print(f"Run {i+1}/10")
            result = run(binary, runArg)
            currSample["times"].append(result["time"])
            currSample["l1CacheLoadMisses"].append(
                result["l1CacheLoadMisses"])
            currSample["l1CacheLoads"].append(result["l1CacheLoads"])
            currSample["cacheMisses"].append(result["cacheMisses"])
            currSample["cacheReferences"].append(result["cacheReferences"])
            currSample["l1CacheLoadMissRate"].append(
                result["l1CacheLoadMissRate"])
            currSample["cacheMissRate"].append(result["cacheMissRate"])

        currSample["meanTime"] = sum(
            currSample["times"]) / len(currSample["times"])
        currSample["meanL1CacheLoadMisses"] = sum(
            currSample["l1CacheLoadMisses"]) / len(currSample["l1CacheLoadMisses"])
        currSample["meanL1CacheLoads"] = sum(
            currSample["l1CacheLoads"]) / len(currSample["l1CacheLoads"])
        currSample["meanCacheMisses"] = sum(
            currSample["cacheMisses"]) / len(currSample["cacheMisses"])
        currSample["meanCacheReferences"] = sum(
            currSample["cacheReferences"]) / len(currSample["cacheReferences"])
        currSample["meanL1CacheLoadMissRate"] = currSample["meanL1CacheLoadMisses"] / \
            currSample["meanL1CacheLoads"]
        currSample["meanCacheMissRate"] = currSample["meanCacheMisses"] / \
            currSample["meanCacheReferences"]

        runs.append(currSample)


with open("runs2.json", 'w') as f:
    f.write(json.dumps(runs, indent=4))
