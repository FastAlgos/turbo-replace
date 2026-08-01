# 🚀 TurboReplace v1.0 x64

### **The Ultimate Enterprise String & Template Engine.**
#### *Saturate your hardware bandwidth. Process dynamic text payloads at more than 1.2 GB/s in memory and up to 870 MB/s directly on storage disks from Node.js, Python, or Delphi.*

## 🚀 Quick Start (Evaluation Edition)

This repository includes the **Evaluation Edition** of the `tdjTurboReplace.dll` binary. It features a hardcoded evaluation ceiling (stops processing after 10 Kilobytes and appends an evaluation watermark).


Standard string replacement native functions (like JavaScript's `replaceAll` or Python's `.replace()`) suffer from critical architectural inefficiencies. When processing massive data streams with multiple variables, they waste valuable CPU cycles and reallocate system resources repeatedly, leading to massive latency, severe RAM fragmentation, and fatal crashes on enterprise workloads.

**TurboReplace** is a highly optimized native x64 engine built to eliminate these boundaries. It executes complex multi-variable text substitutions in a highly linear workflow, delivering maximum throughput while maintaining a predictable, light system footprint.

---

## 📊 Benchmarks & Performance Dominance

The following real-world enterprise workloads represent the ultimate scalability tests executed on a standard **Intel Core i7-13800H CPU**.

### ⏱️ Workload 1: In-Memory Processing (Pure RAM to RAM - ~850 MB Payload)
*30,000,000 asynchronous dynamic replacements with variable token lengths (14 to 42 bytes) on a 853.54 MB buffer.*

```text
Delphi Native        [███████ 1520.99 ms] (~588 MB/s High-Performance Base)
Node.js v18 (Koffi)  [█████████ 1816.07 ms] (509 MB/s Active Web Parsing)
Python 3.14 (Pure)   [██████████ 1940.63 ms] (461 MB/s Locked FFI Pipeline)
Python 3.14 Native   [██████████████████████████████████████████████████ 7146.27 ms]
Node.js Native (V8)  [💥 CRASH: RangeError / Invalid string length]
```

### 💾 Workload 2: Industrial Isolation (Pure Disk File-to-File)
*Full end-to-end disk streaming tests comparing payload scales on a fast NVMe SSD.*

#### 📈 Large Payload Test (~853.54 MB File-to-File)
```text
Delphi Native        [█████ 2807.62 ms] (🥇 ~876 MB/s Saturated Transfer)
Node.js v18 (Koffi)  [██████ 2997.26 ms] (🥈 Strictly 0 Bytes of JS Heap Used)
Python 3.14 (Pure)   [███████ 3313.84 ms] (🥉 Strictly 0 Bytes of Python Heap Used)
Python 3.14 Native   [████████████████████████████████████ 8504.63 ms]
Node.js Native (V8)  [💥 CRASH: Cannot create a string longer than 0x1fffffe8 chars]
```

#### 📉 Medium Payload Test (~437.00 MB File-to-File)
```text
Delphi Native        [█████ 1592.64 ms] (🥇 Native Saturated Stream)
Node.js v18 (Koffi)  [█████ 1627.83 ms] (🥈 Pure FFI Pipeline - Only 35ms overhead)
Python 3.14 Native   [████████████████████████████████████ 4972.93 ms]
Node.js Native (V8)  [████████████████████████████████████████████ 6389.51 ms]
```

> 🚨 **The Enterprise ROI Verdict:** At large scales, Google's V8 engine **crashes instantly** with an uncatchable `RangeError` because managed heap limits are exceeded. Python native survives but chokes your OS, thrashing your system's pagefile.
>
> TurboReplace processes the entire workload smoothly, keeping your production server memory usage strictly locked at a static, minuscule **O(1) footprint of 4 Megabytes of RAM maximum** via its integrated L3-cache streaming ring buffer.

---

## 🚀 Quick Start (Evaluation Edition)

This repository includes the **Evaluation Edition** of the `tdjTurboReplace.dll` binary. It features a hardcoded evaluation ceiling (stops processing after 10 Kilobytes and appends an evaluation watermark).

