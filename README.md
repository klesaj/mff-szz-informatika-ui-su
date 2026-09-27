# Bakalářské státnice z informatiky na MFF UK

Studijní materiály k bakalářské státní závěrečné zkoušce (SZZ) studijního programu Informatika na
Matematicko-fyzikální fakultě UK. Pokrývají **společnou část** (matematika a informatika) a specializaci
**Umělá inteligence, zaměření Strojové učení**. Rozsah odpovídá požadavkům platným v roce 2026.

**PDF ke čtení: <https://klesaj.github.io/mff-szz-informatika-ui-su/>**

## Co tu je

Ke každému okruhu dva dokumenty:

- **Výklad:** definice, věty, intuice, řešené příklady a obrázky podle oficiálních požadavků ke zkoušce.
  Na konci je seznam použitých zdrojů (skripta a slidy přednášejících, učebnice).
- **Příklady otázek:** reálné otázky SZZ z let 2022 až 2026 přepsané z PDF zveřejněných fakultou,
  s oficiálním náčrtem řešení, kde existuje. Kde náčrt chybí, je doplněno vlastní vzorové řešení
  (zřetelně označené), vlastní doplňující vysvětlení jsou oddělená od oficiálního textu.

| Skupina | Okruhy |
|---|---|
| Matematika | M1 Diferenciální a integrální počet, M2 Algebra a lineární algebra, M3 Diskrétní matematika, M4 Teorie grafů, M5 Pravděpodobnost a statistika, M6 Logika |
| Informatika | I1 Automaty a jazyky, I2 Algoritmy a datové struktury, I3 Programovací jazyky (C++), I4 Architektura počítačů a operačních systémů |
| Specializace UI, Strojové učení | S1 Základy umělé inteligence, S3 Strojové učení |

Závazné znění požadavků je vždy na
[webu MFF](https://www.mff.cuni.cz/cs/studenti/bakalarske-studium/statni-zaverecne-zkousky/bakalarske-statni-zkousky-studijniho-programu-informatika).

## Jak materiály vznikly

Materiály vznikly s výraznou pomocí AI (Claude od Anthropicu). Postup: výklad podle oficiálních požadavků
a zdrojů přednášejících, opakovaný fact-check (numerické výpočty ověřené skripty, konstrukce a protipříklady
ověřené programem), samostatná revize každého okruhu a nezávislá kontrola provedených oprav. Z materiálů
se připravilo několik lidí, kteří SZZ úspěšně složili.

I tak mohou obsahovat chyby. Pokud nějakou najdete, založte prosím issue (ideálně s číslem strany a okruhem),
případně rovnou pull request.

## Sestavení

LuaLaTeX a latexmk (TeX Live). Výstup jde do `<okruh>/out/`, pomocné soubory do `<okruh>/tmp/`.

```bash
./build.sh all                                         # všechny okruhy
./build.sh 03_specializace_ui_su/S3_strojove_uceni     # jeden výklad
./build.sh 03_specializace_ui_su/S3_strojove_uceni/priklady
```

Na Windows `build.ps1` se stejnými argumenty. Sdílené styly jsou v `common_latex/`.
GitHub Actions při každém pushi na `main` sestaví všechna PDF a nasadí je na GitHub Pages.

Autor: Jakub Klesa
