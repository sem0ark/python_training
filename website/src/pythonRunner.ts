import type { RunRequest, RunResponse } from "./types";

export type WorkerFactory = () => Worker;

export class PythonRunner {
  private worker: Worker;
  private readonly createWorker: WorkerFactory;

  constructor(
    createWorker: WorkerFactory = () =>
      new Worker(new URL("./pyodide.worker.ts", import.meta.url), {
        type: "module",
      }),
  ) {
    this.createWorker = createWorker;
    this.worker = createWorker();
  }

  run(code: string, stdin = "", timeoutMs = 3000): Promise<RunResponse> {
    return new Promise((resolve) => {
      const id = crypto.randomUUID();
      const start = performance.now();
      const timer = setTimeout(() => {
        this.worker.terminate();
        this.worker = this.createWorker();
        resolve({
          id,
          stdout: "",
          stderr: "",
          error: `Time Limit Exceeded (${timeoutMs}ms)`,
          executionTimeMs: Math.round(performance.now() - start),
        });
      }, timeoutMs);
      const handleMessage = (event: MessageEvent<RunResponse>) => {
        if (event.data.id !== id) return;
        clearTimeout(timer);
        this.worker.removeEventListener("message", handleMessage);
        resolve(event.data);
      };
      this.worker.addEventListener("message", handleMessage);
      const payload: RunRequest = { id, code, stdin };
      this.worker.postMessage(payload);
    });
  }
}
