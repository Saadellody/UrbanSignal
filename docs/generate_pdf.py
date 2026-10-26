"""Génère docs/Analyse_du_besoin.pdf (réponses aux 3 questions du projet)."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (ListFlowable, ListItem, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

OUT = Path(__file__).with_name("Analyse_du_besoin.pdf")
PRIMARY = colors.HexColor("#1F5F8B")

styles = getSampleStyleSheet()
title = ParagraphStyle("T", parent=styles["Title"], textColor=PRIMARY, fontSize=22, spaceAfter=4)
subtitle = ParagraphStyle("ST", parent=styles["Normal"], alignment=1, fontSize=11,
                          textColor=colors.HexColor("#555555"), spaceAfter=14)
h1 = ParagraphStyle("H1", parent=styles["Heading2"], textColor=PRIMARY, spaceBefore=14, spaceAfter=6)
h2 = ParagraphStyle("H2", parent=styles["Heading3"], spaceBefore=6, spaceAfter=4)
body = ParagraphStyle("B", parent=styles["Normal"], fontSize=10.5, leading=15, alignment=TA_JUSTIFY,
                      spaceAfter=6)


def bullets(items):
    return ListFlowable([ListItem(Paragraph(t, body), leftIndent=12) for t in items],
                        bulletType="bullet", start="•", leftIndent=14)


def table(rows, widths):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF4F9")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def cell(text):
    return Paragraph(text, ParagraphStyle("c", parent=body, fontSize=9.5, leading=12, alignment=0,
                                          spaceAfter=0))


story = [
    Paragraph("UrbanSignal", title),
    Paragraph("Application de signalement des problèmes urbains d'un quartier<br/>"
              "Module : Développement distribué (J2EE / Jakarta EE) — Groupe de 5 étudiants", subtitle),

    table([["Membre", "Nom et prénom"]] + [[f"Membre {i}", ""] for i in range(1, 6)],
          [4 * cm, 12 * cm]),

    # ---------------- Question 1 ----------------
    Paragraph("1. Quel est le problème ? Quel besoin avons-nous identifié ?", h1),
    Paragraph(
        "Dans nos quartiers, de nombreux problèmes du quotidien restent visibles pendant des semaines : "
        "nids-de-poule, lampadaires en panne, déchets non ramassés, fuites d'eau, égouts bouchés, "
        "trottoirs dégradés, feux de signalisation défectueux, dépôts sauvages, espaces verts abandonnés. "
        "Le problème n'est pas seulement l'existence de ces dégradations, mais surtout <b>l'absence d'un canal "
        "simple et efficace pour les signaler</b> et en suivre le traitement.", body),
    Paragraph("Constats :", h2),
    bullets([
        "Signaler un problème est compliqué : il faut se déplacer à la commune, téléphoner ou écrire, sans "
        "savoir quel service est responsable.",
        "Les signalements sont dispersés (appels, réseaux sociaux, papier) : ils se perdent, sont dupliqués "
        "ou mal localisés.",
        "Aucune transparence : le citoyen ne sait pas si sa demande a été reçue, ni quand elle sera traitée.",
        "La municipalité manque de données fiables (localisation précise, photos, fréquence, priorité) "
        "pour planifier ses interventions et répartir ses équipes.",
        "Le manque de suivi crée de la frustration et une perte de confiance entre habitants et autorités.",
    ]),
    Paragraph(
        "<b>Besoin identifié :</b> une plateforme centralisée, accessible à tous, permettant de signaler "
        "rapidement un problème urbain géolocalisé avec photo, de le transmettre automatiquement au service "
        "compétent et de suivre son traitement jusqu'à sa résolution.", body),

    # ---------------- Question 2 ----------------
    Paragraph("2. Qui rencontre ce problème ?", h1),
    Paragraph("Le problème touche l'ensemble des acteurs de la vie du quartier :", body),
    table([
        ["Acteur", "Comment il est concerné"],
        [cell("<b>Citoyens / habitants</b>"),
         cell("Subissent directement les dégradations (sécurité, propreté, confort) et n'ont pas de moyen "
              "simple de les signaler ni d'en suivre la résolution.")],
        [cell("<b>Étudiants</b>"),
         cell("Se déplacent quotidiennement à pied ou en transport : éclairage défaillant, routes abîmées "
              "et insécurité sur le trajet université / logement.")],
        [cell("<b>Enseignants et personnel</b>"),
         cell("Concernés par l'état des abords des écoles et universités (sécurité des élèves, accès, "
              "propreté).")],
        [cell("<b>Commerçants</b>"),
         cell("Un environnement dégradé (déchets, voirie, éclairage) fait fuir la clientèle et nuit à "
              "l'activité économique.")],
        [cell("<b>Personnes âgées / à mobilité réduite</b>"),
         cell("Particulièrement exposées aux trottoirs abîmés, obstacles et absence d'éclairage.")],
        [cell("<b>Municipalité et services techniques</b>"),
         cell("Reçoivent des informations incomplètes et dispersées ; ont besoin d'outils pour prioriser, "
              "affecter et suivre les interventions.")],
        [cell("<b>Associations de quartier</b>"),
         cell("Souhaitent porter la voix des habitants et mesurer l'évolution de l'état du quartier.")],
    ], [5 * cm, 11 * cm]),

    # ---------------- Question 3 ----------------
    Paragraph("3. Quelle est notre solution ? Comment notre application peut-elle aider ?", h1),
    Paragraph(
        "Nous proposons <b>UrbanSignal</b>, une application web distribuée développée en <b>J2EE / Jakarta EE</b>, "
        "qui met en relation les habitants et les services municipaux autour du signalement et du traitement "
        "des problèmes urbains.", body),
    Paragraph("Fonctionnalités principales :", h2),
    bullets([
        "<b>Signalement rapide</b> : catégorie (voirie, éclairage, propreté, eau, espaces verts…), description, "
        "photo et position GPS / point sur la carte.",
        "<b>Carte interactive</b> du quartier affichant les signalements et leur état, pour éviter les doublons "
        "(un citoyen peut « soutenir » un signalement existant).",
        "<b>Suivi en temps réel</b> du statut : Nouveau → Validé → En cours → Résolu, avec notifications "
        "(e-mail / dans l'application) à chaque changement.",
        "<b>Espace administrateur municipal</b> : validation, priorisation, affectation des signalements aux "
        "services / agents techniques.",
        "<b>Espace agent technique</b> : liste des interventions, mise à jour du statut, photo « après » comme "
        "preuve de résolution.",
        "<b>Tableau de bord et statistiques</b> : nombre de signalements par catégorie, par zone, délai moyen "
        "de résolution, zones les plus touchées.",
        "<b>Gestion des comptes et des rôles</b> : citoyen, agent, administrateur ; commentaires et évaluation "
        "de la résolution par le citoyen.",
    ]),
    Paragraph("Apports de l'application :", h2),
    bullets([
        "<b>Pour les citoyens</b> : signaler en moins d'une minute, être informé et voir que leur voix compte.",
        "<b>Pour la municipalité</b> : informations précises et centralisées, meilleure planification, "
        "réduction des délais et des coûts d'intervention.",
        "<b>Pour le quartier</b> : un cadre de vie plus sûr et plus propre, plus de transparence et une "
        "participation citoyenne renforcée.",
    ]),
    Paragraph(
        "<b>En résumé :</b> UrbanSignal transforme un processus lent et opaque en un service numérique "
        "simple, transparent et traçable.", body),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "UrbanSignal — Analyse du besoin")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                  bottomMargin=2 * cm, title="UrbanSignal — Analyse du besoin",
                  author="Groupe UrbanSignal").build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF généré : {OUT}")
