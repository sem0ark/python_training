function Run-Ruff {
    Write-Host "Running Ruff..." -ForegroundColor Cyan
    uv run ruff check --select I --fix
    uv run ruff format .
}

function Run-Pytest {
    Write-Host "Running Pytest..." -ForegroundColor Cyan
    uv run pytest .
}

function Run-Solutions {
    Write-Host "Running Solution Files..." -ForegroundColor Cyan
    $files = Get-ChildItem "*-solution.py"
    foreach ($file in $files) {
        Write-Host "Processing $($file.Name)..." -ForegroundColor Yellow
        if ($file.Name -like "*coverage*") {
            uv run internal_coverage_runner.py $file.FullName
        } elseif ($file.Name -like "*type*") {
            uv run internal_type_checker.py $file.FullName
        } else {
            uv run $file.FullName
        }
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Execution of $($file.Name) failed."
            exit $LASTEXITCODE
        }
    }
}

function Run-QualityGate {
    Write-Host "Starting Quality Gate..." -ForegroundColor Blue
    Run-Ruff
    Run-Solutions
    Write-Host "Quality Gate Passed!" -ForegroundColor Green
}

# Simple command dispatcher
if ($args.Count -eq 0) {
    Write-Host "Usage: ./make.ps1 <command>"
    Write-Host "Commands: ruff, pytest, run_solutions, quality_gate"
    exit
}

switch ($args[0]) {
    "ruff" { Run-Ruff }
    "pytest" { Run-Pytest }
    "run_solutions" { Run-Solutions }
    "quality_gate" { Run-QualityGate }
    default { Write-Error "Unknown command: $($args[0])" }
}
