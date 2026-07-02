# Architekturmodell des Forschungsökosystems

## Zweck
Dieses Dokument beschreibt die formalen Beziehungen zwischen den vier Kern-Repositories:
- `psycho-semantischer-guardrail`
- `x-matrix-kern`
- `modellbibliothek-identitaet`
- `forschungsdaten-und-schemata`

Die Struktur dient als gemeinsame Referenz für Portal, Backend, Rechenkern, Dashboard und spätere DOI-/Release-Pfade.

## Rollen der Repositories

### 1. psycho-semantischer-guardrail
Aufgabe: sprachliche Vorprüfung, Markererkennung, Modalitätslogik, erste Statusableitung.

Liest:
- Rohtext
- sprachliche Signale
- Pflicht-Ereignisobjekte aus `forschungsdaten-und-schemata`

Schreibt:
- Markerlisten
- Modalitätsbefunde
- Vorprüfungsstatus

### 2. x-matrix-kern
Aufgabe: formale Achsen, Zustände, Routinglogik und Zuordnung zu Identität/System-Norm.

Liest:
- Marker aus `psycho-semantischer-guardrail`
- Grundbegriffe aus `modellbibliothek-identitaet`

Schreibt:
- Achsenpositionen
- Zustandsverdichtungen
- Routingfelder wie `K1`, `R2`

### 3. modellbibliothek-identitaet
Aufgabe: Theorieebene, Begriffslogik, Relationen, Bedeutungsräume.

Liest:
- theoretische Begriffe
- Umcodierungsrelationen
- Identitäts- und Ko-Abhängigkeitskonzepte

Schreibt:
- Begriffsdefinitionen
- Relationsobjekte
- Interpretationsrahmen für Guardrail und X-Matrix

### 4. forschungsdaten-und-schemata
Aufgabe: kanonische Datenverträge, JSON-Schemas, Pflicht-Ereignisobjekte, Referenzdaten.

Liest:
- Anforderungen aus Dashboard, API und Rechenkern

Schreibt:
- Pflicht-Ereignisobjekte
- Schema-Definitionen
- Referenzbeispiele
- Kennzahlen- und Visualisierungsblöcke

## Abhängigkeitslogik

### Primäre Flüsse
1. `forschungsdaten-und-schemata` definiert das gemeinsame Eingabe- und Ausgabeformat.
2. `psycho-semantischer-guardrail` verarbeitet Rohtext in dieses Format hinein.
3. `x-matrix-kern` verdichtet Marker in Achsen- und Zustandslogik.
4. `modellbibliothek-identitaet` liefert die interpretative Begriffsschicht für Marker, Zustände und Umcodierungen.
5. Das Portal `thefreshmind4o.github.io` dokumentiert die sichtbaren Projektstände, Verweise und DOI-Pfade.

### Sekundäre Flüsse
- `modellbibliothek-identitaet` beeinflusst Benennung und Interpretation von Markern im Guardrail.
- `x-matrix-kern` nutzt Begriffe indirekt, aber formalisiert sie in Routing- und Zustandsfeldern.
- `forschungsdaten-und-schemata` muss Änderungen aus Guardrail, X-Matrix und Dashboard rückspiegeln, damit das Pflichtobjekt aktuell bleibt.

## Gemeinsames Kernobjekt
Das verbindende Objekt ist das `PflichtEreignisObjekt`.

Es enthält mindestens:
- `id`
- `rohtext`
- `marker`
- `zustand`
- `kennzahlen`
- `visualisierung`

Daraus ergibt sich die Systemkopplung:
- Guardrail füllt `rohtext`, `marker`, `modalitaet`, `status`
- X-Matrix ergänzt `achsen`, `routing`, `zustandsverdichtung`
- Modellbibliothek liefert `begriffliche_rahmung`, `relationen`, `ebene`
- Datenverträge definieren, welche Felder gültig und pflichtig sind

## Architekturprinzipien
- Alle sichtbaren Marker und Felder deutsch führen.
- Theorieschicht und Rechenkern trennen, aber referenziell koppeln.
- Pflichtobjekte vor UI-Ansichten definieren.
- Portal, Release, DOI und Dokumentation als eigene Veröffentlichungsschicht behandeln.
- Repositories modular halten, aber über gemeinsame Objekte synchronisieren.

## Änderungsregeln
- Neue Marker zuerst im Guardrail und in der Modellbibliothek beschreiben.
- Neue Achsen oder Zustände zuerst im `x-matrix-kern` definieren.
- Neue Pflichtfelder immer zuerst im Repository `forschungsdaten-und-schemata` festlegen.
- Portaländerungen folgen den fachlichen Änderungen, nicht umgekehrt.

## Release-Reihenfolge
1. `forschungsdaten-und-schemata`
2. `psycho-semantischer-guardrail`
3. `x-matrix-kern`
4. `modellbibliothek-identitaet`
5. `thefreshmind4o.github.io`

Begründung: Zuerst wird das gemeinsame Datenobjekt stabilisiert, danach die Ableitungs- und Verdichtungslogik, zuletzt Dokumentation und Sichtbarkeit.
