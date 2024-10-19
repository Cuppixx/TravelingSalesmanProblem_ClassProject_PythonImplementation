# Result Set 2

## Fragestellung

_Welche der drei EA Konfigurationen hat die kürzesten Rundreisen finden können?_

**Assumption for:**

- mutation_prob = 50%
- min_k = population_size / 4
- population_size = 20
- max_generation = 5000

**The average- and min length accordingly for:**

| EA Config  | Average length  | Min length  |
| ---------- | --------------- | ----------- |
| ox  and swap_mutation        | 17870.0     | 15476 |
| ox  and inversion_mutation   | 18750.2     | 14944 |
| pmx and swap_mutation        | 15468.7     | 13197 |
| pmx and inversion_mutation   | 17279.9     | 13353 |

Die kürzeste Rundreise hat die EA Konfiguration aus pmx und swap_mutation gefunden.
Die selbe Konfiguration ist zudem auch im durchschnitt die beste Wahl.

**Interessant:**
Obwohl die Konfiguration aus ox und inversion_mutation die schlechtesten Touren im durchschnitt findet
hat die Konfiguration dennoch eine äußerst gute Lösung gefunden.
Nach mehrmaligem testen scheint das jedoch nur zufall gewesen zu sein.
Ähnliches gilt für die Konfiguration pmx and inversion_mutation, die zweit-beste Konfiguration im durchschnitt.

## EA Konfiguration

Aus den Erkentnissen wird die Konfiguration pmx and swap_mutation als basis gewählt,
da diese die im durchschnitt besten Lösungen liefert und
(auch wenn nur knapp) die beste Lösung aller Kombinationen gefunden hat.
Auf der EA Konfiguration werden nun mutation_prob; min_k; population_size; max_generation
schrittweise angepasst um besser Ergbnisse zu erziehlen.
Die Einstellung für gute (nicht zwangsweise für beste) durchschnitts-werte
wird für den nächsten schritt beibehalten.
Bsp. Schritt 2. min_k arbeitet weiter / wurde getestet mit der mutation_prob = 25%.

1. mutation_prob durchschnitt mit:
    - 00% --> 25906.7
    - 20% --> 11158.5
    - 25% --> 11673.0 <-- Selected
    - 50% --> 15468.7
    - 75% --> 20670.8

2. min_k durchschnitt mit:
    - population_size / 6 --> 22113.3
    - population_size / 4 --> 11673.0
    - population_size / 2 -->  8559.4 <-- Selected
    - population_size / 1 -->  8288.3

3. population_size durchschnitt mit:
    - 20 --> 8559.4
    - 30 --> 8405.9 <-- Selected
    - 40 --> 8257.7

4. max_generation durchschnitt mit:
    - 3 500 --> 8418.3 <-- Selected
    - 5 000 --> 8405.9

    _3.500 hat eine laufzeit (ca. 20sec) die bei mehrfachem testen auszuhalten ist und einen vernachlässigbaren abfall beim durchschnitt._

    - 10 000 --> takes too long for me to even care
    - 20 000 --> takes too long for me to even care
    - 40 000 --> takes too long for me to even care
    - 80 000 --> takes too long for me to even care

---

Mit den werten:

- mutation_prob = 25%
- min_k = population_size / 2
- population_size = 30
- max_generation = 3500

wird nun die bestresults.txt gefüllt und das beste Ergbniss gesucht:

**best solution found:** 7542
