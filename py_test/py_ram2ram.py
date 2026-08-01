import ctypes
import os
import time

# ==============================================================================
# 1. CONFIGURATION AND LOADING OF THE NATIVE DLL
# ==============================================================================

dll_name = "tdjTurboReplace.dll"
dll_path = os.path.abspath(dll_name)

if not os.path.exists(dll_path):
    raise FileNotFoundError(f"[-] Error: DLL not found at path: {dll_path}")

turbo_dll = ctypes.CDLL(dll_path)

# Declaration of C-Compatible native API signatures
turbo_dll.CreateTurboEngine.restype = ctypes.c_void_p
turbo_dll.AddReplacePair.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
turbo_dll.CompileTurboEngine.argtypes = [ctypes.c_void_p]
turbo_dll.ExecuteTurboReplace.argtypes = [
    ctypes.c_void_p,  # EngineHandle
    ctypes.c_void_p,  # InBuffer (PByte)
    ctypes.c_int,     # InSize
    ctypes.c_void_p   # OutBuffer (PByte)
]
turbo_dll.ExecuteTurboReplace.restype = ctypes.c_int
turbo_dll.FreeTurboEngine.argtypes = [ctypes.c_void_p]

# ==============================================================================
# 2. ONE-TIME INFRASTRUCTURE INITIALIZATION (OUTSIDE TIMED ZONE)
# ==============================================================================
print("[-] Initializing TurboReplace infrastructure...")

# A. One-time instantiation of the hidden dictionary inside the DLL
engine_handle = turbo_dll.CreateTurboEngine()
if not engine_handle:
    raise MemoryError("Unable to instantiate the engine inside the DLL.")

# B. Definition and one-time injection of the variable pattern dictionary
dictionnaire_config = {
    "_{pattern_01}_": "replacement-1-0123456789",
    "_{pattern.property1}_": "PROPRE_ET_STABLE_X64",
    "_{pattern.property2.property3.property4}_": "PROPRE_ET_STABLE_X64. OK"
}

# Retention list to prevent the Garbage Collector from freeing the string memory
protected_refs = []
for pattern, replacement in dictionnaire_config.items():
    pat_bytes = pattern.encode('ansi')
    repl_bytes = replacement.encode('ansi')
    protected_refs.append((pat_bytes, repl_bytes))
    turbo_dll.AddReplacePair(engine_handle, pat_bytes, repl_bytes)

# C. One-time compilation of hash structures and AVX2 inside the DLL
turbo_dll.CompileTurboEngine(engine_handle)

# D. ONE-TIME SAFETY ALLOCATION OF THE GLOBAL OUTPUT BUFFER (PERSISTENT)
# We allocate 1000 MB once and for all. The cost of zeroing out memory is cleared here!
OUT_MAX_SIZE = 1000*1024*1024 #950000 1000 * 1024 * 1024 
print(f"[-] Pre-allocating persistent output buffer ({OUT_MAX_SIZE / 1024 / 1024:.2f} MB)...")
global_out_buffer = ctypes.create_string_buffer(OUT_MAX_SIZE)

print("[+] Infrastructure ready. Launching benchmark...")

# ==============================================================================
# 3. HIGH-PERFORMANCE CRITICAL ROUTINE (ZERO ALLOCATION)
# ==============================================================================
def run_compiled_replace_pure(input_data: bytes) -> bytes:
    """
    Executes vectorized replacement in ultra-fast mode.
    Zero buffer allocation on each run. Guaranteed native Delphi speed.
    """
    in_size = len(input_data)
    if in_size == 0:
        return input_data

    # Instant extraction of the physical pointer address without any copy operation
    in_ptr = ctypes.cast(ctypes.c_char_p(input_data), ctypes.c_void_p).value
    
    # DIRECT BEELINE CALL TO DELPHI ASSEMBLY
    final_size = turbo_dll.ExecuteTurboReplace(engine_handle, in_ptr, in_size, global_out_buffer)
    
    # Extracting the modified memory slice as a view (Memoryview / Slicing)
    return global_out_buffer.raw[:final_size]

# ==============================================================================
# 4. EXECUTION AND BENCHMARK ON REAL PAYLOAD
# ==============================================================================
if __name__ == "__main__":
    # Generation of the same test source file in RAM of about 850 MB
    base_chunk = b"<html>_{pattern_01}_ zone de texte _{pattern.property1}_ neutre HTML _{pattern.property2.property3.property4}_ de test _{pattern_01}_ end_{pattern.property1}_</html>_{pattern_01}_"
    iterations = 5000000
    
    print(f"[-] Preparing the test buffer of {len(base_chunk)*iterations/1024/1024:.2f} MB in RAM...")
    input_test = base_chunk * iterations
    
    print("\n====================================================")
    print("🚀 BENCHMARK: PYTHON 3.14.3 + PURE AVX2 NO-ALLOC COUPLING")
    print("====================================================")
    
    # High-precision time capture
    start_ns = time.perf_counter_ns()
    
    # Calling the critical loop freed from ctypes overhead
    output_result = run_compiled_replace_pure(input_test)
    
    end_ns = time.perf_counter_ns()
    
    # Final metrics
    elapsed_ns = end_ns - start_ns
    elapsed_ms = elapsed_ns / 1_000_000
    
    print(f"[*] Input size  : {len(input_test)} bytes ({len(input_test)/1024/1024:.2f} MB)")
    print(f"[*] Output size : {len(output_result)} bytes ({len(output_result)/1024/1024:.2f} MB)")
    print(f"[+] Elapsed time: {elapsed_ns} nanoseconds ({elapsed_ms:.2f} ms)")
    print("====================================================\n")

    # Clean cleanup when shutting down the program
    turbo_dll.FreeTurboEngine(engine_handle)
