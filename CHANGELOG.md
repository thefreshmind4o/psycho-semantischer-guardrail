# Changelog

## v0.1.1 — 2026-07-02

### Neu
- `evaluate_to_pflichtereignis(expr) -> dict` liefert ein Fragment für das `PflichtEreignisObjekt`.
- Feldpfade folgen der v0.1.0-Konvention aus `modellbibliothek-identitaet`:
  - `analyse.marker` (V1..V8 / V_pathologie)
  - `umcodierung.operator` (U1..U9)
  - `bewertung.waagenzustand` (W0..W4)
  - `bewertung.stufe` (`ok`, `spannung`, `verzerrung`, `bruch`)
  - `guardrail.entscheidung` (`allow`, `warn`, `block`) und `guardrail.axiom` (11/12/13)
  - `meta.zustand_id` (`W2:U1:verzerrung`)
- Marker→Operator-Zuordnung deckungsgleich mit `x-matrix-kern` v0.1.0-Default.
- `app.py`: Streamlit zeigt Legacy-String und JSON-Fragment nebeneinander.
- 8 Tests in `tests/test_guardrail_core.py` (ohne externe Abhängigkeiten).

### Rückwärtskompatibilität
- `evaluate_expr_extended(expr) -> str` bleibt in unveränderter Signatur bestehen und ist intern als Wrapper um den neuen Pfad implementiert. Bestandsintegrationen laufen ohne Anpassung weiter.

### Bezug zum Ökosystem
- Feldpfade: `modellbibliothek-identitaet/docs/UEBERBLICK.md`
- Zustandslogik: `x-matrix-kern/docs/UEBERBLICK.md`

## v0.1.0 — 2026-07-02

- Erste öffentliche Version. DOI: [10.5281/zenodo.21139679](https://doi.org/10.5281/zenodo.21139679).
- Legacy-API `evaluate_expr_extended`, Axiome 11/12/13, Symboltabelle, Streamlit-Demo.
