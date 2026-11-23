import { describe, expect, it, vi } from "vitest";
import { loadPyodide } from "pyodide";
import { PythonRunner } from "./pythonRunner";

class FakeWorker {
  terminated = false;
  constructor(private readonly responds = true) {}
  private listener?: (event: MessageEvent) => void;
  addEventListener(_type: string, listener: (event: MessageEvent) => void) {
    this.listener = listener;
  }
  removeEventListener() {
    this.listener = undefined;
  }
  postMessage(payload: { id: string }) {
    if (!this.responds) return;
    setTimeout(() => {
      if (!this.terminated)
        this.listener?.({
          data: {
            id: payload.id,
            stdout: "hello\n",
            stderr: "",
            executionTimeMs: 1,
          },
        } as MessageEvent);
    }, 0);
  }
  terminate() {
    this.terminated = true;
  }
}

describe("PythonRunner", () => {
  it("can import the Pyodide runtime", () => {
    expect(loadPyodide).toBeTypeOf("function");
  });

  it("returns worker output", async () => {
    const runner = new PythonRunner(
      () => new FakeWorker() as unknown as Worker,
    );
    await expect(runner.run("print('hello')")).resolves.toMatchObject({
      stdout: "hello\n",
    });
  });

  it("ignores responses belonging to another request", async () => {
    class NoisyWorker extends FakeWorker {
      override postMessage(payload: { id: string }) {
        setTimeout(
          () =>
            this.listenerForTest?.({
              data: {
                id: "other-request",
                stdout: "wrong",
                stderr: "",
                executionTimeMs: 1,
              },
            } as MessageEvent),
          0,
        );
        super.postMessage(payload);
      }
      listenerForTest?: (event: MessageEvent) => void;
      override addEventListener(
        _type: string,
        listener: (event: MessageEvent) => void,
      ) {
        this.listenerForTest = listener;
        super.addEventListener(_type, listener);
      }
    }
    const runner = new PythonRunner(
      () => new NoisyWorker() as unknown as Worker,
    );
    await expect(runner.run("print('hello')")).resolves.toMatchObject({
      stdout: "hello\n",
    });
  });

  it("terminates and replaces a worker on timeout", async () => {
    vi.useFakeTimers();
    const workers: FakeWorker[] = [];
    const runner = new PythonRunner(() => {
      const worker = new FakeWorker(workers.length > 0);
      workers.push(worker);
      return worker as unknown as Worker;
    });
    const result = runner.run("while True: pass", "", 100);
    vi.advanceTimersByTime(100);
    await expect(result).resolves.toMatchObject({
      error: "Time Limit Exceeded (100ms)",
    });
    expect(workers[0].terminated).toBe(true);
    expect(workers).toHaveLength(2);
    vi.useRealTimers();
  });
});
