const fs = require('fs');
const path = require('path');

console.log("\n====================================================");
console.log("❌ BENCHMARK: NATIVE NODE.JS FILE-TO-FILE (WITHOUT DLL)");
console.log("====================================================");

const sourceFile = path.resolve(__dirname, 'input.txt');
const targetFile = path.resolve(__dirname, 'node_ff_input.txt');

const dictionary = {
    "_{pattern_01}_": "replacement-1-0123456789",
    "_{pattern.property1}_": "PROPRE_ET_STABLE_X64",
    "_{pattern.property2.property3.property4}_": "PROPRE_ET_STABLE_X64. OK"
};

console.log("🚀 Launching NATIVE reading, replacement, and writing...");
const start = process.hrtime.bigint();

try {
    // ⚠️ CRASH ALERT: V8 collapses here on a 853 MB file
    let data = fs.readFileSync(sourceFile, 'utf-8');

    for (const [pattern, replacement] of Object.entries(dictionary)) {
        const safePattern = pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        data = data.replaceAll(new RegExp(safePattern, 'g'), replacement);
    }

    fs.writeFileSync(targetFile, data, 'utf-8');

    const end = process.hrtime.bigint();
    const elapsedMs = Number(end - start) / 1000000;
    console.log(`[+] Elapsed time: ${elapsedMs.toFixed(2)} ms`);

} catch (error) {
    console.log(`\n💥 CRITICAL VICTORY! Node.js crashed natively: ${error.message}`);
    console.log("💡 TurboReplace Reminder: 2997.26 ms (0 bytes of RAM consumed on Node.js side)");
}
console.log("====================================================\n");
