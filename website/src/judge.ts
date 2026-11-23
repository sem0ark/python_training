import { PythonRunner } from "./pythonRunner";

export interface TestCase {
  input: string;
  expected: string;
}
export interface TestResult extends TestCase {
  actual: string;
  passed: boolean;
  error?: string;
  executionTimeMs: number;
}

export async function runTestCases(
  runner: PythonRunner,
  code: string,
  cases: TestCase[],
  timeoutMs = 3000,
): Promise<TestResult[]> {
  const results: TestResult[] = [];
  for (const testCase of cases) {
    const result = await runner.run(code, testCase.input, timeoutMs);
    const actual = result.stdout.trim();
    results.push({
      ...testCase,
      actual,
      passed: !result.error && actual === testCase.expected,
      error: result.error ?? (result.stderr || undefined),
      executionTimeMs: result.executionTimeMs,
    });
  }
  return results;
}
