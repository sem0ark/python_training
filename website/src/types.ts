export interface RunRequest {
  id: string;
  code: string;
  stdin?: string;
}

export interface RunResponse {
  id: string;
  stdout: string;
  stderr: string;
  error?: string;
  executionTimeMs: number;
}
