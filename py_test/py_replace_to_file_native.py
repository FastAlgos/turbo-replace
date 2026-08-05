import time
import os

print("\n====================================================")
print("❌ BENCHMARK: NATIVE PYTHON TO FILE (WITHOUT YOUR DLL)")
print("====================================================")

# 1. Generation of the 850 MB buffer in RAM
base_chunk = b"<html>_{pattern_01}_ zone de texte _{pattern.property1}_ neutre HTML _{pattern.property2.property3.property4}_ de test _{pattern_01}_ end_{pattern.property1}_</html>_{pattern_01}_"
iterations = 5000000

print(f"[-] Preparing the test buffer of {len(base_chunk)*iterations/1024/1024:.2f} MB in RAM...")
input_test = base_chunk * iterations

dictionary = {
    b"_{pattern_01}_": b"replacement-1-0123456789",
    b"_{pattern.property1}_": b"PROPRE_ET_STABLE_X64",
    b"_{pattern.property2.property3.property4}_": b"PROPRE_ET_STABLE_X64. OK"
}

target_path = os.path.abspath("output_python_native.txt")

print("🚀 Launching NATIVE replacement and writing...")
start_ns = time.perf_counter_ns()

# Standard multi-pass processing of CPython
output_result = input_test
for pattern, replacement in dictionary.items():
    output_result = output_result.replace(pattern, replacement)

# Raw disk write via the OS
with open(target_path, 'wb') as f:
    f.write(output_result)

end_ns = time.perf_counter_ns()
elapsed_ms = (end_ns - start_ns) / 1_000_000

print(f"[*] Input size  : {len(input_test)} bytes")
print(f"[*] Output size : {len(output_result)} bytes")
print(f"[+] Elapsed time: {elapsed_ms:.2f} ms")
print("====================================================\n")
