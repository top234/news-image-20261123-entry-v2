import { spawnSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.OUTPUT_DIR ?? process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outPath = join(outDir, "entry.png");
const bundled = join(here, "entry.png");

function sha256(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function verify(path: string): void {
  const buf = readFileSync(path);
  const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (!buf.subarray(0, 8).equals(pngSig)) throw new Error("not a PNG");
  const w = buf.readUInt32BE(16);
  const h = buf.readUInt32BE(20);
  if (w !== 1024 || h !== 1024) throw new Error(`bad size ${w}x${h}, want 1024x1024`);
  if (buf.length > 1048576) throw new Error(`too big: ${buf.length} bytes`);
}

function renderWithPython(): boolean {
  for (const py of ["python3", "python"]) {
    const r = spawnSync(py, [join(here, "generate.py")], {
      env: { ...process.env, OUTPUT_DIR: outDir },
      stdio: "pipe",
    });
    if (r.error && (r.error as NodeJS.ErrnoException).code === "ENOENT") continue;
    if (r.status === 0 && existsSync(outPath)) return true;
    const err = (r.stderr?.toString() ?? "").trim() || r.error?.message || "unknown";
    process.stderr.write(`generate.py via ${py} failed: ${err}\n`);
    return false;
  }
  return false;
}

mkdirSync(outDir, { recursive: true });
let ok = false;
let renderError = "";
try {
  ok = renderWithPython();
  if (ok) verify(outPath);
} catch (e) {
  renderError = (e as Error).message;
  process.stderr.write(`render failed (${renderError}); using bundled entry.png\n`);
  ok = false;
}
if (!ok) {
  if (!existsSync(bundled)) {
    throw new Error(`render failed (${renderError || "no Python/PIL"}) and no bundled entry.png`);
  }
  // Verify the bundled copy BEFORE it replaces anything in the output dir,
  // so a corrupt bundle can never silently clobber a previous render.
  verify(bundled);
  copyFileSync(bundled, outPath);
  verify(outPath);
}
const size = statSync(outPath).size;
console.log(`entry.png ${size} bytes sha256=${sha256(outPath)}`);
