# UrbanSignal

Application web de **signalement des problèmes urbains d'un quartier** (voirie, éclairage, propreté, eau, espaces verts…).
Projet du module **Développement distribué (J2EE / Jakarta EE)** — groupe de 5 étudiants.

## Documents

- [Analyse du besoin (PDF)](docs/Analyse_du_besoin.pdf) — réponses aux trois questions :
  1. Quel est le problème / le besoin identifié ?
  2. Qui rencontre ce problème ?
  3. Quelle est notre solution ?

Le PDF est généré par `docs/generate_pdf.py` (`pip install reportlab`, puis `python docs/generate_pdf.py`).

## Architecture envisagée

| Couche | Technologies |
|---|---|
| Présentation | JSF / JSP, carte Leaflet / OpenStreetMap |
| Services / API | Servlets, REST JAX-RS (JSON) |
| Logique métier | EJB, CDI, JMS (notifications) |
| Persistance | JPA / Hibernate, MySQL ou PostgreSQL |
| Serveur | WildFly / Payara / GlassFish |

## Équipe

| Membre | Nom |
|---|---|
| 1 | |
| 2 | |
| 3 | |
| 4 | |
| 5 | |
