const koffi = require('koffi');
const path = require('path');

const turboLib = koffi.load(path.resolve(__dirname, 'tdjTurboReplace.dll'));
const CreateTurboEngine             = turboLib.func('CreateTurboEngine', 'void*', []);
const AddReplacePair                = turboLib.func('AddReplacePair', 'void', ['void*', 'string', 'string']);
const CompileTurboEngine            = turboLib.func('CompileTurboEngine', 'void', ['void*']);
const ExecuteTurboReplaceFileToFile = turboLib.func('ExecuteTurboReplaceFileToFile', 'int', ['void*', 'string', 'string']);
const FreeTurboEngine               = turboLib.func('FreeTurboEngine', 'void', ['void*']);

const engine = CreateTurboEngine();
AddReplacePair(engine, "_{pattern_01}_", "replacement-1-0123456789");
AddReplacePair(engine, "_{pattern.property1}_", "PROPRE_ET_STABLE_X64");
AddReplacePair(engine, "_{pattern.property2.property3.property4}_", "PROPRE_ET_STABLE_X64. OK");
CompileTurboEngine(engine);

// Direct Disk-to-Disk streaming. Node.js RAM consumption = 0 bytes.
const sourceFile = path.resolve(__dirname, 'input500.txt');
const targetFile = path.resolve(__dirname, 'node_output.txt');


console.log("\n====================================================");
console.log("🚀 BENCHMARK: NODE.JS v18.15.0 + DELPHI FILE2FILE");
console.log("====================================================");

const start = process.hrtime.bigint();
const success = ExecuteTurboReplaceFileToFile(engine, sourceFile, targetFile);

const end = process.hrtime.bigint();
const elapsedNs = Number(end - start);
const elapsedMs = elapsedNs / 1000000;

if (success === 1) console.log("[+] File processed successfully!");

console.log(`[+] Elapsed time    : ${elapsedNs} nanoseconds (${elapsedMs.toFixed(2)} ms)`);
console.log("====================================================\n");

FreeTurboEngine(engine);
