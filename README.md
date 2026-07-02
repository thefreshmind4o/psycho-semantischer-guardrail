# Psycho-Semantischer Guardrail

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21139679.svg)](https://doi.org/10.5281/zenodo.21139679)

Axiomatische Governance-Schicht für KI mit PSS und SM69 — filtert Lüge-Spektren präventiv.

**v0.1.1** — liefert zusätzlich zum Legacy-Bewertungstext ein `PflichtEreignisObjekt`-Fragment (Feldkonvention aus [`modellbibliothek-identitaet`](https://github.com/thefreshmind4o/modellbibliothek-identitaet), Zustands-ID aus [`x-matrix-kern`](https://github.com/thefreshmind4o/x-matrix-kern)).

## Rolle im Forschungsökosystem
Dieses Repository ist Teil eines fünfteiligen Ökosystems (siehe [ARCHITEKTURMODELL.md](./ARCHITEKTURMODELL.md)):

1. `forschungsdaten-und-schemata`
2. **`psycho-semantischer-guardrail`** ← dieses Repo
3. `x-matrix-kern`
4. `modellbibliothek-identitaet`
5. `thefreshmind4o.github.io`

Aufgabe: sprachliche Vorprüfung, Markererkennung, Modalitätslogik und erste Statusableitung.

## Axiome
- **11** — Wahrheit ist kindliche Basis (Unten: Unschuld, ✓)
- **12** — Zweifel gabelt in Pubertät (Mitte: ⚠, 6↑/9↓)
- **13** — Systemische Lüge oben (✗, 666/999 blocken)

## API (v0.1.1)

```python
from guardrail_core import evaluate_to_pflichtereignis

frag = evaluate_to_pflichtereignis("das ist halb so wild")
# -> {
#   "analyse":    {"marker": ["V1"]},
#   "umcodierung":{"operator": "U1"},
#   "bewertung":  {"waagenzustand": "W0", "stufe": "spannung"},
#   "guardrail":  {"entscheidung": "warn", "axiom": 12},
#   "meta":       {"zustand_id": "W0:U1:spannung", "core_version": "0.1.1", ...}
# }
```

Die Legacy-Funktion `evaluate_expr_extended(expr) -> str` bleibt für Rückwärtskompatibilität erhalten und ist intern als Wrapper implementiert.

## Tests

```bash
python3 tests/test_guardrail_core.py
```

v0.1.1: 8/8 Tests bestehen (ohne externe Abhängigkeiten).

## Demo
Streamlit-App zur Live-Prüfung von Prompts:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Autor
- Maximilian Heiler
- ORCID: [0009-0003-2785-1710](https://orcid.org/0009-0003-2785-1710)
- Independent Researcher, Hamburg

## Lizenz
Apache-2.0 — siehe [`LICENSE`](./LICENSE) und [`LIZENZHINWEIS.md`](./LIZENZHINWEIS.md).

## Zitation
Siehe [`CITATION.cff`](./CITATION.cff). DOI wird nach dem ersten Release über Zenodo geprägt und in [`DOI_REGISTER.md`](./DOI_REGISTER.md) eingetragen.

## Release
Ablauf: [`RELEASE_CHECKLISTE.md`](./RELEASE_CHECKLISTE.md). Metadatenkonvention: [`METADATEN_STANDARD.md`](./METADATEN_STANDARD.md).
