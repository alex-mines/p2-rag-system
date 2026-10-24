# Ingest report

Written by `uv run p2 ingest`.
It lists every document in this corpus that ingest added, with what the cleaning pass did and anything that looks wrong.
Running ingest again adds to the table and replaces the "last run" section, and `uv run p2 ingest --report` rewrites it for the documents in docs/ now, after you removed some.

## Summary

- Documents: 209 (the final check needs at least 200)
- Words: 437,176
- Estimated tokens (words times 1.4): 612,046 (`p2 check` warns above 800,000 and fails above 1,000,000)
- Flagged documents: 6

## Documents

| docid | words | characters per page | flags | cleaning |
|---|---:|---:|---|---|
| `ds955__p001-005` | 419 | 894 | - | 6 running line(s) removed |
| `ds955__p006-010` | 1,835 | 2507 | - | 6 running line(s) removed |
| `ds955__p011-015` | 1,409 | 1940 | - | 6 running line(s) removed |
| `ds955__p016-020` | 2,012 | 2768 | - | 6 running line(s) removed |
| `ds955__p021-025` | 505 | 646 | - | 6 running line(s) removed |
| `ds955__p026-030` | 311 | 337 | scanned-looking (337 characters per page, under 400) | 6 running line(s) removed |
| `ds955__p031-035` | 320 | 350 | scanned-looking (350 characters per page, under 400) | 6 running line(s) removed |
| `ds955__p036-040` | 315 | 340 | scanned-looking (340 characters per page, under 400) | 6 running line(s) removed |
| `ds955__p041-045` | 1,148 | 1366 | - | 6 running line(s) removed |
| `ds955__p046-051` | 1,115 | 1150 | - | 6 running line(s) removed |
| `fs20133047` | 3,543 | 3897 | - | - |
| `fs20173002` | 2,124 | 2376 | - | reference list dropped, 2,219 characters (heading) |
| `fs20233005` | 2,791 | 4780 | - | - |
| `fs20233017` | 2,379 | 2854 | - | - |
| `fs20253006` | 2,556 | 3034 | - | 1 running line(s) removed |
| `fs20253008` | 2,364 | 4344 | - | - |
| `fs20253036` | 2,700 | 4715 | - | - |
| `fs20253039` | 2,198 | 3836 | - | - |
| `fs24296` | 1,005 | 3347 | - | - |
| `ofr20131259__p001-005` | 1,240 | 2036 | - | 1 running line(s) removed |
| `ofr20131259__p006-010` | 3,135 | 3864 | - | 1 running line(s) removed |
| `ofr20131259__p011-015` | 961 | 1288 | - | 1 running line(s) removed |
| `ofr20131259__p016-020` | 190 | 240 | scanned-looking (240 characters per page, under 400) | 1 running line(s) removed |
| `ofr20131259__p021-025` | 150 | 183 | scanned-looking (183 characters per page, under 400) | 1 running line(s) removed |
| `ofr20131259__p026-030` | 192 | 243 | scanned-looking (243 characters per page, under 400) | 1 running line(s) removed |
| `ofr20131259__p031-034` | 1,274 | 1736 | - | 1 running line(s) removed |
| `ofr20141158__p001-005` | 1,127 | 1873 | - | 1 running line(s) removed |
| `ofr20141158__p006-010` | 2,236 | 2987 | - | 1 running line(s) removed |
| `ofr20141158__p011-015` | 1,610 | 2110 | - | 1 running line(s) removed |
| `ofr20141158__p016-020` | 1,800 | 2573 | - | 1 running line(s) removed |
| `ofr20211078__p001-005` | 515 | 731 | - | 1 running line(s) removed |
| `ofr20211078__p006-010` | 1,126 | 2261 | - | 1 running line(s) removed |
| `ofr20211078__p011-015` | 2,662 | 3476 | - | 1 running line(s) removed |
| `ofr20211078__p016-020` | 2,837 | 3694 | - | 1 running line(s) removed |
| `ofr20211078__p021-025` | 3,046 | 3884 | - | 1 running line(s) removed |
| `ofr20211078__p026-030` | 3,214 | 4151 | - | 1 running line(s) removed |
| `ofr20211078__p031-035` | 2,087 | 2611 | - | 1 running line(s) removed |
| `ofr20211078__p036-040` | 2,660 | 3444 | - | 1 running line(s) removed |
| `ofr20211078__p041-045` | 3,559 | 4835 | - | 1 running line(s) removed |
| `ofr20211078__p046-048` | 1,127 | 2785 | - | 1 running line(s) removed |
| `ofr20251009__p001-005` | 400 | 943 | - | 1 running line(s) removed |
| `ofr20251009__p006-010` | 2,712 | 3606 | - | 1 running line(s) removed |
| `ofr20251009__p011-015` | 3,198 | 4376 | - | 1 running line(s) removed |
| `ofr20251009__p016-020` | 1,708 | 2457 | - | 1 running line(s) removed |
| `sir20125003__p001-005` | 548 | 1350 | - | 1 running line(s) removed |
| `sir20125003__p006-010` | 1,922 | 2550 | - | 1 running line(s) removed |
| `sir20125003__p011-015` | 365 | 485 | - | 1 running line(s) removed |
| `sir20125003__p016-020` | 3,493 | 4425 | - | 1 running line(s) removed |
| `sir20125003__p021-025` | 1,952 | 2455 | - | 1 running line(s) removed |
| `sir20125003__p026-030` | 2,608 | 3523 | - | 1 running line(s) removed |
| `sir20125003__p031-035` | 1,592 | 2217 | - | 1 running line(s) removed |
| `sir20125003__p036-040` | 1,171 | 1515 | - | 1 running line(s) removed |
| `sir20125220__p001-005` | 897 | 1277 | - | - |
| `sir20125220__p006-010` | 1,588 | 2906 | - | - |
| `sir20125220__p011-015` | 3,662 | 4891 | - | - |
| `sir20125220__p016-020` | 2,723 | 3504 | - | - |
| `sir20125220__p021-025` | 2,216 | 2686 | - | - |
| `sir20125220__p026-030` | 2,859 | 3468 | - | - |
| `sir20125220__p031-035` | 3,015 | 3917 | - | - |
| `sir20125220__p036-040` | 2,013 | 2592 | - | - |
| `sir20125220__p041-045` | 2,845 | 4067 | - | - |
| `sir20125220__p046-051` | 878 | 894 | - | - |
| `sir20125252__p001-005` | 554 | 1398 | - | 3 running line(s) removed |
| `sir20125252__p006-010` | 1,444 | 2244 | - | 3 running line(s) removed |
| `sir20125252__p011-015` | 3,007 | 3883 | - | 3 running line(s) removed |
| `sir20125252__p016-020` | 1,854 | 2412 | - | 3 running line(s) removed |
| `sir20125252__p021-025` | 3,361 | 4126 | - | 3 running line(s) removed |
| `sir20125252__p026-030` | 1,505 | 1896 | - | 3 running line(s) removed |
| `sir20125252__p031-035` | 1,439 | 1763 | - | 3 running line(s) removed |
| `sir20125252__p036-040` | 1,539 | 1898 | - | 3 running line(s) removed |
| `sir20125252__p041-045` | 1,456 | 1822 | - | 3 running line(s) removed |
| `sir20125252__p046-050` | 2,913 | 3504 | - | 3 running line(s) removed |
| `sir20125252__p051-055` | 1,554 | 1896 | - | 3 running line(s) removed |
| `sir20125252__p056-060` | 1,482 | 1823 | - | 3 running line(s) removed |
| `sir20125252__p061-064` | 2,133 | 3648 | - | 3 running line(s) removed |
| `sir20125255__p001-005` | 447 | 1543 | - | 2 running line(s) removed |
| `sir20125255__p006-010` | 902 | 1508 | - | 2 running line(s) removed |
| `sir20125255__p011-015` | 3,664 | 4763 | - | 2 running line(s) removed |
| `sir20125255__p016-020` | 3,180 | 4255 | - | 2 running line(s) removed |
| `sir20125255__p021-025` | 3,652 | 4191 | - | 2 running line(s) removed |
| `sir20125255__p026-030` | 3,937 | 3976 | - | 2 running line(s) removed |
| `sir20125255__p031-035` | 2,841 | 3126 | - | 2 running line(s) removed |
| `sir20125255__p036-040` | 2,272 | 2360 | - | 2 running line(s) removed |
| `sir20125255__p041-045` | 2,889 | 3632 | - | 2 running line(s) removed |
| `sir20125255__p046-050` | 4,085 | 4672 | - | 2 running line(s) removed |
| `sir20125255__p051-055` | 3,971 | 4573 | - | 2 running line(s) removed |
| `sir20125255__p056-060` | 3,768 | 4316 | - | 2 running line(s) removed |
| `sir20125255__p061-065` | 2,567 | 3228 | - | 2 running line(s) removed |
| `sir20125255__p066-070` | 2,438 | 3097 | - | 2 running line(s) removed |
| `sir20125255__p071-075` | 3,287 | 3578 | - | 2 running line(s) removed |
| `sir20125255__p076-080` | 3,743 | 4967 | - | 2 running line(s) removed |
| `sir20125255__p081-085` | 1,229 | 1774 | - | 2 running line(s) removed |
| `sir20145095__p001-005` | 548 | 1764 | - | 1 running line(s) removed |
| `sir20145095__p006-010` | 1,637 | 3142 | - | 1 running line(s) removed |
| `sir20145095__p011-015` | 2,888 | 3943 | - | 1 running line(s) removed |
| `sir20145095__p016-020` | 2,932 | 3972 | - | 1 running line(s) removed |
| `sir20145095__p021-025` | 2,933 | 4020 | - | 1 running line(s) removed |
| `sir20145095__p026-030` | 2,620 | 3251 | - | 1 running line(s) removed |
| `sir20145095__p031-035` | 3,539 | 4598 | - | 1 running line(s) removed |
| `sir20145095__p036-040` | 3,219 | 4052 | - | 1 running line(s) removed |
| `sir20145095__p041-045` | 2,003 | 2426 | - | 1 running line(s) removed |
| `sir20145095__p046-050` | 2,363 | 3190 | - | 1 running line(s) removed |
| `sir20145095__p051-055` | 3,287 | 4378 | - | 1 running line(s) removed |
| `sir20145095__p056-060` | 1,933 | 2738 | - | 1 running line(s) removed |
| `sir20145095__p061-065` | 2,180 | 2297 | - | 1 running line(s) removed |
| `sir20145095__p066-070` | 1,645 | 2269 | - | 1 running line(s) removed |
| `sir20145095__p071-074` | 576 | 1040 | - | 1 running line(s) removed |
| `sir20165134__p001-005` | 463 | 1435 | - | 1 running line(s) removed |
| `sir20165134__p006-010` | 1,500 | 3201 | - | 1 running line(s) removed |
| `sir20165134__p011-015` | 3,200 | 4471 | - | 1 running line(s) removed |
| `sir20165134__p016-020` | 2,515 | 3442 | - | 1 running line(s) removed |
| `sir20165134__p021-025` | 2,423 | 3247 | - | 1 running line(s) removed |
| `sir20165134__p026-030` | 3,024 | 4022 | - | 1 running line(s) removed |
| `sir20165134__p031-035` | 2,290 | 2800 | - | 1 running line(s) removed |
| `sir20165134__p036-040` | 2,186 | 2928 | - | 1 running line(s) removed |
| `sir20165134__p041-045` | 3,134 | 4067 | - | 1 running line(s) removed |
| `sir20165134__p046-050` | 2,728 | 3430 | - | 1 running line(s) removed |
| `sir20165134__p051-055` | 1,426 | 1962 | - | 1 running line(s) removed |
| `sir20165134__p056-060` | 2,053 | 2869 | - | 1 running line(s) removed |
| `sir20165134__p061-065` | 2,677 | 3389 | - | 1 running line(s) removed |
| `sir20165134__p066-070` | 2,954 | 3777 | - | 1 running line(s) removed |
| `sir20165134__p071-075` | 3,405 | 4665 | - | 1 running line(s) removed |
| `sir20165134__p076-080` | 3,198 | 4632 | - | 1 running line(s) removed |
| `sir20165134__p081-085` | 1,158 | 1443 | - | 1 running line(s) removed |
| `sir20165134__p086-090` | 813 | 1014 | - | 1 running line(s) removed |
| `sir20175015__p001-005` | 464 | 1554 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p006-010` | 1,088 | 2010 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p011-015` | 2,664 | 3551 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p016-020` | 3,774 | 5081 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p021-025` | 2,536 | 3261 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p026-030` | 2,003 | 2578 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p031-035` | 1,298 | 1730 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p036-040` | 2,031 | 2514 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p041-045` | 1,479 | 1669 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p046-050` | 1,968 | 2606 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p051-055` | 723 | 959 | - | reference list dropped, 21,874 characters (heading) |
| `sir20175015__p056-060` | 1,496 | 2346 | - | reference list dropped, 21,874 characters (heading) |
| `sir20195049__p001-005` | 331 | 473 | - | 1 running line(s) removed |
| `sir20195049__p006-010` | 2,446 | 4207 | - | 1 running line(s) removed |
| `sir20195049__p011-015` | 2,436 | 3246 | - | 1 running line(s) removed |
| `sir20195049__p016-020` | 3,407 | 4375 | - | 1 running line(s) removed |
| `sir20195049__p021-025` | 1,718 | 2208 | - | 1 running line(s) removed |
| `sir20195049__p026-030` | 2,904 | 3603 | - | 1 running line(s) removed |
| `sir20195049__p031-034` | 2,364 | 4099 | - | 1 running line(s) removed |
| `sir20215066__p001-005` | 426 | 605 | - | 1 running line(s) removed |
| `sir20215066__p006-010` | 907 | 2214 | - | 1 running line(s) removed |
| `sir20215066__p011-015` | 3,531 | 4743 | - | 1 running line(s) removed |
| `sir20215066__p016-020` | 3,399 | 4514 | - | 1 running line(s) removed |
| `sir20215066__p021-025` | 3,681 | 4723 | - | 1 running line(s) removed |
| `sir20215066__p026-030` | 2,232 | 2759 | - | 1 running line(s) removed |
| `sir20215066__p031-035` | 2,681 | 3441 | - | 1 running line(s) removed |
| `sir20215066__p036-040` | 3,025 | 3877 | - | 1 running line(s) removed |
| `sir20215066__p041-045` | 3,937 | 5497 | - | 1 running line(s) removed |
| `sir20215066__p046-048` | 264 | 652 | - | 1 running line(s) removed |
| `sir20215070__p001-005` | 628 | 1460 | - | 1 running line(s) removed |
| `sir20215070__p006-010` | 1,720 | 2463 | - | 1 running line(s) removed |
| `sir20215070__p011-015` | 2,690 | 3485 | - | 1 running line(s) removed |
| `sir20215070__p016-020` | 2,752 | 3521 | - | 1 running line(s) removed |
| `sir20215070__p021-025` | 2,816 | 4018 | - | 1 running line(s) removed |
| `sir20215070__p026-030` | 1,526 | 1716 | - | 1 running line(s) removed |
| `sir20215070__p031-034` | 338 | 506 | - | 1 running line(s) removed |
| `sir20225023__p001-005` | 573 | 1309 | - | 1 running line(s) removed |
| `sir20225023__p006-010` | 2,055 | 2764 | - | 1 running line(s) removed |
| `sir20225023__p011-015` | 2,099 | 2650 | - | 1 running line(s) removed |
| `sir20225023__p016-020` | 1,921 | 2475 | - | 1 running line(s) removed |
| `sir20225023__p021-026` | 1,886 | 2206 | - | 1 running line(s) removed |
| `sir20225061__p001-005` | 402 | 568 | - | 1 running line(s) removed |
| `sir20225061__p006-010` | 1,122 | 2377 | - | 1 running line(s) removed |
| `sir20225061__p011-015` | 2,841 | 3806 | - | 1 running line(s) removed |
| `sir20225061__p016-020` | 2,601 | 3448 | - | 1 running line(s) removed |
| `sir20225061__p021-025` | 2,129 | 2782 | - | 1 running line(s) removed |
| `sir20225061__p026-030` | 3,251 | 4095 | - | 1 running line(s) removed |
| `sir20225061__p031-035` | 2,113 | 2652 | - | 1 running line(s) removed |
| `sir20225061__p036-040` | 1,422 | 1772 | - | 1 running line(s) removed |
| `sir20225061__p041-045` | 2,108 | 2667 | - | 1 running line(s) removed |
| `sir20225061__p046-050` | 3,072 | 4134 | - | 1 running line(s) removed |
| `sir20225061__p051-056` | 1,799 | 2149 | - | 1 running line(s) removed |
| `sir20225085__p001-005` | 305 | 456 | - | 1 running line(s) removed |
| `sir20225085__p006-010` | 1,825 | 2689 | - | 1 running line(s) removed |
| `sir20225085__p011-015` | 2,212 | 3094 | - | 1 running line(s) removed |
| `sir20225085__p016-020` | 1,442 | 1968 | - | 1 running line(s) removed |
| `sir20225085__p021-026` | 1,188 | 1436 | - | 1 running line(s) removed |
| `sir20235119__p001-005` | 646 | 1568 | - | 1 running line(s) removed |
| `sir20235119__p006-010` | 2,255 | 3447 | - | 1 running line(s) removed |
| `sir20235119__p011-015` | 2,966 | 4111 | - | 1 running line(s) removed |
| `sir20235119__p016-020` | 2,564 | 3450 | - | 1 running line(s) removed |
| `sir20235119__p021-025` | 2,907 | 3838 | - | 1 running line(s) removed |
| `sir20235119__p026-030` | 2,022 | 2818 | - | 1 running line(s) removed |
| `sir20235119__p031-035` | 2,459 | 3239 | - | 1 running line(s) removed |
| `sir20235119__p036-040` | 1,992 | 2601 | - | 1 running line(s) removed |
| `sir20235119__p041-045` | 1,264 | 1690 | - | 1 running line(s) removed |
| `sir20235119__p046-050` | 2,718 | 3860 | - | 1 running line(s) removed |
| `sir20235119__p051-054` | 1,943 | 3593 | - | 1 running line(s) removed |
| `sir20235145__p006-010` | 2,034 | 2879 | - | 1 running line(s) removed |
| `sir20235145__p011-015` | 3,736 | 5099 | - | 1 running line(s) removed |
| `sir20235145__p016-020` | 3,286 | 4382 | - | 1 running line(s) removed |
| `sir20235145__p021-025` | 2,554 | 3528 | - | 1 running line(s) removed |
| `sir20235145__p026-030` | 1,821 | 2341 | - | 1 running line(s) removed |
| `sir20235145__p031-035` | 3,257 | 4556 | - | 1 running line(s) removed |
| `sir20235145__p036-040` | 3,499 | 4983 | - | 1 running line(s) removed |
| `sir20235145__p041-042` | 423 | 1506 | - | 1 running line(s) removed |
| `wri20014022__p001-005` | 806 | 1149 | - | 1 running line(s) removed |
| `wri20014022__p006-010` | 1,902 | 3461 | - | 1 running line(s) removed |
| `wri20014022__p011-015` | 2,295 | 2983 | - | 1 running line(s) removed |
| `wri20014022__p016-020` | 2,646 | 3344 | - | 1 running line(s) removed |
| `wri20014022__p021-025` | 2,397 | 2904 | - | 1 running line(s) removed |
| `wri20014022__p026-030` | 1,777 | 2459 | - | 1 running line(s) removed |
| `wri20014022__p031-035` | 1,784 | 1828 | - | 1 running line(s) removed |
| `wri20014022__p036-040` | 1,809 | 1874 | - | 1 running line(s) removed |

