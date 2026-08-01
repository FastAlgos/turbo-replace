const time = require('process').hrtime;


// 1. Generation of the same 980 MB buffer as your test
const baseChunk = "<html><html>_{pattern_01}_ zone de texte _{pattern.property1}_ neutre HTML _{pattern.property2.property3.property4}_ de test _{pattern_01}_ end_{pattern.property1}_</html>_{pattern_01}_";
const iterations = 5000000;

console.log(`[-] Preparing the file of ${((baseChunk.length*iterations)/1024/1024).toFixed(2)} MB in RAM...`);
let inputTest = baseChunk.repeat(iterations);

const dictionary = {
    "_{pattern_01}_": "replacement-1-0123456789",
    "_{pattern.property1}_": "PROPRE_ET_STABLE_X64",
    "_{pattern.property2.property3.property4}_": "PROPRE_ET_STABLE_X64. OK"
};

console.log("🚀 Launching replacement NATIVELY under Node.js...");
const start = process.hrtime.bigint();

// Standard native method: Chaining global regular expressions
// Forces the V8 engine to reallocate memory 3 consecutive times for the full payload!
let outputResult = inputTest;
for (const [pattern, replacement] of Object.entries(dictionary)) {
    // Escaping special characters for the RegEx
    const safePattern = pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    outputResult = outputResult.replaceAll(new RegExp(safePattern, 'g'), replacement);
}

const end = process.hrtime.bigint();
const elapsedMs = Number(end - start) / 1000000;

console.log("====================================================");
console.log("❌ NATIVE NODE.JS RESULT (WITHOUT YOUR DLL)");
console.log("====================================================");
console.log(`[*] Input size   : ${inputTest.length} bytes`);
console.log(`[*] Output size  : ${outputResult.length} bytes`);
console.log(`[+] Elapsed time : ${elapsedMs.toFixed(2)} ms`);
console.log(`💡 TurboReplace Reminder: ~448.23 ms (Node v26.5)`);
console.log("====================================================\n");
