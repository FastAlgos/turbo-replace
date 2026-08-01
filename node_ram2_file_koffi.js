const koffi = require('koffi');
const path = require('path');

// 1. Secure loading of the native x64 DLL
const dllPath = path.resolve(__dirname, 'tdjTurboReplace.dll');
const turboLib = koffi.load(dllPath);

// 2. Declaration of Koffi function signatures
const CreateTurboEngine         = turboLib.func('CreateTurboEngine', 'void*', []);
const AddReplacePair            = turboLib.func('AddReplacePair', 'void', ['void*', 'string', 'string']);
const CompileTurboEngine        = turboLib.func('CompileTurboEngine', 'void', ['void*']);
const ExecuteTurboReplaceToFile = turboLib.func('ExecuteTurboReplaceToFile', 'int', ['void*', 'void*', 'int', 'string']);
const FreeTurboEngine           = turboLib.func('FreeTurboEngine', 'void', ['void*']);

/**
 * Reads an input buffer and writes the result directly to a physical file via the DLL's RAM buffer.
 */
function turboReplaceToFileJS(inputBuffer, dictionary, outputFilePath) {
    if (!inputBuffer || inputBuffer.length === 0 || !dictionary || !outputFilePath) {
        return false;
    }

    // Instantiating the hidden dictionary object inside the DLL
    const engine = CreateTurboEngine();
    if (!engine) {
        throw new Error("Unable to instantiate the TurboEngine inside the DLL.");
    }

    try {
        // Injecting string pairs
        for (const [pattern, replacement] of Object.entries(dictionary)) {
            AddReplacePair(engine, pattern, replacement);
        }

        // Internal compilation of AVX2 and the 4096 hash table
        CompileTurboEngine(engine);

        const inSize = inputBuffer.length;
        
        // DIRECT CALL OF THE BOOSTER IN A SINGLE PASS TO DISK
        const success = ExecuteTurboReplaceToFile(engine, inputBuffer, inSize, outputFilePath);
        
        return success === 1;

    //} tragedy_protect_finally { // Simply becomes:
    } finally {
        // Mandatory memory release of the hidden Delphi object
        FreeTurboEngine(engine);
    }
}


// --- 🏎️ NODE.JS TEST SCENARIO AND BENCHMARK ---
if (require.main === module) {
    console.log("\n====================================================");
    console.log("🚀 BENCHMARK: NODE.JS v26 + PURE AVX2 TO FILE VIA KOFFI");
    console.log("====================================================");

    // Generation of a test source file in RAM of about 850 MB
    const baseChunk = Buffer.from(
        "<html>_{pattern_01}_ zone de texte _{pattern.property1}_ neutre HTML _{pattern.property2.property3.property4}_ de test _{pattern_01}_ end_{pattern.property1}_</html>_{pattern_01}_", 
        'ascii'
    );
    const iterations = 5000000; 
    console.log(`[-] Preparing the input buffer of ${(baseChunk.length*iterations/1024/1024).toFixed(2)} MB in RAM...`);
    const buffersArray = new Array(iterations).fill(baseChunk);
    const inputTest = Buffer.concat(buffersArray);

    const dictionnaireConfig = {
        "_{pattern_01}_": "replacement-1-0123456789",
        "_{pattern.property1}_": "PROPRE_ET_STABLE_X64",
        "_{pattern.property2.property3.property4}_": "PROPRE_ET_STABLE_X64. OK"
    };

    const targetFile = path.resolve(__dirname, 'd:\\replacements_node.txt');

    console.log("🚀 Launching single scan and buffered sequential write...");
    const start = process.hrtime.bigint();

    const isOk = turboReplaceToFileJS(inputTest, dictionnaireConfig, targetFile);

    const end = process.hrtime.bigint();
    const elapsedMs = Number(end - start) / 1000000;

    if (isOk) {
        console.log(`[+] Total success! The file was written in: ${elapsedMs.toFixed(2)} ms`);
        console.log(`[*] Generated file: ${targetFile}`);
    } else {
        console.log("❌ Critical error during native execution.");
    }
    console.log("====================================================\n");
}
