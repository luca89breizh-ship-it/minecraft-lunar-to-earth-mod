# Lunaire — mod Minecraft 26.3 (Fabric)

Échoué sur la Lune : survie, serre, électrolyse, fusée, retour à la maison.

## Jouer
1. Mettez le `.jar` (téléchargé depuis GitHub Actions) dans le dossier `mods` + Fabric API.
2. Créer un monde → **Plus d'options du monde** → Type de monde : **Lunaire (la Lune)**.
3. Vous apparaissez dans les débris de la capsule : le coffre contient l'épurateur endommagé.

## Contenu
- Monde lunaire : ciel noir étoilé, soleil, pas de nuages, gravité /6, relief, régolithe, roche lunaire
- Minerais : fer lunaire, titane, aluminium, glace lunaire
- Structures : capsule de départ, laboratoires abandonnés, temples enfouis (schéma de fusée Tier 3)
- Survie : jauge d'O₂, bouteilles, électrolyseur (glace → O₂), panneaux solaires (jour) /
  générateur à hydrogène (cellules), radiateur, Scelleur d'atmosphère (pièce étanche), régolithe hydratée (serre)
- Brûlure en plein jour sans combinaison, gel la nuit sans radiateur
- Créatures : Sélénites de l'Ombre (groupes, brûlent au soleil), Golems de poussière (neutres, éclats de météorite)
- Fusée : Plateforme de lancement + Module de rentrée + schéma → compte à rebours 10 s, tremblement, chute en parachute

## Compiler
`python3 tools/gen_all.py` (génère textures/données/structures) puis `./gradlew -p fabric build` (JDK 25).
GitHub Actions fait les deux automatiquement.
