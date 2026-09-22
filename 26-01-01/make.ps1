$Cli = "uv run python ../cli.py"

function Run-Ruff {
    uv run ruff check --select I --fix .
    uv run ruff format .
}

function Run-Tests {
    uv run pytest .
}

function Invoke-Cli {
    param([string[]]$Arguments)
    Invoke-Expression "$Cli $($Arguments -join ' ')"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Require-Prefix {
    param([string]$Command, [string]$Prefix)
    if ([string]::IsNullOrWhiteSpace($Prefix)) {
        Write-Error "Usage: ./make.ps1 $Command <prefix>"
        exit 1
    }
}

if ($args.Count -eq 0) {
    Write-Host "Usage: ./make.ps1 <command> [prefix]"
    Write-Host "Commands: ruff, test, pack, unpack, run, watch, solution, quality_gate"
    exit 0
}

switch ($args[0]) {
    "ruff" { Run-Ruff }
    "test" { Run-Tests }
    "pack" { Invoke-Cli @("pack") }
    "unpack" { Invoke-Cli @("unpack") }
    "run" {
        Require-Prefix $args[0] $args[1]
        Invoke-Cli @("run", $args[1])
    }
    "watch" {
        Require-Prefix $args[0] $args[1]
        Invoke-Cli @("watch", $args[1])
    }
    "solution" {
        Require-Prefix $args[0] $args[1]
        Invoke-Cli @("solution", $args[1])
    }
    "quality_gate" {
        Run-Ruff
        Run-Tests
    }
    default { Write-Error "Unknown command: $($args[0])"; exit 1 }
}