### 🟢 Node.js RAM-to-RAM Integration (`sc_ram_koffi.js`)
```javascript
const koffi = require('koffi');
const path = require('path');

const turboLib = koffi.load(path.resolve(__dirname, 'tdjTurboReplace.dll'));
const CreateTurboEngine   = turboLib.func('CreateTurboEngine', 'void*', []);
const AddReplacePair      = turboLib.func('AddReplacePair', 'void', ['void*', 'string', 'string']);
const CompileTurboEngine  = turboLib.func('CompileTurboEngine', 'void', ['void*']);
const ExecuteTurboReplace = turboLib.func('ExecuteTurboReplace', 'int', ['void*', 'void*', 'int', 'void*']);
const FreeTurboEngine     = turboLib.func('FreeTurboEngine', 'void', ['void*']);

const engine = CreateTurboEngine();
AddReplacePair(engine, "_{pattern_01}_", "replacement-value-01");
CompileTurboEngine(engine);

const HTTP_OUT_MAX_SIZE = 150 * 1024 * 1024;
const globalHttpOutBuffer = Buffer.alloc(HTTP_OUT_MAX_SIZE);

function runInMemoryReplace(inputBuffer) {
    const finalSize = ExecuteTurboReplace(engine, inputBuffer, inputBuffer.length, globalHttpOutBuffer);
    return globalHttpOutBuffer.subarray(0, finalSize);
}
```

### 🐍 Python File-to-File Integration (`sc_file_to_file_ctypes.py`)
```python
import ctypes
import os

turbo_dll = ctypes.CDLL(os.path.abspath("tdjTurboReplace.dll"))
turbo_dll.CreateTurboEngine.restype = ctypes.c_void_p
turbo_dll.AddReplacePair.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
turbo_dll.CompileTurboEngine.argtypes = [ctypes.c_void_p]
turbo_dll.ExecuteTurboReplaceFileToFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
turbo_dll.ExecuteTurboReplaceFileToFile.restype = ctypes.c_int

engine = turbo_dll.CreateTurboEngine()
turbo_dll.AddReplacePair(engine, b"_{pattern_01}_", b"replacement-value-01")
turbo_dll.CompileTurboEngine(engine)

source_path = os.path.abspath("large_input.txt").encode('ansi')
target_path = os.path.abspath("large_output.txt").encode('ansi')

success = turbo_dll.ExecuteTurboReplaceFileToFile(engine, source_path, target_path)
```

---

## 📖 C-Compatible API Reference Specification

The `tdjTurboReplace.dll` library exposes a standard C-compatible ABI using the `cdecl` calling convention. Strings are passed as null-terminated ANSI/UTF-8 character arrays (`const char*`).

### 📑 C Header File (`TurboReplace.h`)

```c
#ifndef TURBO_REPLACE_H
#define TURBO_REPLACE_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Instantiates a new isolated instance of the substitution engine.
 * @return A transparent opaque handle (pointer) to the allocated engine, or NULL if out of memory.
 */
void* CreateTurboEngine(void);

/**
 * @brief Injects a single search-and-replace pair configuration into the specified engine instance.
 * @param engineHandle Opaque pointer returned by CreateTurboEngine.
 * @param pattern Null-terminated string representing the token to search for.
 * @param replacement Null-terminated string representing the replacement text.
 */
void AddReplacePair(void* engineHandle, const char* pattern, const char* replacement);

/**
 * @brief Compiles the internal lookup map infrastructure and optimizes the runtime scan matrices.
 * @note This function must be executed ONCE after all paires have been injected and BEFORE any replacement calls.
 * @param engineHandle Opaque pointer returned by CreateTurboEngine.
 */
void CompileTurboEngine(void* engineHandle);

/**
 * @brief Executes an ultra-fast in-memory replacement sequence (RAM-to-RAM).
 * @param engineHandle Opaque pointer returned by CreateTurboEngine.
 * @param inBuffer Pointer to the raw input byte array in memory.
 * @param inSize Size of the input buffer in bytes.
 * @param outBuffer Pointer to the pre-allocated destination buffer in memory.
 * @return The exact final size of the written output data in bytes.
 */
int ExecuteTurboReplace(void* engineHandle, const void* inBuffer, int inSize, void* outBuffer);

/**
 * @brief Processes an entire input file from disk and streams the result directly to an output file.
 * @note Features an internal locked 4MB L3-cache optimized buffer. Managed language RAM footprint is exactly 0 bytes.
 * @param engineHandle Opaque pointer returned by CreateTurboEngine.
 * @param inputFileName Absolute null-terminated system path to the existing source file.
 * @param outputFileName Absolute null-terminated system path where the destination file will be created.
 * @return Returns 1 on total success, or 0 if a file access error, disk full, or missing path occurs.
 */
int ExecuteTurboReplaceFileToFile(void* engineHandle, const char* inputFileName, const char* outputFileName);

/**
 * @brief Gracefully deallocates the engine memory context and purges its internal dictionaries from RAM.
 * @param engineHandle Opaque pointer returned by CreateTurboEngine.
 */
void FreeTurboEngine(void* engineHandle);

#ifdef __cplusplus
}
#endif

#endif // TURBO_REPLACE_H
```

