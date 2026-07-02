"""Tests für die v0.1.1-API des Guardrail-Cores.

Läuft ohne externe Abhängigkeiten (kein streamlit-Import).
"""

import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from guardrail_core import (  # noqa: E402
    evaluate_expr_extended,
    evaluate_to_pflichtereignis,
)


def test_leerer_prompt_ist_allow():
    f = evaluate_to_pflichtereignis("")
    assert f["guardrail"]["entscheidung"] == "allow"
    assert f["bewertung"]["stufe"] == "ok"
    assert f["analyse"]["marker"] == []
    assert f["meta"]["core_version"] == "0.1.1"


def test_pathologie_wird_blockiert():
    f = evaluate_to_pflichtereignis("das ist doch eine lüge")
    assert f["guardrail"]["entscheidung"] == "block"
    assert f["guardrail"]["axiom"] == 13
    assert f["bewertung"]["stufe"] == "bruch"
    assert "V_pathologie" in f["analyse"]["marker"]


def test_einzelner_marker_ergibt_warn():
    f = evaluate_to_pflichtereignis("das ist halb so wild")
    assert f["guardrail"]["entscheidung"] == "warn"
    assert f["bewertung"]["stufe"] == "spannung"
    assert "V1" in f["analyse"]["marker"]
    assert f["umcodierung"]["operator"] == "U1"


def test_zustand_id_format():
    f = evaluate_to_pflichtereignis("das ist halb so wild")
    zid = f["meta"]["zustand_id"]
    assert zid.count(":") == 2
    parts = zid.split(":")
    assert parts[0].startswith("W")
    assert parts[1].startswith("U")
    assert parts[2] in ("ok", "spannung", "verzerrung", "bruch")


def test_legacy_wrapper_string_bei_block():
    s = evaluate_expr_extended("das ist eine lüge")
    assert s.startswith("✗ Blockiert")


def test_legacy_wrapper_string_bei_allow():
    s = evaluate_expr_extended("")
    assert "Unbekannt" in s or "Grenzbereich" in s


def test_axiom_bei_stufe_ok_ist_11():
    f = evaluate_to_pflichtereignis("")
    assert f["guardrail"]["axiom"] == 11


def test_axiom_bei_warn_ist_12():
    f = evaluate_to_pflichtereignis("das ist halb so wild")
    assert f["guardrail"]["axiom"] == 12


if __name__ == "__main__":
    import types
    fns = [
        test_leerer_prompt_ist_allow,
        test_pathologie_wird_blockiert,
        test_einzelner_marker_ergibt_warn,
        test_zustand_id_format,
        test_legacy_wrapper_string_bei_block,
        test_legacy_wrapper_string_bei_allow,
        test_axiom_bei_stufe_ok_ist_11,
        test_axiom_bei_warn_ist_12,
    ]
    fail = 0
    for fn in fns:
        try:
            fn()
            print(f"[ok] {fn.__name__}")
        except Exception as e:
            fail += 1
            print(f"[FAIL] {fn.__name__}: {e!r}")
    print(f"\n{len(fns)-fail}/{len(fns)} Tests bestanden")
    raise SystemExit(1 if fail else 0)
