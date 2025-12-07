**PlantUML Diagrams**

- **Use case diagram**: `docs/use_case_diagram.puml`

How to generate PNG locally

- Option A — PlantUML JAR (Java):

```powershell
# Download PlantUML: https://plantuml.com/download
# Then from the repository root:
java -jar path\to\plantuml.jar -tpng docs\use_case_diagram.puml
```

- Option B — Docker (no local jar required):

```powershell
# from repo root (Windows PowerShell)
docker run --rm -v "$PWD:/workspace" plantuml/plantuml -tpng "/workspace/docs/use_case_diagram.puml"
```

- Option C — Helper script (PowerShell):

```powershell
# Try generating via local PlantUML jar (default expected at $HOME\tools\plantuml.jar)
./scripts/generate_diagrams.ps1

# Or force Docker
./scripts/generate_diagrams.ps1 -UseDocker
```

Notes

- The generated PNG will be placed in `docs/` next to the `.puml` file (filename `use_case_diagram.png`).
- If you want me to produce the PNG here, I can do so if you enable running PlantUML locally or provide the PlantUML jar path; otherwise I can (a) embed a generated PNG if allowed, or (b) produce an SVG/text alternative.
