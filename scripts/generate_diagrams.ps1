# Helper script to generate PlantUML diagrams as PNG
# Usage (PowerShell):
#   ./scripts/generate_diagrams.ps1 -InputPath docs\use_case_diagram.puml
# Requirements: Java + PlantUML jar, or Docker with plantuml image.

param(
    [string]$InputPath = "docs\use_case_diagram.puml",
    [string]$PlantUmlJar = "$HOME\\tools\\plantuml.jar",
    [switch]$UseDocker
)

$full = Resolve-Path $InputPath -ErrorAction Stop
$dir = Split-Path $full

if ($UseDocker) {
    Write-Host "Using Docker image plantuml/plantuml to generate PNG..."
    docker run --rm -v "$PWD:/workspace" plantuml/plantuml -tpng "/workspace/$InputPath"
    exit $LASTEXITCODE
}

if (Test-Path $PlantUmlJar) {
    Write-Host "Using PlantUML JAR: $PlantUmlJar"
    java -jar $PlantUmlJar -tpng $InputPath
    exit $LASTEXITCODE
}

Write-Host "PlantUML JAR not found at $PlantUmlJar and --UseDocker not specified."
Write-Host "Options to generate PNG:"
Write-Host "  1) Install PlantUML JAR: https://plantuml.com/download"
Write-Host "     Then run: java -jar path\\to\\plantuml.jar -tpng $InputPath"
Write-Host "  2) Use Docker: ./scripts/generate_diagrams.ps1 -UseDocker"
Write-Host "  3) On Windows you can install PlantUML via Chocolatey and run plantuml directly."
exit 1
