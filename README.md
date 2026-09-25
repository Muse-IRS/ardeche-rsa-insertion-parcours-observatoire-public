# Observatoire public du parcours RSA — Ardèche

**Projet indépendant et sans affiliation institutionnelle.** Restitution publique et pédagogique consacrée au suivi RSA : orientation, référents, dispositifs d'insertion, marchés et organismes, circulation des données, documents administratifs et droit d'accès.

**Charte : « Un socle, une posture ».** Reconnaître les apports documentés, décrire les écarts réellement établis, publier les inconnues sans accusation ni faux équilibre.

## Architecture

Le site statique occupe la racine du dépôt pour permettre GitHub Pages depuis `main / (root)`. Une branche `gh-pages` identique est également préparée pour une configuration compatible avec l'Observatoire Ardèche Habitat. **Une branche présente ne signifie pas que GitHub Pages est activé : tester le lien HTTP.**

Accueil prévu : https://muse-irs.github.io/ardeche-rsa-insertion-parcours-observatoire-public/

- `index.html` : accueil et parcours pédagogique.
- `marches-prestataires.html` : distinguer publication, attribution, contrat, sous-traitance, exécution.
- `demarches.html` : accès aux documents, référent, RGPD et sources officielles.
- `sources.html` : registre lisible des sources primaires, périmètres, temporalités et limites.
- `charte-editoriale.html` et `privacy.html` : cadre éditorial et confidentialité.
- `affiche-qr-observatoire.html` : affiche A4 avec QR code **autonome** pointant vers ce site et lien de retour vers l'accueil.
- `assets/` : feuille de style, QR SVG, affiche PDF imprimable.
- `data/` : sources et affirmations minimales vérifiables.

Aucun compte, formulaire de collecte, analytics, cookie applicatif ni générateur QR tiers. Les traitements techniques éventuels de GitHub Pages relèvent de l'hébergeur et ne sont pas masqués.

**Frontière** : aucune correspondance privée, donnée personnelle d'allocataire, capture d'écran personnelle ou pièce issue d'un dossier individuel n'est publiée ici. La recherche générale est gouvernée séparément ; aucun identifiant de dossier privé n'est exposé.

**Conception collaborative :** initiative éditoriale Muse-IRS, assistance de rédaction et de développement ChatGPT ; responsabilité éditoriale et choix de publication humains.

## Audits documentaires des sites — 25 septembre 2026

[Sommaire des six pages](audit-technique-sites.html) · [Département de l’Ardèche](audit-technique-departement.html) · [Capévol](audit-technique-capevol.html) · [Pollen SCOP](audit-technique-pollen.html) · [CréaGestion](audit-technique-creagestion.html) · [Ambition ESS et Ambition Travail 07](audit-technique-ambitions.html).

Les pages distinguent déclarations des éditeurs et sources primaires vérifiées des informations issues du rapport Perplexity. Le site public ne détaille aucun point d'entrée de base de prospects ni aucun dossier individuel ; toute vérification technique nécessitant une administration est réservée à l'exploitant.

## Contrôles de publication

Le validateur `python tools/validate.py`, exécuté par GitHub Actions sur `main` et `gh-pages`, vérifie les pages, les liens locaux, les identifiants des sources, le sitemap, les URL canoniques, les ressources QR/PDF et des invariants élémentaires de confidentialité. Ces contrôles statiques ne remplacent **pas** un audit de sécurité, d'accessibilité ou une consultation HTTP indépendante du site effectivement servi. En cas d'impossibilité de lecture externe, le statut reste `CDN_HTTP_UNVERIFIED`.
