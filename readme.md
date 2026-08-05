# ⚡ tdjTurboReplace DLL v1.0

### **The Fastest Multi-Pattern Template & String Engine on Earth.**
#### *Saturate your hardware. Process nearly 1 Gigabyte of dense dynamic templates under 2 seconds from Node.js, Python, or Delphi.*

Standard string replacement engines (like JavaScript's `replaceAll` or Python's `.replace()`) suffer from a fatal structural flaw: **Multi-Pass Immutability**. When replacing multiple variables, they rescan and reallocate the entire payload in RAM *for every single pattern*, causing massive latency, CPU cache thrashing, and fatal crashes on large workloads.

**TurboReplace** bypasses the managed heap completely. Written in an ultra-optimized hybrid architecture—combining high-speed cache-aligned scanning with raw assembly vector operations (**SIMD Intel/AMD AVX2**) and an explicit 4MB dynamic L3-cache buffer—it parses and outputs data in a **single linear pass (O(N))** at the physical limit of your hardware.

---

### 💎 Key Engineering Achievements
* **Advanced Multi-Pattern Indexing**: Eliminates traditional nested loops for length scanning. Search time remains constant regardless of the configuration size.
* **Hardware-Level Register Routing**: 8-byte target patterns are matched instantly inside raw CPU registers to minimize memory-to-memory call latencies.
* **Vectorized Skip Path**: Integrates a highly optimized SIMD scanning layer to fly over non-matching data chunks at maximum clock frequency.
* **Zero-Allocation Memory Pipeline**: Executes entirely inside isolated, contiguous linear buffers. Zero garbage collection, zero heap overhead.

---

### 🛑 Evaluation vs Premium Mode
The Free Evaluation DLL has **no file size restrictions**, **no time limits**, and **no throughput throttling**. You can benchmark its extreme raw speed on multi-gigabyte production files instantly.

⚠️ **Important Limitation:** In Evaluation Mode, the actual replacement text you provide is completely bypassed and destroyed at memory-level. It is replaced cyclically by our 64-character signature string while strictly preserving your requested replacement length:
`FastAlgos/turbo-replace # THANK YOU FOR TEST # EVALUATION COPY #`

*Example: If your replacement string length is 5 characters, it will output `FastA`. If it is 20 characters, it will output `FastAlgos/turbo-repl`.*

Purchase a Premium License to unlock genuine data replacement in production.

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
$turbo = FFI::cdef("
    void* CreateTurboEngine(void);
    void AddReplacePair(void* engineHandle, const char* pattern, const char* replacement);
    void CompileTurboEngine(void* engineHandle);
    int ExecuteTurboReplace(void* engineHandle, const void* inBuffer, int inSize, void* outBuffer);
    void FreeTurboEngine(void* engineHandle);
", __DIR__ . "/tdjTurboReplace.dll");

// Instantiate and compile your global template dictionary once at initialization
$engine = $turbo->CreateTurboEngine();
$turbo->AddReplacePair($engine, "_{pattern_01}_", "replacement-value-01");
$turbo->AddReplacePair($engine, "_{user.meta_data}_", "PROPRE_ET_STABLE_X64");
$turbo->CompileTurboEngine($engine);

/**
 * High-Speed WordPress Hook / Shortcode Rendering Example
 */
function fast_cms_render_pipeline($html_template_string) {
    global $turbo, $engine;
    
    $in_size = strlen($html_template_string);
    if ($in_size === 0) return $html_template_string;

    // Allocate a persistent native memory segment outside the PHP managed heap
    // This entirely bypasses PHP's standard memory_limit restrictions
    $out_max_size = 50 * 1024 * 1024; // 50MB Max Output Buffer Zone
    $out_buffer = FFI::new("char[$out_max_size]");

    // Execute single-pass execution directly on the CPU silicon
    $final_size = $turbo->ExecuteTurboReplace($engine, $html_template_string, $in_size, $out_buffer);

    // Cast the native C-buffer back into a standard high-speed PHP string
    return FFI::string($out_buffer, $final_size);
}

// Example usage inside an advanced shortcode or database output loop
$wp_raw_template = "<html>... heavy dynamic content ...</html>";
$wp_final_output = fast_cms_render_pipeline($wp_raw_template);

// Free context on plugin deactivation / process death
// $turbo->FreeTurboEngine($engine);
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


### 🎯 Get Your Premium Binary Now. Choose Your Production License

| License Tier | Price | Deliverable | Ideal For |
| :--- | :--- | :--- | :--- |
| **Developer / Indie** | **149 €** | Custom Signed Binary | Local workstation usage & prototyping. |
| **Single Server Node** | **499 €** | Custom Signed Binary | 1 Live Production Server or SaaS node (Lifetime). |
| **Enterprise SaaS Cluster** | **1,199 €/yr**| Custom Signed Binary | Unlimited nodes, High-Availability clusters, 24/7 patches. |

### 🎯 Get Your Premium Binary Now. Choose Your Production License

| License Tier | Price | Deliverable | Ideal For |
| :--- | :--- | :--- | :--- |
| **Student / Academic** | **Just buy me a coffee 🎓** | Custom Signed Binary | Academic research, non-commercial university projects. |
| **Developer / Indie** | **149 €** | Custom Signed Binary | Local workstation usage & prototyping. |
| **Single Server Node** | **499 €** | Custom Signed Binary | 1 Live Production Server or SaaS node (Lifetime). |
| **Enterprise SaaS Cluster** | **1,199 €/yr**| Custom Signed Binary | Unlimited nodes, High-Availability clusters, 24/7 patches. |

> 🔒 **Pure Speed Guarantee**: Every single commercial binary is built without cloud license trackers, zero slow validation network calls, and zero external runtimes.

👉 **Are you a student or researcher?** We believe in accessible engineering. [Just buy me a coffee](https://fastalgos.net) to support the project! 

⚠️ **How to get your binary:** Make your donation, leave a friendly message with your **academic/university email address**, and we will compile, watermark, and email your custom Premium binary directly to you.

👉 **Ready to unlock commercial/production mode?** [Buy instantly](https://fastalgos.net) and receive your binary automatically within 5 minutes.

---

---

## ⚖️ Legal Policies & Compliance

### 🔒 Privacy Notice
FastAlgos is committed to security and user privacy. Our pre-compiled native software binaries run 100% autonomously on your local infrastructure. Our tools collect strictly zero user data, contain no telemetry or analytics tracking, and establish no external internet socket connections. 

### 📜 Terms of Service
By purchasing a license for FastAlgos Turbo-Replace, you are granted a non-exclusive, non-transferable right to execute the provided binary within your specified deployment tier. Reverse-engineering, decompiling, or modifying the watermarked machine code is strictly prohibited.

### 💳 Refund Policy
Due to the digital distribution nature of pre-compiled native binaries and custom cryptographic watermarking, all sales are final and non-refundable once the signed library files have been built and delivered to your team.


---
*Distributed under Shareware Terms. Copyright © 2026 TurboReplace Technologies.*
