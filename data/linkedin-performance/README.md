# LinkedIn Post Performance Tracking

Automatisches Tracking & Analyse der LinkedIn Post Performance nach Post-Type, KMU-Segment und Hook-Variante.

## 📊 Dateien

- **posts-tracker.csv** — Zentrale Datenquelle für alle Posts
- **analyze-performance.py** — Python-Script zur Analyse
- **performance-report.json** — Generierter JSON-Report

## 🚀 Quick Start

### Neuen Post hinzufügen:
```bash
# In posts-tracker.csv neue Zeile hinzufügen:
LP-XXX,2026-09-19,Awareness,Ressourcen-Manager,Effizienz-Framing,DE,3000,9.5,285,50,30,9.5,3,active
```

### Report generieren:
```bash
python3 analyze-performance.py
```

## 📋 CSV Spalten erklären

| Spalte | Beschreibung | Beispiel |
|--------|-------------|----------|
| post_id | Eindeutige Post-ID | LP-001 |
| publish_date | Veröffentlichungsdatum | 2026-09-15 |
| post_type | Einer der 7 Post-Types | Awareness, Education, Conversion, etc. |
| kmu_segment | Zielgruppen-Segment | Ressourcen-Manager, AI-Skeptiker, Budget-Manager, Fachkräfte-Mangel |
| hook_variant | Hook-Variante verwendet | Effizienz-Framing, Bedenken-Validierung, etc. |
| language | Sprache | DE, EN |
| impressions | Anzahl der Impressionen | 2450 |
| engagement_rate | Engagement % (clicks/impressions*100) | 8.2 |
| clicks | Anzahl Klicks auf Links | 201 |
| comments | Anzahl Kommentare | 45 |
| shares | Anzahl Shares | 32 |
| ctr_percent | Click-Through Rate % | 8.2 |
| days_tracked | Tage seit Veröffentlichung | 4 |
| status | active oder closed | active |

## 📈 Report-Output erklärt

### BY POST TYPE
Zeigt welcher Post-Type die beste Performance hat:
```
Education: 11.5% Engagement (Best)
Awareness: 10.15% Engagement
Personal Story: 9.4% Engagement
Conversion: 6.8% Engagement (Needs improvement)
```
**→ Actionable Insight**: Weniger Conversion Posts, mehr Education

### BY KMU SEGMENT
Zeigt welcher Kundentyp am besten reagiert:
```
AI-Skeptiker: 11.5% (Most engaged)
Ressourcen-Manager: 10.15%
Fachkräfte-Mangel: 9.4%
Budget-Manager: 6.8% (Needs new angle)
```
**→ Actionable Insight**: AI-Skeptiker-Posts sollten skaliert werden

### BY HOOK VARIANT
Zeigt welche Hook-Formulierung funktioniert:
```
Schnell-Gewinn-Framing: 12.1% (WINNER)
Bedenken-Validierung: 11.5%
Know-How-Rettung: 9.4%
Effizienz-Framing: 8.2%
Budget-Reallokation: 6.8% (Underperformer)
```
**→ Actionable Insight**: Schnell-Gewinn-Hooks sind deine goldene Formel

## 🎯 Metriken verstehen

**Engagement Rate**
- Definition: (Clicks + Comments + Shares) / Impressions * 100
- Ziel: > 10% ist sehr gut
- Good: 8-10%, Excellent: 11%+, Needs work: < 6%

**Click-Through Rate (CTR)**
- Definition: Clicks / Impressions * 100
- Ziel: > 10% ist strong
- Trackable via First Comment links

**Comment Rate**
- Definition: Comments / Impressions * 100
- High comment rate = Strong hook quality
- Ziel: > 2% Comments

## 🔄 Monatliches Tracking-Workflow

### Wöchentlich (jeden Montag):
1. LinkedIn Analytics öffnen
2. Metriken der vergangenen 7 Tage kopieren
3. In posts-tracker.csv aktualisieren
4. Script laufen lassen → Report generieren

### Monatlich:
```bash
python3 analyze-performance.py
# Report analysieren:
# 1. Welcher Post-Type gewinnt?
# 2. Welcher KMU-Segment am meisten engaged?
# 3. Welche Hook-Variante sollte ich skalieren?
```

## 💡 Optimization Loop

```
1. Analyse → Hook X hat 12% Engagement
           ↓
2. Insight → Das ist 3% über Durchschnitt
           ↓
3. Action → Nächste 3 Posts mit Hook X schreiben
           ↓
4. Track → Metriken in CSV eintragen
           ↓
5. Validate → Ist die Performance stabil? Ja/Nein
           ↓
6. Scale/Pivot → Wenn Ja: Skaliere Hook X
               → Wenn Nein: Pivotiere zu Hook Y
```

## 📊 Metriken zum Monitoren

**Monthly Watch List:**
- [ ] Welcher Post-Type hat highest engagement? → Verdoppelt
- [ ] Welcher Hook variant performs best? → Skaliert
- [ ] Welches KMU-Segment antwortet am besten? → Mehr Posts für diese Gruppe
- [ ] Welche First Comment Pattern hat best CTR? → Repliziert
- [ ] Budget-Manager-Posts zu schwach? → Neue Hook-Variante testen

## 🔧 Integration mit Skill

Die Top-Performer werden automatisch in den Content Strategist Skill übernommen:

```
Letzten Monat Best Performers:
1. Schnell-Gewinn-Framing (12.1% engagement)
2. Bedenken-Validierung (11.5% engagement)

→ Diese Hooks werden im Skill ganz oben angezeigt
```

## 📝 Beispiel: Performance-Based Content Calendar

Basierend auf Performance Reports:

**Montag** → Awareness + Schnell-Gewinn-Framing (12.1% ✅)
**Dienstag** → Education + Bedenken-Validierung (11.5% ✅)
**Mittwoch** → Personal Story + Know-How-Rettung (9.4% ✅)
**Donnerstag** → Methodology + [Test neuer Hook]
**Freitag** → Lead Magnet + Newsletter

## 🛠️ Erweiterungen (Roadmap)

- [ ] Automatische LinkedIn API Integration (fetch real metrics)
- [ ] Slack Integration → Wöchentliche Performance Summary
- [ ] Dashboard → Real-time Metriken in HTML
- [ ] A/B Testing Framework (Hook A vs Hook B)
- [ ] Anomalie-Erkennung (wenn Post plötzlich viral geht)
