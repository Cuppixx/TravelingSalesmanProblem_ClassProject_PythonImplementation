# Result Set 1

| n  | Len  | Rechenzeit [sec]    | Len  | Len  | Len  | Len  | Len  | Rundreise | Rechenzeit [sec]     | Len  | Len  | Len  | Len  | Len  | Rechenzeit [sec] | Rundreise |
|----|------|---------------------|------|------|------|------|------|-----------|----------------------|------|------|------|------|------|------------------|-----------|
| 5  |  778 | 0 .000215           |  778 |  778 |  805 | 1159 |  805 | 18.0      | 3.90800181e-05       |  778 |  778 |  778 |  778 |  778 | 0.053252499969   | 11508     |
| 6  | 1140 | 0 .000881           | 1141 | 1140 | 1159 | 1159 | 1167 | 27.8      | 6.43000006e-05       | 1140 | 1140 | 1140 | 1140 | 1140 | 0.057989539974   | 11508     |
| 7  | 1934 | 0 .007182           | 1950 | 1934 | 1934 | 2091 | 1976 | 35.0      | 7.22000841e-05       | 1934 | 1934 | 1934 | 1934 | 1934 | 0.057086660014   | 11508     |
| 8  | 2030 | 0 .045710           | 2044 | 2229 | 2030 | 2670 | 2087 | 86.6      | 0.000120699987       | 2030 | 2030 | 2030 | 2030 | 2030 | 0.058352959994   | 11508     |
| 9  | 2123 | 0 .452157           | 2123 | 2123 | 2178 | 2123 | 2445 | 109.6     | 0.000244459998       | 2123 | 2123 | 2123 | 2123 | 2123 | 0.059894739952   | 11508     |
| 10 | 2275 | 4 .882488           | 2432 | 2818 | 2607 | 2432 | 2596 | 130.4     | 0.000306859984       | 2275 | 2275 | 2275 | 2275 | 2275 | 0.059558480000   | 11508     |
| 11 | 2370 | 1 min               | 2635 | 2370 | 2691 | 2370 | 2900 | 209.0     | 0.000539260008       | 2370 | 2370 | 2370 | 2370 | 2370 | 0.060838059987   | 11508     |
| 12 | 2409 | 13 min              | 2600 | 2446 | 2575 | 2645 | 2679 | 261.4     | 0.000622700015       | 2409 | 2409 | 2409 | 2409 | 2409 | 0.061583600006   | 11508     |
| 13 | 2511 | 2.8 h               | 3124 | 3171 | 2557 | 2511 | 2741 | 260.2     | 0.000745199969       | 2511 | 2511 | 2511 | 2511 | 2511 | 0.062811879999   | 11508     |
| 14 |      |                     | 3003 | 2754 | 3006 | 2992 | 2952 | 373.8     | 0.001017519994       | 2639 | 2639 | 2639 | 2639 | 2639 | 0.064890959998   | 11508     |
| 15 |      |                     | 2999 | 2985 | 3230 | 3050 | 2945 | 493.4     | 0.001291939988       | 2806 | 2806 | 2806 | 2806 | 2806 | 0.064239860000   | 11508     |
| 16 |      |                     | 3099 | 3403 | 3201 | 3373 | 2940 | 776.8     | 0.002071800013       | 2794 | 2794 | 2794 | 2794 | 2794 | 0.067777460021   | 11508     |

## Fragen

_Könnte Dein “Brute Force” Programm in diesem Jahr die kürzeste Rundreise durch alle Landeshauptstädte berechnen?_

- Ja! Für n = 16 würde das Programm zwischen 5 und 7 Tagen laufen. Die Angabe ist jedoch sehr grob.

---

_Für bekannte kürzeste Rundreisen: Findet 2-opt auch immer die kürzeste Rundreise?_

- Nein! 2-opt findet nicht immer die Optimale Tour (siehe n = 12, n = 10). Durchschnittlich findet 2-opt für 1.333 von 5 Läufen die Optimale Lösung.

---

_Wenn nicht, wie nahe kommt 2-opt an eine beste Lösung?_

- Im durchschnitt kommt 2-opt bei einer von 5 läufen an die Optimal Lösung heran. Jedoch kann sich 2-opt auch um bis zu 500+ Len verschätzen.
Die Fehler scheinen mit zunehmendem n häufiger zu werden. Eventuell da ein größeres n mehr lokale optima mitbringt in denen 2-opt festhängen kann?

---

_Für bekannte kürzeste Rundreisen: Findet SA auch immer die kürzeste Rundreise?_

- Ja! Jedoch stark abhängig vom Abkühlschema

---

_Wenn nicht, wie nahe kommt SA an eine beste Lösung?_

-

---

_Nimmt die Rechenzeit von SA mit größer werdenden n zu?_

- Ja! Die Rechenzeit nimmt durchschnittlich um 0.00119 sekunden mit jedem n zu.

---

_Ist Deine SA Implementierung schneller als 2-opt?_

- Für das Implementierte Abkühlschema nein. Für ungenauere Abkühlschema ja. Zudem steigt die Rechenzeit langsammer als für 2-opt.

---

_Erzeugt Dein SA bessere Lösungen als 2-opt?_

- Ja! Jedoch stark abhängig vom Abkühlschema
