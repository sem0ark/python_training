import { describe, expect, it, vi } from "vitest";
import { runTestCases } from "./judge";

describe("runTestCases", () => {
  it("returns no results for an empty test suite", async () => {
    const runner = { run: vi.fn() };
    await expect(runTestCases(runner as never, "code", [])).resolves.toEqual(
      [],
    );
    expect(runner.run).not.toHaveBeenCalled();
  });

  it("runs cases in order and marks matching output as passed", async () => {
    const runner = {
      run: vi
        .fn()
        .mockResolvedValueOnce({
          stdout: "first\n",
          stderr: "",
          executionTimeMs: 2,
        })
        .mockResolvedValueOnce({
          stdout: "wrong\n",
          stderr: "",
          executionTimeMs: 3,
        }),
    };
    const cases = [
      { input: "a", expected: "first" },
      { input: "b", expected: "expected" },
    ];

    await expect(
      runTestCases(runner as never, "code", cases, 50),
    ).resolves.toEqual([
      {
        input: "a",
        expected: "first",
        actual: "first",
        passed: true,
        executionTimeMs: 2,
      },
      {
        input: "b",
        expected: "expected",
        actual: "wrong",
        passed: false,
        executionTimeMs: 3,
      },
    ]);
    expect(runner.run).toHaveBeenNthCalledWith(1, "code", "a", 50);
    expect(runner.run).toHaveBeenNthCalledWith(2, "code", "b", 50);
  });

  it("returns Python errors and stderr as failed results", async () => {
    const runner = {
      run: vi
        .fn()
        .mockResolvedValueOnce({
          stdout: "",
          stderr: "traceback",
          error: "SyntaxError",
          executionTimeMs: 1,
        })
        .mockResolvedValueOnce({
          stdout: "",
          stderr: "runtime output",
          executionTimeMs: 1,
        }),
    };
    const results = await runTestCases(runner as never, "bad", [
      { input: "", expected: "" },
      { input: "", expected: "" },
    ]);

    expect(results[0].error).toBe("SyntaxError");
    expect(results[0].passed).toBe(false);
    expect(results[1].error).toBe("runtime output");
  });
});
