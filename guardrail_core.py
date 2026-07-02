"""Psycho-Semantischer Guardrail — Core-Modul.

v0.1.1: zusätzlich zum bisherigen String-Ergebnis liefert der Guardrail nun
ein PflichtEreignisObjekt-Fragment, das die Feldkonvention aus
modellbibliothek-identitaet (v0.1.0) und den X-Matrix-Kern (v0.1.0) nutzt:

  analyse.marker              -> IDs aus verzerrungsmarker (V1..V8)
  umcodierung.operator        -> dominanter Operator (U1..U9)
  bewertung.waagenzustand     -> Waagen-ID (W0..W4)
  bewertung.stufe             -> ok | spannung | verzerrung | bruch
  meta.zustand_id             -> W2:U1:verzerrung
  meta.erklaerung             -> Kurzerklärung

Die alte Funktion `evaluate_expr_extended()` bleibt für Rückwärtskompatibilität
erhalten und ruft intern den neuen Pfad auf.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


# -----------------------------------------------------------------------------
# Legacy-Vokabular (unverändert seit v0.1.0)
# -----------------------------------------------------------------------------

axiome = {
    11: "Wahrheit ist kindliche Basis (Unten: Unschuld, ✓)",
    12: "Zweifel gabelt in Pubertät (Mitte: ⚠, 6↑/9↓)",
    13: "Systemische Lüge oben (✗, 666/999 blocken)",
}

symbole = {
    "A": "Erkenntnis",
    "B": "Sein/Identität",
    "C": "Sehen/Verändern",
    "6↑": "Stabilität hoch",
    "9↓": "Entgleisung runter",
    "666": "Pathologie",
    "999": "Systemfehler",
}


# -----------------------------------------------------------------------------
# v0.1.1 — Anbindung an Modellbibliothek
# -----------------------------------------------------------------------------

# Marker-Erkennung: Signalwörter -> Verzerrungsmarker-ID (V1..V8).
# Konservative erste Zuordnung; wird in v0.2 an eine begründete Regeltafel
# aus modellbibliothek-identitaet/begriffe/verzerrungsmarker.json angebunden.
_MARKER_SIGNALE: Dict[str, List[str]] = {
    "V1": ["bagatell", "nicht so schlimm", "halb so wild"],
    "V2": ["eigentlich müsste", "als ob ich", "rolle"],
    "V3": ["kontext", "situationsbedingt", "damals war"],
    "V4": ["deshalb war ich", "weil du", "wegen dir"],
    "V5": ["nicht meine schuld", "du hast angefangen", "verantwortung"],
    "V6": ["ich bin nur wütend", "eigentlich bin ich", "aber ich fühle"],
    "V7": ["ist doch normal", "macht doch jeder", "norm"],
    "V8": ["dafür stehe ich", "legitim", "berechtigt"],
    # Pathologie-Signale (aus dem Legacy-Vokabular)
    "V_pathologie": ["lüge", "666", "999", "9↓"],
}

# Waagen-Signale: einfache Heuristik für W0..W4.
_WAAGEN_SIGNALE: Dict[str, List[str]] = {
    "W0": [],  # Default (Neutral)
    "W1": ["zweifel", "unsicher", "pubertät"],
    "W2": ["spannung", "gabelung"],
    "W3": ["entgleisung", "kippt"],
    "W4": ["bruch", "666", "999"],
}

# Marker -> Operator (deckungsgleich mit x-matrix-kern v0.1.0-Default).
_MARKER_OPERATOR: Dict[str, str] = {
    "V1": "U1",
    "V2": "U2",
    "V3": "U3",
    "V4": "U4",
    "V5": "U5",
    "V6": "U6",
    "V7": "U7",
    "V8": "U8",
    "V_pathologie": "U9",
}

_FALLBACK_OPERATOR = "U9"


def _finde_marker(expr_lower: str) -> List[str]:
    """Sammelt alle Marker-IDs, deren Signalwörter im Text vorkommen."""
    treffer: List[str] = []
    for marker_id, signale in _MARKER_SIGNALE.items():
        if any(s in expr_lower for s in signale):
            treffer.append(marker_id)
    return treffer


def _finde_waage(expr_lower: str) -> str:
    """Erste Waage, deren Signalwort auftaucht — sonst W0."""
    for waage_id in ("W4", "W3", "W2", "W1"):  # ernstere zuerst
        if any(s in expr_lower for s in _WAAGEN_SIGNALE[waage_id]):
            return waage_id
    return "W0"


def _stufe_aus_markern(marker: List[str]) -> str:
    """Grobe Stufe (deckt sich mit x-matrix-kern v0.1.0)."""
    n = len(marker)
    if n == 0:
        return "ok"
    if n == 1:
        return "spannung"
    if n <= 3:
        return "verzerrung"
    return "bruch"


def _dominanter_operator(marker: List[str]) -> str:
    for m in marker:
        if m in _MARKER_OPERATOR:
            return _MARKER_OPERATOR[m]
    return _FALLBACK_OPERATOR


def _blockiert(marker: List[str]) -> bool:
    """Blockade nach Axiom 13 — Pathologie-Marker vorhanden."""
    return "V_pathologie" in marker


# -----------------------------------------------------------------------------
# Neue API v0.1.1
# -----------------------------------------------------------------------------

def evaluate_to_pflichtereignis(expr: str) -> dict:
    """Bewertet einen Prompt und liefert ein PflichtEreignisObjekt-Fragment.

    Feldkonvention: siehe Modul-Docstring / modellbibliothek-identitaet.
    """
    expr_lower = (expr or "").lower()
    marker = _finde_marker(expr_lower)
    waage = _finde_waage(expr_lower)
    stufe = _stufe_aus_markern(marker)
    operator = _dominanter_operator(marker)

    blockiert = _blockiert(marker)
    if blockiert:
        # Blockade override: harte Stufe bruch, Operator U9 (Passthrough / Ausleitung).
        stufe = "bruch"
        operator = "U9"

    entscheidung = "block" if blockiert else ("warn" if stufe != "ok" else "allow")

    zustand_id = f"{waage}:{operator}:{stufe}"
    erklaerung = (
        f"{len(marker)} Marker: {marker or '—'}; Waage={waage}; "
        f"Operator={operator}; Stufe={stufe}; Entscheidung={entscheidung}"
    )

    return {
        "analyse": {
            "marker": list(marker),
        },
        "umcodierung": {
            "operator": operator,
        },
        "bewertung": {
            "waagenzustand": waage,
            "stufe": stufe,
        },
        "guardrail": {
            "entscheidung": entscheidung,   # allow | warn | block
            "axiom": 13 if blockiert else (12 if stufe != "ok" else 11),
        },
        "meta": {
            "zustand_id": zustand_id,
            "erklaerung": erklaerung,
            "core_version": "0.1.1",
        },
    }


# -----------------------------------------------------------------------------
# Legacy-API v0.1.0 (Wrapper, gibt weiterhin einen String zurück)
# -----------------------------------------------------------------------------

def evaluate_expr_extended(expr: str) -> str:
    """Legacy-Wrapper: liefert den bisherigen String-Bewertungs-Text.

    Baut den String aus dem neuen Fragment auf, um beide Pfade konsistent zu halten.
    """
    frag = evaluate_to_pflichtereignis(expr)
    ent = frag["guardrail"]["entscheidung"]
    stufe = frag["bewertung"]["stufe"]
    marker = frag["analyse"]["marker"]

    if ent == "block":
        return "✗ Blockiert (Axiom 13) – Pathologie erkannt"

    # Legacy-Scoring, damit Bestandsnutzer nicht überrascht werden.
    score = len(marker)
    if stufe == "ok":
        return "⚠ Unbekannt (Score: 0)"
    if stufe in ("spannung", "verzerrung"):
        detail = ", ".join(marker) if marker else ""
        return f"⚠ Grenzbereich {detail} (Score: {score})".strip()
    # stufe == "bruch"
    return f"✓ Stabil (Score: {score})" if score >= 3 else f"⚠ Grenzbereich (Score: {score})"


__all__ = [
    "axiome",
    "symbole",
    "evaluate_expr_extended",
    "evaluate_to_pflichtereignis",
]
