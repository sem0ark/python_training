/// <reference lib="webworker" />
import { loadPyodide, type PyodideInterface } from "pyodide";
import type { RunRequest, RunResponse } from "./types";

let pyodideInstance: PyodideInterface | null = null;

async function getPyodide() {
  const baseUrl = import.meta.env.BASE_URL.endsWith("/")
    ? import.meta.env.BASE_URL
    : `${import.meta.env.BASE_URL}/`;
  pyodideInstance ??= await loadPyodide({
    indexURL: new URL(`${baseUrl}assets/`, self.location.origin).href,
  });
  return pyodideInstance;
}

self.onmessage = async ({ data }: MessageEvent<RunRequest>) => {
  const start = performance.now();
  try {
    const pyodide = await getPyodide();
    pyodide.globals.set("__user_code__", data.code);
    pyodide.globals.set("__user_stdin__", data.stdin ?? "");
    await pyodide.runPythonAsync(`
import io, sys
_stdout = io.StringIO()
_stderr = io.StringIO()
sys.stdin = io.StringIO(__user_stdin__)
sys.stdout = _stdout
sys.stderr = _stderr
try:
    exec(__user_code__, {"__name__": "__main__"})
finally:
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
`);
    self.postMessage({
      id: data.id,
      stdout: pyodide.runPython("_stdout.getvalue()"),
      stderr: pyodide.runPython("_stderr.getvalue()"),
      executionTimeMs: Math.round(performance.now() - start),
    } satisfies RunResponse);
  } catch (error) {
    self.postMessage({
      id: data.id,
      stdout: "",
      stderr: "",
      error: error instanceof Error ? error.message : String(error),
      executionTimeMs: Math.round(performance.now() - start),
    } satisfies RunResponse);
  }
};