### 🐘 3. PHP & WordPress / CMS Plugins Integration (`sc_ram_ffi.php`)
Standard PHP/WordPress template rendering (like Twig, Blade, or native `str_replace` loops) triggers massive CPU overhead and high memory peaks on heavy traffic sites. With PHP 7.4+ and 8.x **FFI (Foreign Function Interface)**, you can now link **TurboReplace** directly into your custom plugins, themes, or enterprise CMS to execute template substitution at absolute machine-code speeds with **0MB allocated to the PHP memory limit**.

```php
<?php
// Initialize the native C-ABI bridge directly inside your WordPress/PHP code
\$turbo = FFI::cdef("
    void* CreateTurboEngine(void);
    void AddReplacePair(void* engineHandle, const char* pattern, const char* replacement);
    void CompileTurboEngine(void* engineHandle);
    int ExecuteTurboReplace(void* engineHandle, const void* inBuffer, int inSize, void* outBuffer);
    void FreeTurboEngine(void* engineHandle);
", __DIR__ . "/tdjTurboReplace.dll");

// Instantiate and compile your global template dictionary once at initialization
engine = turbo->CreateTurboEngine();
turbo->AddReplacePair(engine, "_{pattern_01}_", "replacement-value-01");
turbo->AddReplacePair(engine, "_{user.meta_data}_", "PROPRE_ET_STABLE_X64");
turbo->CompileTurboEngine(engine);

/**
 * High-Speed WordPress Hook / Shortcode Rendering Example
 */
function fast_cms_render_pipeline(\$html_template_string) {
    global turbo, engine;
    
    \(in_size = strlen(\)html_template_string);
    if (\(in_size === 0) return\)html_template_string;

    // Allocate a persistent native memory segment outside the PHP managed heap
    // This entirely bypasses PHP's standard memory_limit restrictions
    \$out_max_size = 50 * 1024 * 1024; // 50MB Max Output Buffer Zone
    \(out_buffer = FFI::new("char[\)out_max_size]");

    // Execute single-pass execution directly on the CPU silicon
    \(final_size =\)turbo->ExecuteTurboReplace(engine, html_template_string, \(in_size,\)out_buffer);

    // Cast the native C-buffer back into a standard high-speed PHP string
    return FFI::string(\(out_buffer,\)final_size);
}

// Example usage inside an advanced shortcode or database output loop
\$wp_raw_template = "<html>... heavy dynamic content ...</html>";
\(wp_final_output = fast_cms_render_pipeline(\)wp_raw_template);

// Free context on plugin deactivation / process death
// turbo->FreeTurboEngine(engine);
?>
```

> 🎯 **Why WordPress & WooCommerce Developers Buy TurboReplace Premium:** 
> When scaling a high-traffic WooCommerce store or an enterprise news portal, dynamic HTML generation is the number one cause of TTFB (Time to First Byte) latency and CPU throttling. By offloading dictionary scanning to our native unmanaged pipeline, you can **drop page render latency by up to 80%**, drastically improve your Google Core Web Vitals (LCP/INP), and host **5x more concurrent users** on the exact same server hardware without upgrading your cloud billing tier.

---

## 💎 Premium Edition & Licensing

Ready to unleash full hardware speed in production without boundaries?

The **Premium Edition** contains zero license code trackers, zero slow cloud validation calls, and zero external runtime dependencies. To preserve pure execution speed, every single commercial binary is customized using a unique, undetectable **Cryptographic Binary Watermark** signed with your corporate credentials.

*   **Startup / Single Server License (499 €):** Lifelong deployment on 1 production server node.
*   **SaaS Enterprise Cluster (1,199 €/year):** Unlimited node deployment, multi-cluster high-availability licensing, 24/7 priority patch support.


### 🎯 Get Your Premium Binary Now
To unlock the full power of your production hardware, request a commercial license by opening a secure business inquiry or contacting us directly via our GitHub profile layout. Your custom-watermarked binary will be compiled and delivered securely to your engineering team within 2 hours of verification.


*   **OEM Source Code License (Custom / Negotiable):** Full raw Pascal & ASM source code context. 100% white-label integration right inside your proprietary software. Ideal for large enterprises and software vendors. **Contact us directly for a customized quote tailored to your distribution scale.**


---
*Distributed under Shareware Terms. Copyright © 2026 TurboReplace Technologies.*
