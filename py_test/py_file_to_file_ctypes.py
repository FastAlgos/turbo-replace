import ctypes
import os
import time

# ==============================================================================
# 1. CONFIGURATION AND LOADING OF THE NATIVE DLL
# ==============================================================================

turbo_dll = ctypes.CDLL(os.path.abspath("tdjTurboReplace.dll"))
turbo_dll.CreateTurboEngine.restype = ctypes.c_void_p
turbo_dll.AddReplacePair.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
turbo_dll.CompileTurboEngine.argtypes = [ctypes.c_void_p]

# Prototype for direct file-to-file I/O
turbo_dll.ExecuteTurboReplaceFileToFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
turbo_dll.ExecuteTurboReplaceFileToFile.restype = ctypes.c_int


turbo_dll.FreeTurboEngine.argtypes = [ctypes.c_void_p]

engine = turbo_dll.CreateTurboEngine()
turbo_dll.AddReplacePair(engine, b"_{pattern_01}_", b"replacement-value-01")
turbo_dll.CompileTurboEngine(engine)

# Autonomous execution. Python reads zero bytes, the DLL directly handles the OS.
source_path = os.path.abspath("d:\\input.txt").encode('ansi')
target_path = os.path.abspath("d:\\py_output.txt").encode('ansi')

print("\n====================================================")
print("🚀 BENCHMARK: PYTHON 3.14.3 + DELPHI File to File 853.54 MB")
print("====================================================")

start_ns = time.perf_counter_ns()

success = turbo_dll.ExecuteTurboReplaceFileToFile(engine, source_path, target_path)

end_ns = time.perf_counter_ns()
elapsed_ns = end_ns - start_ns
elapsed_ms = elapsed_ns / 1_000_000

if success == 1: print("[+] File processed successfully!")

print(f"[+] Elapsed time    : {elapsed_ns} nanoseconds ({elapsed_ms:.2f} ms)")

turbo_dll.FreeTurboEngine(engine)
