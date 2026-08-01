import ctypes
import os
import time

# 1. Secure loading of the native x64 DLL
dll_path = os.path.abspath("tdjTurboReplace.dll")
turbo_dll = ctypes.CDLL(dll_path)

# 2. Configuration of C-Compatible native API signatures
turbo_dll.CreateTurboEngine.restype = ctypes.c_void_p
turbo_dll.AddReplacePair.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
turbo_dll.CompileTurboEngine.argtypes = [ctypes.c_void_p]

# Strict specification of types for file writing
turbo_dll.ExecuteTurboReplaceToFile.argtypes = [
    ctypes.c_void_p,  # EngineHandle
    ctypes.c_void_p,  # InBuffer (PByte)
    ctypes.c_int,     # InSize
    ctypes.c_char_p   # AOutputFileName (PAnsiChar)
]
turbo_dll.ExecuteTurboReplaceToFile.restype = ctypes.c_int # Returns 1 or 0

turbo_dll.FreeTurboEngine.argtypes = [ctypes.c_void_p]


def turbo_replace_to_file_python(input_data: bytes, dictionary: dict[str, str], output_file_path: str) -> bool:
    """
    Executes vectorized replacement and writes directly onto the disk.
    Python RAM consumption = 0 bytes for the output payload.
    """
    if not input_data or not dictionary or not output_file_path:
        return False

    # Instantiating the hidden engine object inside the DLL
    engine = turbo_dll.CreateTurboEngine()
    if not engine:
        raise MemoryError("Unable to instantiate the engine inside the DLL.")
    
    try:
        # Encoding and single injection of string pairs
        protected_refs = []
        for pattern, replacement in dictionary.items():
            pat_bytes = pattern.encode('ansi')
            repl_bytes = replacement.encode('ansi')
            protected_refs.append((pat_bytes, repl_bytes)) # GC protection
            
            turbo_dll.AddReplacePair(engine, pat_bytes, repl_bytes)
            
        # Internal compilation of the 4096 hash table and AVX2
        turbo_dll.CompileTurboEngine(engine)
        
        # Extraction of the physical memory address from the input buffer
        in_size = len(input_data)
        in_ptr = ctypes.cast(ctypes.c_char_p(input_data), ctypes.c_void_p).value
        
        # Encoding the target file path to PAnsiChar
        path_bytes = output_file_path.encode('ansi')
        
        # SINGLE DIRECT CALL WITHOUT ANY OUTPUT ALLOCATION
        success = turbo_dll.ExecuteTurboReplaceToFile(engine, in_ptr, in_size, path_bytes)
        
        return success == 1
        
    finally:
        # Mandatory memory release of the hidden Delphi object
        turbo_dll.FreeTurboEngine(engine)


# --- 🏎️ TEST CASE AND BENCHMARK IN PYTHON 3.14 ---
if __name__ == "__main__":
    print("\n====================================================")
    print("🚀 BENCHMARK: PYTHON 3.14.3 + DLL TO FILE")
    print("====================================================")
    
    # Generation of a test source file in RAM of about 850 MB
    base_chunk = b"<html>_{pattern_01}_ zone de texte _{pattern.property1}_ neutre HTML _{pattern.property2.property3.property4}_ de test _{pattern_01}_ end_{pattern.property1}_</html>_{pattern_01}_"
    iterations = 5000000
    
    print(f"[-] Preparing the test buffer of {len(base_chunk)*iterations/1024/1024:.2f} MB in RAM...")
    input_test = base_chunk * iterations
    
    dictionnaire_config = {
        "_{pattern_01}_": "replacement-1-0123456789",
        "_{pattern.property1}_": "PROPRE_ET_STABLE_X64",
        "_{pattern.property2.property3.property4}_": "PROPRE_ET_STABLE_X64. OK"
    }
    
    target_path = os.path.abspath("d:\\replacements_py.txt")
    
    print("🚀 Launching single scan and buffered sequential write...")
    start_time = time.perf_counter_ns()
    
    success_flag = turbo_replace_to_file_python(input_test, dictionnaire_config, target_path)
    
    end_time = time.perf_counter_ns()
    elapsed_ms = (end_time - start_time) / 1_000_000
    
    if success_flag:
        print(f"[+] Total success! The file was written in: {elapsed_ms:.2f} ms")
        print(f"[*] Generated file: {target_path}")
    else:
        print("❌ Error during direct writing by the DLL.")
    print("====================================================\n")
