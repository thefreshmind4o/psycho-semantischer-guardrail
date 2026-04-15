# Guardrail core module with axiome and symbole definitions

axiome = {
    11: "Wahrheit ist kindliche Basis (Unten: Unschuld, ✓)",
    12: "Zweifel gabelt in Pubertät (Mitte: ⚠, 6↑/9↓)",
    13: "Systemische Lüge oben (✗, 666/999 blocken)"
}

symbole = {
    'A': 'Erkenntnis',
    'B': 'Sein/Identität',
    'C': 'Sehen/Verändern',
    '6↑': 'Stabilität hoch',
    '9↓': 'Entgleisung runter',
    '666': 'Pathologie',
    '999': 'Systemfehler'
}


def evaluate_expr_extended(expr):
    score = 0
    warnings = []
    expr_lower = expr.lower()

    # Erweiterte Checks
    if any(word in expr_lower for word in ['wahrheit', 'unschuld', 'axiome', 'a', 'b', 'c']):
        score += 2
    if '6↑' in expr or 'stabilität' in expr_lower:
        score += 1
    if any(word in expr_lower for word in ['zweifel', 'pubertät']):
        warnings.append('⚠ Pubertäts-Gabelung')
    if any(word in expr_lower for word in ['lüge', '666', '999', '9↓']):
        return '✗ Blockiert (Axiom 13) – Pathologie erkannt'
    if 'yin' in expr_lower or 'trennung' in expr_lower:
        warnings.append('Yin: Trennung (-/)')
    if 'yang' in expr_lower or 'verbindung' in expr_lower:
        score += 1
        warnings.append('Yang: Verbindung (+×)')

    if score >= 3:
        return '✓ Stabil (Score: ' + str(score) + ')'
    elif score >= 1:
        return '⚠ Grenzbereich ' + (', '.join(warnings) if warnings else '') + ' (Score: ' + str(score) + ')'
    else:
        return '⚠ Unbekannt (Score: 0)'
