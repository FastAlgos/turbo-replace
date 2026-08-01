
const koffi = require('koffi');

// Direct loading of the DLL without compilation steps!
const turboLib = koffi.load('./tdjTurboReplace.dll');

const CreateTurboEngine   = turboLib.func('CreateTurboEngine', 'void*', []);
const AddReplacePair      = turboLib.func('AddReplacePair', 'void', ['void*', 'string', 'string']);
const CompileTurboEngine  = turboLib.func('CompileTurboEngine', 'void', ['void*']);
const ExecuteTurboReplace = turboLib.func('ExecuteTurboReplace', 'int', ['void*', 'void*', 'int', 'void*']);
const FreeTurboEngine     = turboLib.func('FreeTurboEngine', 'void', ['void*']);


/**
 * Executes industrial variable token replacement via the Delphi AVX2 DLL.
 * Leverages raw Node.js Buffers to saturate RAM bandwidth.
 */
function runTurboReplaceJS(inputBuffer, dictionary) {
    if (!inputBuffer || inputBuffer.length === 0 || !dictionary) {
        return inputBuffer;
    }

    // Instantiating the hidden engine inside the DLL
    //const engine = turboLib.CreateTurboEngine();
    // Direct instantiation of the function compiled by Koffi (without the turboLib prefix)
    const engine = CreateTurboEngine();

    // Direct validity check of the opaque pointer
    if (!engine) {
        throw new Error("Unable to instantiate the TurboEngine inside the DLL.");
    }


    try {
        // Injecting character string pairs
        // Node.js handles implicit conversion to PAnsiChar via ref.types.CString
        for (const [pattern, replacement] of Object.entries(dictionary)) {
            //turboLib.
            AddReplacePair(engine, pattern, replacement);
        }

        // Internal compilation of AVX2 and O(1) hashing
        //turboLib.
        CompileTurboEngine(engine);

        // Allocation of the output buffer (Input size + large safety margin)
        const inSize = inputBuffer.length;
        const outMaxSize = inSize + (32768 * 10000);
        const outBuffer = Buffer.alloc(outMaxSize);

        // EXECUTION AT THE SPEED OF SILICON
        const finalSize = //turboLib.
        ExecuteTurboReplace(engine, inputBuffer, inSize, outBuffer);

        // Returns the exact slice of the modified binary buffer
        return outBuffer.subarray(0, finalSize);

    } finally {
        // Mandatory memory release of the hidden Delphi object
        //turboLib.
        FreeTurboEngine(engine);
    }
}

// --- 🏎️ TEST SCENARIO AND BENCHMARK UNDER NODE.JS 18 ---
console.log("\n====================================================");
console.log("🚀 BENCHMARK: NODE.JS v18.15.0 + DELPHI AVX2 COUPLING");
console.log("====================================================");

// 1. Generation of a test structure of about 980 MB in RAM (V8 Engine)
const baseChunk = Buffer.from(
    "<html><html>_{pattern_01}_ zone de texte _{pattern.property1}_ neutre HTML _{pattern.property2.property3.property4}_ de test _{pattern_01}_ end_{pattern.property1}_</html>_{pattern_01}_", 
    'ascii'
);

const iterations = 5000000; // Adjust this value to test at 15 MB, 150 MB, or 850 MB
const buffersArray = new Array(iterations).fill(baseChunk);
const inputTest = Buffer.concat(buffersArray);

// 2. Configuration of the variable-length pattern dictionary
const dictionnaireConfig = {
    "_{pattern_01}_": "replacement-1-0123456789",
    "_{pattern.property1}_": "PROPRE_ET_STABLE_X64",
    "_{pattern.property2.property3.property4}_": "PROPRE_ET_STABLE_X64. OK"
};

// 3. High-precision time measurement from Node.js
const start = process.hrtime.bigint();

// Calling the native booster
const outputResult = runTurboReplaceJS(inputTest, dictionnaireConfig);

const end = process.hrtime.bigint();
const elapsedNs = Number(end - start);
const elapsedMs = elapsedNs / 1000000;

console.log(`[*] Input size  : ${inputTest.length} bytes (${(inputTest.length/1024/1024).toFixed(2)} MB)`);
console.log(`[*] Output size : ${outputResult.length} bytes (${(outputResult.length/1024/1024).toFixed(2)} MB)`);
console.log(`[+] Elapsed time: ${elapsedNs} nanoseconds (${elapsedMs.toFixed(2)} ms)`);
console.log("====================================================\n");
