# Project Worksheet

Gestion des **feuilles de travail (worksheets)** pour les interventions de projet :
saisie des heures par intervention, soumission au client via le **portail** pour
approbation, génération automatique des **feuilles de temps (timesheets)** et
suivi des relances.

* **Version** : `14.0.3.0.0`
* **Catégorie** : Project Management
* **Auteur** : [Numigi](https://numigi.com/r/home)
* **Licence** : AGPL-3

---

## Fonctionnalités

* Création de feuilles de travail rattachées à un projet et à un superviseur, sur
  une **période hebdomadaire** (du lundi au dimanche).
* Lignes de feuille détaillées (date, employé, tâche, description, heures) avec
  calcul automatique du **total d'heures**.
* **Workflow d'approbation** complet : brouillon → ouvert → en attente → confirmé.
* **Portail client** : envoi d'un lien sécurisé au client pour consulter et
  approuver la feuille en ligne.
* **Double voie d'approbation** : par le client (portail) ou en interne par un
  manager.
* **Génération automatique des timesheets** (`account.analytic.line`) à partir des
  lignes de la feuille, avec verrouillage des timesheets liés.
* **Relances automatiques** : tâche planifiée (cron) qui crée une activité de suivi
  lorsqu'une feuille reste trop longtemps en attente d'approbation.
* Notifications par **email** (demande d'approbation, relance, confirmation).
* **Multi-société** et contrôle d'accès par groupes (Utilisateur / Manager).
* Comptage des feuilles de travail directement depuis la fiche **Projet**.

---

## Dépendances

| Module | Usage |
|---|---|
| `project` | Projets et tâches |
| `hr_timesheet` | Feuilles de temps et employés |
| `project_stage_allow_timesheet` | Gestion des étapes autorisant la saisie de temps |

---

## Modèles

### Nouveaux modèles

| Modèle | Description |
|---|---|
| `project.worksheet` | Feuille de travail (hérite de `portal.mixin`, `mail.thread`, `mail.activity.mixin`) |
| `project.worksheet.line` | Ligne de feuille de travail (date, employé, tâche, heures) |

### Modèles étendus

| Modèle | Ajout |
|---|---|
| `project.project` | `worksheet_count` + action d'ouverture des feuilles |
| `account.analytic.line` | Champ `worksheet_id` + verrouillage des timesheets liés |
| `res.company` | Paramètres de délais (`worksheet_approval_delay`, `worksheet_reminder_delay`) |
| `res.config.settings` | Exposition des paramètres de délais dans la configuration |

---

## Cycle de vie (workflow)

```
  new  ──action_open──►  open  ──action_send_to_client──►  pending  ──┐
   ▲                                                                  │
   │                                       action_client_confirm (portail)
   │                                       action_manager_confirm (interne)
   │                                                                  ▼
   └──────────────  action_reset_to_draft  ◄────────────────────  confirmed
```

| État | Libellé | Signification |
|---|---|---|
| `new` | New | Brouillon, modifiable, seul état supprimable |
| `open` | Open | Validée en interne (lignes + heures > 0), timesheets générés |
| `pending` | Pending Approval | Envoyée au client, en attente d'approbation |
| `confirmed` | Confirmed | Approuvée (client ou manager) |

**Règles métier principales :**

* La période (`date_start` / `date_end`) doit être chronologique **et** dans la
  **même semaine calendaire**.
* Pas de **chevauchement** de feuilles pour un même projet + superviseur.
* Chaque ligne doit avoir une date **comprise dans la période** de la feuille.
* Une feuille ne peut être ouverte que si elle a des lignes et un total d'heures > 0.
* Les timesheets liés à une feuille sont **verrouillés** (pas de modification /
  suppression directe hors contexte de synchronisation).
* Suppression d'une feuille autorisée **uniquement à l'état `new`**.
* Un **manager** est requis pour remettre à `new` une feuille `confirmed` ; les
  timesheets déjà verrouillés (feuille de temps en `confirm`/`done`) bloquent le
  reset.

---

## Portail client

Lien sécurisé par jeton (`access_token`) :

* `GET /my/worksheet/<id>/<access_token>` — consultation de la feuille.
* `POST /my/worksheet/<id>/accept` — approbation (case de confirmation requise).

Un utilisateur interne arrivant sur le lien portail est **redirigé vers la vue
backend**. L'approbation client est journalisée dans le chatter avec l'adresse IP.

---

## Sécurité

Deux groupes (catégorie **Worksheets**) :

| Groupe | Droits |
|---|---|
| `group_project_worksheet_user` | Lecture / écriture / création. Ne voit que les feuilles où il est **superviseur** ou **manager du superviseur**. |
| `group_project_worksheet_manager` | Tous droits (dont suppression) et visibilité sur **toutes** les feuilles. |

Règles multi-société (`ir.rule`) appliquées sur `project.worksheet` et
`project.worksheet.line`.

---

## Configuration

Dans **Paramètres → Project Worksheet** (par société) :

| Paramètre | Défaut | Description |
|---|---|---|
| `worksheet_approval_delay` | `0` | Nombre de jours avant qu'un manager puisse forcer l'approbation. |
| `worksheet_reminder_delay` | `2` | Nombre de jours après l'envoi avant la création d'une activité de relance. |

**Tâche planifiée** : `Worksheets: Remind pending client approvals` s'exécute une
fois par jour et crée une activité de suivi « Follow up on client approval » sur
les feuilles `pending` dont le délai de relance est dépassé.

---

## Installation

```bash
# placer le module dans votre addons_path puis :
odoo -u project_worksheet -d <votre_base>
```

---

## Tests

```bash
odoo -i project_worksheet -d <base_de_test> --test-enable --stop-after-init
```

Les tests (`tests/test_project_worksheet.py`) couvrent le calcul du total
d'heures, la validation des dates, la génération des timesheets, les transitions
d'états et la logique de relance.

---

## Mainteneur

Ce module est maintenu par **Numigi**.

Pour toute question ou contribution : <https://numigi.com/r/home>