## Not added in the last run

Nothing was left out.

## What to check by eye

Ingest cleans text by rules, and rules miss things.
Take five minutes to open the shortest, a middle one and the longest document next to its original and read one page of each.

- Search the documents for `þ`, `¼`, `(cid:` and the replacement character.
  A hit usually means the PDF's font map is wrong, which no tool can repair, so treat it as a defect and leave that document out.
- Look at the end of a few papers.
  Ingest drops a trailing reference list when it finds a References heading or a run of numbered entries.
  A paper whose list has neither can keep it, and then every author and journal name matches queries it should not.
- Open the first lines of a few documents.
  Author lists, copyright pages and tables of contents are not removed automatically, and you may want to cut them.
- Compare one table with the PDF.
  A PDF prints footnote marks as small raised digits, and the converter glues them onto the word or number next to them: `ALUMINUM1` is the heading ALUMINUM with footnote 1, and `11210,000` can be 210,000 with footnote 11.
  Quotes still match the stored text, but a number read from it can be wrong, so check before you trust a figure in a query, a judgment or an answer.
- Fix the `license` column in the manifest for every document, then run `uv run p2 license`.
  It is `unknown` until you do, and `unknown` does not pass.

## If a document is flagged as scanned

A scan is a picture of a page, so there is no text for ingest to read.
This template does not install an OCR tool, because it is large and most students never need it.
If you do need one, the opt-in route is pymupdf4llm with rapidocr, run on its own outside the template's environment:

```
uv run --no-project --with pymupdf4llm --with rapidocr python -c "import pymupdf4llm, sys, pathlib; pathlib.Path(sys.argv[2]).write_text(pymupdf4llm.to_markdown(sys.argv[1], use_ocr=True, force_ocr=True), encoding='utf-8')" scan.pdf scan.md
```

Put the resulting `.md` file in your folder and ingest the folder again.
It costs about 2 seconds a page, and OCR text needs a second look: it misreads ligatures, hyphens and numbers.
pymupdf4llm is AGPL-3.0 software, so use it only as a tool on your own machine, and do not add it to this repo's dependencies or copy its code into the repo.
