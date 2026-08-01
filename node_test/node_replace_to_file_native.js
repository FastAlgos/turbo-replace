const fs = require('fs');
const path = require('path');

console.log("\n====================================================");
console.log("❌ BENCHMARK: NATIVE NODE.JS TO FILE (WITHOUT YOUR DLL)");
console.log("====================================================");

// 1. Generation of the 850 MB buffer in RAM
const baseChunk = "<html>_{pattern_01}_ zone de texte _{pattern.property1}_ neutre HTML _{pattern.property2.property3.property4}_ de test _{pattern_01}_ end_{pattern.property1}_</html>_{pattern_01}_";
const iterations = 5000000;

console.log(`[-] Preparing the input buffer of ${(baseChunk.length*iterations/1024/1024).toFixed(2)} MB in RAM...`);
const inputTest = baseChunk.repeat(iterations);

const dictionary = {
    "_{pattern_01}_": "replacement-1-0123456789",
    "_{pattern.property1}_": "PROPRE_ET_STABLE_X64",
    "_{pattern.property2.property3.property4}_": "PROPRE_ET_STABLE_X64. OK"
};

const targetFile = path.resolve(__dirname, 'd:\\output_node_native.txt');

console.log("🚀 Launching NATIVE replacement and writing...");
const start = process.hrtime.bigint();

// Standard processing: chaining global replacements in V8 memory
let outputResult = inputTest;
for (const [pattern, replacement] of Object.entries(dictionary)) {
    const safePattern = pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    outputResult = outputResult.replaceAll(new RegExp(safePattern, 'g'), replacement);
}

// Synchronous disk write
fs.writeFileSync(targetFile, outputResult, 'utf-8');

const end = process.hrtime.bigint();
const elapsedMs = Number(end - start) / 1000000;

console.log(`[*] Input size  : ${inputTest.length} bytes`);
console.log(`[*] Output size : ${outputResult.length} bytes`);
console.log(`[+] Elapsed time: ${elapsedMs.toFixed(2)} ms`);
console.log("====================================================\n");
