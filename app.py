"""Streamlit-App für den Psycho-Semantischen Guardrail.

v0.1.1: zeigt neben dem Legacy-Bewertungstext zusätzlich das
PflichtEreignisObjekt-Fragment (JSON), das an andere Repositories des
Forschungsökosystems weitergegeben werden kann.
"""

import json

import streamlit as st

from guardrail_core import (
    axiome,
    symbole,
    evaluate_expr_extended,
    evaluate_to_pflichtereignis,
)


st.set_page_config(page_title="Psycho-Semantischer Guardrail", page_icon="🛡️")
st.title("🛡️ Psycho-Semantischer Guardrail")
st.caption("v0.1.1 — mit PflichtEreignisObjekt-Ausgabe")

prompt = st.text_area("Prompt:", height=120)

if st.button("Evaluieren") and prompt:
    legacy = evaluate_expr_extended(prompt)
    fragment = evaluate_to_pflichtereignis(prompt)

    ent = fragment["guardrail"]["entscheidung"]
    farbe = {"allow": "success", "warn": "warning", "block": "error"}[ent]
    getattr(st, farbe)(f"Entscheidung: **{ent.upper()}** — {legacy}")

    st.subheader("PflichtEreignisObjekt-Fragment")
    st.code(json.dumps(fragment, indent=2, ensure_ascii=False), language="json")

    with st.expander("Details"):
        st.write("**Axiome**", axiome)
        st.write("**Symbole**", symbole)
