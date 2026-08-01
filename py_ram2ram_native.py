import time

base_chunk = b"<html>_{pattern_01}_ zone de texte _{pattern.property1}_ neutre HTML _{pattern.property2.property3.property4}_ de test _{pattern_01}_ end_{pattern.property1}_</html>_{pattern_01}_"
iterations = 5000000     

input_test = base_chunk * iterations

print(f"[-] Generation of the {(len(input_test)/1024/1024):.2f} MB buffer in RAM...")

dictionary = {
    b"_{pattern_01}_": b"replacement-1-0123456789",
    b"_{pattern.property1}_": b"PROPRE_ET_STABLE_X64",
    b"_{pattern.property2.property3.property4}_": b"PROPRE_ET_STABLE_X64. OK"
}

print("🚀 Launching replacement NATIVELY in Python 3.14...")
start_ns = time.perf_counter_ns()

# Native method: Each loop copies the full payload to another RAM location
output_result = input_test
for pattern, replacement in dictionary.items():
    output_result = output_result.replace(pattern, replacement)

end_ns = time.perf_counter_ns()
elapsed_ms = (end_ns - start_ns) / 1_000_000

#print(output_result);

print("====================================================")
print("❌ NATIVE PYTHON RESULT (WITHOUT YOUR DLL)")
print("====================================================")
print(f"[*] Input size   : {len(input_test)} bytes")
print(f"[*] Output size  : {len(output_result)} bytes")
print(f"[+] Elapsed time : {elapsed_ms:.2f} ms")
#print(f"💡 TurboReplace Reminder: ~570.34 ms (Python 3.14)")
print("====================================================\n")
