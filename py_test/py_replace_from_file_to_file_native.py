import time
import os
import sys

print("\n====================================================")
print("❌ BENCHMARK: NATIVE PYTHON FILE-TO-FILE (WITHOUT DLL)")
print("====================================================")

source_path = os.path.abspath("d:\\input500.txt")
target_path = os.path.abspath("d:\\py_ff_native.txt")

dictionary = {
    b"_{pattern_01}_": b"replacement-1-0123456789",
    b"_{pattern.property1}_": b"PROPRE_ET_STABLE_X64",
    b"_{pattern.property2.property3.property4}_": b"PROPRE_ET_STABLE_X64. OK"
}

print("🚀 Launching NATIVE reading, replacement, and writing...")
start_ns = time.perf_counter_ns()

try:
    # Full read of the file on the disk
    with open(source_path, 'rb') as f:
        data = f.read()

    # Multi-pass replacement (The nightmare of allocating ~2.7 GB in RAM)
    for pattern, replacement in dictionary.items():
        data = data.replace(pattern, replacement)

    # Writing the final result onto the disk
    with open(target_path, 'wb') as f:
        f.write(data)

    end_ns = time.perf_counter_ns()
    elapsed_ms = (end_ns - start_ns) / 1_000_000
    print(f"[+] Elapsed time: {elapsed_ms:.2f} ms")

except MemoryError:
    print("\n💥 CRASH: Python exploded along the way with a 'MemoryError'.")

print("💡 TurboReplace Reminder: 3313.84 ms (Total stability)")
print("====================================================\n")
