import streamlit as st
from guardrail_core import axiome, symbole, evaluate_expr_extended

st.title("🛡️ Psycho-Semantischer Guardrail MVP")
prompt = st.text_input("Prompt:")
if st.button("Evaluieren") and prompt:
    result = evaluate_expr_extended(prompt)
    st.markdown(f"**{result}**")
