# Lunaire — mod Minecraft 26.3 (Fabric + Forge)

Échoué sur la Lune : survie, serre, électrolyse, fusée, retour à la maison.

> **État : base de projet NON compilée.** Elle a été écrite sans accès aux dépôts Maven
> (Fabric / Forge), donc aucune compilation n'a pu être testée. Les versions ont été vérifiées,
> mais les noms d'API 26.3 et le `build.gradle` Forge peuvent demander de petits ajustements
> (voir « Si ça ne compile pas »).

## Versions ciblées

| Élément | Fabric | Forge |
|---|---|---|
| Minecraft | 26.3 (non obfusqué, sans mappings) | 26.3 |
| Java | 25 | 25 |
| Gradle | 9.6.0 (wrapper fourni) | 9.6.0 |
| Outil de build | Fabric Loom 1.17 (`net.fabricmc.fabric-loom`) | ForgeGradle 7 (`net.minecraftforge.gradle`) |
| Loader | Fabric Loader 0.19.5 | Forge 26.3-66.1.0 |
| API | Fabric API 0.165.0+26.3 | — |

## Structure

```
common/   code Java + assets + data partagés (blocs, items, textures, langues, loot, tags)
fabric/   build Fabric + point d'entrée LunaireFabric
forge/    build Forge  + point d'entrée LunaireForge, mods.toml, pack.mcmeta
tools/    generate_assets.py : régénère JSON + textures provisoires
```

Les deux builds sont indépendants (deux projets Gradle) et lisent `common/` comme dossier source,
ce qui évite les conflits de dépôts entre Loom et ForgeGradle. Un seul wrapper à la racine sert aux deux.

## Compiler

Il faut un JDK 25.

```bash
./gradlew -p fabric build     # -> fabric/build/libs/lunaire-fabric-26.3-0.1.0.jar
./gradlew -p forge build      # -> forge/build/libs/lunaire-forge-26.3-0.1.0.jar
./gradlew -p fabric runClient # lancer le jeu en dev
./gradlew -p forge runClient
```

Sans JDK 25 en local : poussez le dossier sur GitHub, le workflow `.github/workflows/build.yml`
compile les deux loaders et publie les jars.

## Contenu actuel (v0.1.0)

- Blocs : Régolithe (pelle), Roche lunaire (pioche), Glace lunaire (pioche)
- Objets : Épurateur d'air portatif endommagé, Éclat de météorite, Circuit imprimé, Morceau de fer
- Onglets créatifs : Blocs de construction, Ingrédients
- Textures 16x16 provisoires (à remplacer), traductions FR/EN, loot tables, tags de minage

## Si ça ne compile pas

1. **Forge** : comparez `forge/build.gradle` avec le MDK officiel 26.3-66.1.0
   (https://files.minecraftforge.net/net/minecraftforge/forge/index_26.3.html). Le bloc `repositories`,
   `minecraft.runs` et `minecraft.dependency(...)` est reconstitué d'après ForgeGradle 7.
2. **Noms Mojang** : `Identifier` (ex-`ResourceLocation`), `Item.Properties#setId`,
   `useBlockDescriptionPrefix`. Si une classe est introuvable, regardez les imports du projet d'exemple
   de votre loader.
3. **Loom** : si `1.17-SNAPSHOT` est refusé, essayez la version indiquée dans le template Fabric
   (https://fabricmc.net/develop/template/).
4. **pack.mcmeta** (Forge) : format 121 pour 26.3.

Envoyez-moi l'erreur exacte et je corrige.

## Feuille de route (d'après le plan de jeu)

Statut : ✅ fait · ⬜ à faire

**Étape 1 — Âge de pierre lunaire**
- ✅ Régolithe, Roche lunaire, Glace lunaire, épurateur endommagé
- ⬜ Dimension Lune (gravité /6, pas d'atmosphère, sons étouffés à 80 %)
- ⬜ Spawn dans une capsule de sauvetage (coffre avec l'épurateur)
- ⬜ Cratères sombres avec glace lunaire
- ⬜ Bloc Scelleur d'atmosphère + serre (régolithe hydraté + pousse d'arbre)

**Étape 2 — Systèmes centraux**
- ⬜ Jauge d'O₂ (HUD) + asphyxie sans équipement
- ⬜ Électrolyseur (glace → O₂ pour les bouteilles)
- ⬜ Énergie : panneaux solaires (jour/nuit), générateur à hydrogène
- ⬜ Chaleur de jour (brûlures) / gel de nuit (radiateur)

**Étape 3 — Faune, flore, exploration**
- ⬜ Sélénites de l'Ombre (hostiles, brûlent au soleil), Golems de poussière (neutres, éclats de météorite)
- ⬜ Laboratoires abandonnés (circuits, fer), Temples enfouis (schémas fusée Tier 3)

**Étape 4 — Retour à la maison**
- ⬜ Tier 1 : outils en roche lunaire, première serre, autonomie en eau
- ⬜ Tier 2 : combinaison renforcée, Titane/Aluminium, automatisation de l'O₂
- ⬜ Tier 3 : Plateforme de lancement, Module de rentrée, compte à rebours 10 s, tremblement d'écran, chute en parachute dans l'Overworld

Chaque brique de gameplay sera écrite dans `common/` pour rester identique sur Fabric et Forge ;
seuls les points d'entrée et les événements propres à chaque loader vivent dans `fabric/` et `forge/`.
