# Maintenance checklist

Things to check or fix, found while moving the book from Publisher to this site. Tick an item by
changing `- [ ]` to `- [x]` (on GitHub: open this file, click the pencil, edit, commit). The site's
maintainers page shows this list with progress, and links each card (`0198-mcmenemy`) and page
(`p344`, the original Publisher page) to the site.

The three sections marked "generated" are refreshed from the content files by
`python3 tools/report.py`, which keeps ticks. Everything else is written by hand: add items or notes
anywhere outside the generated sections.

## Needs a decision

- [ ] p342 `1399-footballer`: the name line is a research note ("Although H. Morgan was probably a Grimsby player, research has found no trace..."). The player is presumably H. Morgan; set the name.
- [ ] p285 `1877-three`: "A card anomaly in terms of identification. This image could be one of three." Decide what the card page should say.
- [ ] p958 `1174-`: a heading with no text. The scan reads "A. H. Collins".
- [ ] p964, p965 (Woking): cards with a name and empty birth/death lines only (`1424-shaw`, `2428-crane`).
- [ ] Card 558: given to both `0558-thompson` (p137) and `0558-jones` (p139a), and Thompson's page shows the E. Jones scan. An external checklist gives 558 as E. Jones.
- [ ] p432 `0625-lodge`: listed as Lodge, but the scan reads "J. Barrass" with 625 printed on it.
- [ ] p236 `2318-green`: listed as "F.N.E. Green", but the scan reads "F. N. S. Creek".
- [ ] p761 `2057-foweather`: given 2057, the same as `2057-short`; Foweather's scan shows 1763.
- [ ] p344: Thomas 'Tommy' Talks has a biography but no "Card" heading, so he is not a card yet. His text is at the end of `0941-smith`; his scan is with the Grimsby Town photos.
- [ ] p303: Andrew Nesbit Wilson's biography has no "Card" heading either. His scan shows card 382 with Dunfermline on the front, so he is `0382-wilson-2`, a second version of `0382-wilson` (Middlesbrough, p551). Check the two biographies against each other: they differ in places (e.g. his son's details).
- [ ] p67, p183, p186, p189, p210, p592, p856: one more card scan than cards. The extra scan is with the team's photos; it may be a second version of one of the cards.
- [ ] p144 (Bristol Rovers): a page about 'Tancy' Lea's 1921 Cup Final shirt and programme, shown as team photos and a note. It could become a feature.
- [ ] Copyright: confirm the statement in `COPYRIGHT.md` with Michael Postles.
- [ ] Wikipedia credit: many card biographies are adapted from Wikipedia without naming the article. CC BY-SA asks for credit, so add a source footnote linking the article (as the features have) when checking each card.
- [ ] Unidentified players: the compiler could not trace these and they are notes on the team page. Where the page gives card numbers (p236, p281) they are also name-only cards. p220 Civil Service, p224 Clapton, p236 Corinthians, p281 Dulwich Hamlet, p658 Oxford City, p906 Tufnell Park, p948 West Norwood, p980 Wycombe Wanderers.
- [ ] Unidentified players have numbered cards: the scans on those team pages show card numbers (on Civil Service, numbers in the 2390s and 2400s) and some names differ from the typed list (scan "A. E. Batchelor", typed "A.E.Butcher"; "F. J. Hayns" / "F.J. Haynes"). Decide whether they should be name-only cards on the checklist, as on p236 and p281. On p220, C.W. Harbridge is now card `0146-harbridge-3`, the Civil Service version of card 146.

## Card numbers given to different players (generated)

<!-- generated: conflicts -->
Card numbers given to players with different names (42). Usually a typo in the number or the name; correct the card file, or tick the item if both are right.

- [ ] **119**: `0119-metcalf` (Accrington Stanley, p16a), `0119-osmond` (Clapton Orient, p227), `0119-metcalf-2` (Stockport County, p847), `0119-metcalf-3` (Swindon Town, p875)
- [ ] **123**: `0123-elvey` (Luton Town, p491), `0123-dunn` (Luton Town, p494)
- [ ] **135**: `0135-anderson` (Clyde, p173c), `0135-currie` (Leicester City, p458), `0135-currie-2` (Wigan, p956)
- [ ] **165**: `0165-doran` (Brighton & Hove, p125), `0165-doran-2` (Manchester City, p526), `0165-scott` (St Mirren, p783)
- [ ] **225**: `0225-hugall` (Clapton Orient, p225), `0225-hugall-2` (Hamilton Acc, p351), `0225-o-hagen` (St Mirren, p778)
- [ ] **254**: `0254-neish` (Clydebank, p176), `0254-ellson` (Halifax Town, p410)
- [ ] **272**: `0272-kerr` (Hibernian, p404), `0272-mcnab` (Morton, p508)
- [ ] **344**: `0344-stansfield` (Bristol Rovers, p142), `0344-smith` (Grimsby Town, p345)
- [ ] **433**: `0433-stephenson` (Huddersfield Town, p423), `0433-lyon` (Leeds United, p450)
- [ ] **515**: `0515-ferguson` (Motherwell, p515), `0515-banks` (Tottenham Hotspur, p896)
- [ ] **525**: `0525-brennan` (Manchester City, p528), `0525-cookson` (Manchester City, p534)
- [ ] **540**: `0540-travers` (Gillingham, p339), `0540-weston` (Swindon Town, p877)
- [ ] **558**: `0558-thompson` (Bristol City, p137), `0558-jones` (Bristol City, p139a)
- [ ] **639**: `0639-watson` (Northampton Town, p605), `0639-kasher` (Stoke, p859)
- [ ] **659**: `0659-allen` (West Ham United, p939), `0659-kay` (West Ham United, p940)
- [ ] **695**: `0695-elliott` (Preston North End, p702), `0695-woodhouse` (Preston North End, p702)
- [ ] **705**: `0705-brough` (Huddersfield Town, p425), `0705-slade` (Huddersfield Town, p425)
- [ ] **1162**: `1162-eatock` (Wigan, p953), `1162-whitfield` (Wigan, p954)
- [ ] **1195**: `1195-kellett` (Crewe Alex, p246), `1195-steele` (Crewe Alex, p246)
- [ ] **1216**: `1216-mcferran` (Darlington, p269), `1216-bradford` (St Mirren, p780)
- [ ] **1253**: `1253-howieson` (Airdrie, p25), `1253-griffin` (Newport County, p578)
- [ ] **1278**: `1278-gillies` (St Mirren, p781), `1278-duff` (St Mirren, p782)
- [ ] **1285**: `1285-ritchie` (Hibernian, p405), `1285-lawson` (St Mirren, p782)
- [ ] **1323**: `1323-sivewright` (Dulwich Hamlet, p281), `1323-brown` (Morton, p510)
- [ ] **1328**: `1328-darvill` (Ilford, p438), `1328-buchanan` (Morton, p512)
- [ ] **1357**: `1357-milne` (Aberdeen, p18), `1357-crighton` (Partick Thistle, p665)
- [ ] **1359**: `1359-middleton` (Aberdeen, p21b), `1359-guilliard` (Dulwich Hamlet, p281)
- [ ] **1424**: `1424-reid` (Motherwell, p518), `1424-shaw` (Woking, p964)
- [ ] **1447**: `1447-sharp` (Albion Rovers, p31c), `1447-brown` (Clyde, p173b)
- [ ] **1558**: `1558-rigby` (Exeter City, p316), `1558-wilson` (Portsmouth, p697)
- [ ] **1663**: `1663-mclean` (Ayr Utd, p46c), `1663-muir` (Ayr Utd, p46c)
- [ ] **1664**: `1664-low` (Ayr Utd, p46c), `1664-nesbit` (Ayr Utd, p46c)
- [ ] **1715**: `1715-spence` (Manchester Utd, p544), `1715-wood` (Manchester Utd, p545)
- [ ] **1754**: `1754-shaw` (Hibernian, p407), `1754-graham` (Leytonstone, p474)
- [ ] **1781**: `1781-murphy` (Derby Co, p277), `1781-slater` (Southend United, p831)
- [ ] **1782**: `1782-hampson` (Hartlepool Utd, p415), `1782-barnes` (Southend United, p832)
- [ ] **1783**: `1783-christie` (Southampton, p822), `1783-dobson` (Southend United, p832)
- [ ] **1997**: `1997-sibbald` (Southport, p835), `1997-tyler` (Stalybridge Celtic, p843)
- [ ] **2025**: `2025-cairney` (Glasgow Celtic, p259), `2025-dixon` (Halifax Town, p413)
- [ ] **2052**: `2052-harris` (Rotherham County, p768), `2052-emmett` (Rotherham County, p769)
- [ ] **2057**: `2057-foweather` (Rochdale, p761), `2057-short` (Rochdale, p761)
- [ ] **2437**: `2437-noble` (Leeds United, p454), `2437-sherwin` (Leeds United, p454)
<!-- end generated -->

## Career rows to check (generated)

<!-- generated: career -->
Career tables with biography text in a row (12), or a card header read as a career row. Move the text to the biography, or rewrite the row from the .pub page.

- [ ] `0044-wren-2` (Notts County, p625): 1919-1922 row: biography text in the table
- [ ] `0141-skiller` (Swindon Town, p875): 1920-1922 row: biography text in the table
- [ ] `0245-gould-2` (Glasgow Rangers, p750): 1921-1924 row: biography text in the table
- [ ] `0762-lennon` (Luton Town, p490): 1919-1920 row: biography text in the table
- [ ] `0763-tirrell` (Luton Town, p490): 1920-1924 row: biography text in the table
- [ ] `1147-brown` (Raith Rovers, p728): 1924-1925 row: biography text in the table
- [ ] `1328-darvill` (Ilford, p438): 1924-1925 row: biography text in the table
- [ ] `1536-watson` (Huddersfield Town, p427): 1911-1927 row: biography text in the table
- [ ] `1732-clark` (Southampton, p822): 1920-1922 row: biography text in the table
- [ ] `1797-chatton` (Dumbarton, p290): 1924-1925 row: biography text in the table
- [ ] `1836-gatland` (Ilford, p438): 1922 row: biography text in the table
- [ ] `1862-howson` (Nelson, p587): 1922-1923 row: biography text in the table
<!-- end generated -->

## Sources to trace (generated)

<!-- generated: sources -->
Footnotes whose source is still `TO TRACE` (0). Find the reference in the Wikipedia article the text came from and replace the source line (see the README).

<!-- end generated -->

## Cards missing a detail (generated)

<!-- generated: details -->
Cards with a missing detail. Often the book simply has none; check the .pub page and fill it in, or tick the item.

<details><summary>no card scan (0)</summary>


</details>

<details><summary>no career rows (86)</summary>

- [ ] `0004-hardy-2` (Nottingham Forest, p634)
- [ ] `0135-anderson` (Clyde, p173c)
- [ ] `0146-harbridge` (Charlton, p195)
- [ ] `0167-spencer` (Brighton & Hove, p132a)
- [ ] `0254-neish` (Clydebank, p176)
- [ ] `0258-hall-3` (Millwall, p560)
- [ ] `0268-thomson` (Clyde, p173b)
- [ ] `0277-mackie` (Dumbarton, p288)
- [ ] `0282-cock-2` (Everton, p311a)
- [ ] `0304-smith-2` (Swansea Town, p772)
- [ ] `0318-collins` (Newport County, p573)
- [ ] `0319-mann` (Newport County, p573)
- [ ] `0430-feebury` (Crystal Palace, p252a)
- [ ] `0433-stephenson` (Huddersfield Town, p423)
- [ ] `0438-walker` (Aston Villa, p7)
- [ ] `0676-kirton` (Aston Villa, p9)
- [ ] `0695-woodhouse` (Preston North End, p702)
- [ ] `0743-mcintyre-2` (Sheffield Wednesday, p800)
- [ ] `0797-clarkson-2` (Rotherham County, p766)
- [ ] `0799-paterson` (Derby Co, p275)
- [ ] `0854-edge-2` (Exeter City, p314)
- [ ] `0959-nicholas` (Corinthians, p231)
- [ ] `0960-butcher` (Corinthians, p236)
- [ ] `0963-morrison` (Corinthians, p231)
- [ ] `0968-coleman` (Dulwich Hamlet, p279)
- [ ] `1169-goodens` (Wimbledon, p958)
- [ ] `1174-` (Wimbledon, p958)
- [ ] `1176-macey` (Wimbledon, p960)
- [ ] `1188-dickinson` (Barrow, p71d)
- [ ] `1190-charlton` (Crewe Alex, p247a)
- [ ] `1319-henderson` (Hearts, p356)
- [ ] `1323-sivewright` (Dulwich Hamlet, p281)
- [ ] `1359-guilliard` (Dulwich Hamlet, p281)
- [ ] `1367-brooker` (Dulwich Hamlet, p281)
- [ ] `1368-goodliffe` (Dulwich Hamlet, p281)
- [ ] `1370-jonas` (Dulwich Hamlet, p280)
- [ ] `1371-evans` (Dulwich Hamlet, p281)
- [ ] `1372-young` (Dulwich Hamlet, p281)
- [ ] `1373-davis` (Dulwich Hamlet, p281)
- [ ] `1374-caesar` (Dulwich Hamlet, p279)
- [ ] `1376-kendrick` (Dulwich Hamlet, p281)
- [ ] `1377-nicol` (Dulwich Hamlet, p281)
- [ ] `1399-footballer` (Grimsby Town, p342)
- [ ] `1424-shaw` (Woking, p964)
- [ ] `1452-meikle` (Airdrie, p25)
- [ ] `1524-hunt` (Dulwich Hamlet, p281)
- [ ] `1549-mcgee` (Portsmouth, p696)
- [ ] `1568-o-gorman` (Wycombe Wanderers, p979)
- [ ] `1587-howard` (Stalybridge Celtic, p841)
- [ ] `1663-mclean` (Ayr Utd, p46c)
- [ ] `1664-nesbit` (Ayr Utd, p46c)
- [ ] `1759-taylor` (Rochdale, p760)
- [ ] `1760-gee` (Rochdale, p758)
- [ ] `1789-payne` (Leytonstone, p474)
- [ ] `1812-ross` (Wimbledon, p960)
- [ ] `1877-three` (Durham, p285)
- [ ] `1960-bond` (Wimbledon, p960)
- [ ] `1977-swan` (Clydebank, p179a)
- [ ] `1980-chalmers` (Clydebank, p175)
- [ ] `1990-bower` (Casuals, p190)
- [ ] `1996-ewer` (Casuals, p191)
- [ ] `2031-mann` (Wimbledon, p962)
- [ ] `2034-stacey` (Wimbledon, p962)
- [ ] `2057-short` (Rochdale, p761)
- [ ] `2171-thomson` (Raith Rovers, p732)
- [ ] `2213-milne` (Clydebank, p179a)
- [ ] `2318-green` (Corinthians, p236)
- [ ] `2319-bell` (Corinthians, p233)
- [ ] `2320-barker` (Corinthians, p236)
- [ ] `2321-moulsdale` (Corinthians, p236)
- [ ] `2324-doggart` (Corinthians, p235)
- [ ] `2394-sharp` (Clydebank, p179)
- [ ] `2411-lowson` (Lincoln City, p467)
- [ ] `2425-mallett` (Woking, p964)
- [ ] `2426-briggs` (Woking, p964)
- [ ] `2427-gibbs` (Woking, p964)
- [ ] `2428-crane` (Woking, p965)
- [ ] `2429-ledger` (Woking, p965)
- [ ] `2430-thayers` (Woking, p965)
- [ ] `2431-harman` (Woking, p965)
- [ ] `2432-stocks` (Woking, p966)
- [ ] `2433-norcott` (Woking, p966)
- [ ] `2434-urpeth` (Woking, p966)
- [ ] `2435-griffin` (Woking, p966)
- [ ] `2436-berry` (Woking, p967)
- [ ] `2452-soulsby` (Ashington, p60)

</details>

<details><summary>no position (100)</summary>

- [ ] `0086-boyle` (Burnley, p153)
- [ ] `0141-skiller` (Swindon Town, p875)
- [ ] `0146-harbridge` (Charlton, p195)
- [ ] `0192-gibbon` (Dundee, p295)
- [ ] `0242-walker` (Third Lanark, p883)
- [ ] `0246-dickson-2` (Queens Park, p708)
- [ ] `0246-dickson` (Hamilton Acc, p351)
- [ ] `0272-kerr` (Hibernian, p404)
- [ ] `0282-cock-2` (Everton, p311a)
- [ ] `0389-mcalpine` (Queens Park, p709)
- [ ] `0465-walker` (Third Lanark, p885)
- [ ] `0538-seddon` (Bolton Wanderers, p98)
- [ ] `0633-bown` (Halifax Town, p411)
- [ ] `0635-pynegar` (Leicester City, p461)
- [ ] `0665-james` (West Ham United, p943)
- [ ] `0748-lyons` (Derby Co, p274)
- [ ] `0802-short` (Watford, p922)
- [ ] `0817-smith` (Norwich City, p618)
- [ ] `0830-hole` (Swansea Town, p774)
- [ ] `0852-walters` (Millwall, p569)
- [ ] `0874-moore` (Brighton & Hove, p130)
- [ ] `0876-lawrence` (Derby Co, p274)
- [ ] `0960-butcher` (Corinthians, p236)
- [ ] `0964-ashton` (Corinthians, p232)
- [ ] `1174-` (Wimbledon, p958)
- [ ] `1193-moss` (Crewe Alex, p245)
- [ ] `1221-archer` (Swindon Town, p879)
- [ ] `1245-noble` (Albion Rovers, p31a)
- [ ] `1270-sneddon` (Queens Park, p710)
- [ ] `1278-duff` (St Mirren, p782)
- [ ] `1291-ford` (Alloa, p41a)
- [ ] `1292-young` (Alloa, p41a)
- [ ] `1294-quinn` (Alloa, p41b)
- [ ] `1303-mclean` (Dundee, p299)
- [ ] `1304-nicol` (Dundee, p297)
- [ ] `1323-sivewright` (Dulwich Hamlet, p281)
- [ ] `1345-mcclure` (Clyde, p173b)
- [ ] `1359-guilliard` (Dulwich Hamlet, p281)
- [ ] `1367-brooker` (Dulwich Hamlet, p281)
- [ ] `1368-goodliffe` (Dulwich Hamlet, p281)
- [ ] `1371-evans` (Dulwich Hamlet, p281)
- [ ] `1372-young` (Dulwich Hamlet, p281)
- [ ] `1373-davis` (Dulwich Hamlet, p281)
- [ ] `1376-kendrick` (Dulwich Hamlet, p281)
- [ ] `1377-nicol` (Dulwich Hamlet, p281)
- [ ] `1386-bellamy` (Watford, p924)
- [ ] `1399-footballer` (Grimsby Town, p342)
- [ ] `1411-mcdonald` (Queens Park, p712)
- [ ] `1413-calderwood` (Queens Park, p713)
- [ ] `1423-wallace` (Clydebank, p176)
- [ ] `1424-shaw` (Woking, p964)
- [ ] `1439-farrell` (Clyde, p173c)
- [ ] `1452-meikle` (Airdrie, p25)
- [ ] `1524-hunt` (Dulwich Hamlet, p281)
- [ ] `1542-johnstone` (Hamilton Acc, p353)
- [ ] `1648-harvey` (Kilmarnock, p445)
- [ ] `1654-dickson` (Queens Park, p711)
- [ ] `1655-bell` (Clydebank, p176)
- [ ] `1657-mckechnie` (Partick Thistle, p668)
- [ ] `1663-muir` (Ayr Utd, p46c)
- [ ] `1664-nesbit` (Ayr Utd, p46c)
- [ ] `1765-gillespie` (Aberdare, p36c)
- [ ] `1836-gatland` (Ilford, p438)
- [ ] `1877-three` (Durham, p285)
- [ ] `1879-elliott` (Durham, p286)
- [ ] `1880-young` (Durham, p286)
- [ ] `1882-andrews` (Durham, p286)
- [ ] `1883-hall` (Durham, p286)
- [ ] `1932-nuttall` (Bolton Wanderers, p102)
- [ ] `1981-mcgovern` (Clydebank, p178)
- [ ] `2015-haywood` (Chelsea, p212)
- [ ] `2032-slader` (Wimbledon, p962)
- [ ] `2033-goodchild` (Wimbledon, p962)
- [ ] `2034-stacey` (Wimbledon, p962)
- [ ] `2076-edelston` (Fulham, p334)
- [ ] `2109-timmins` (Walsall, p915)
- [ ] `2144-jenkins` (Brighton & Hove, p132)
- [ ] `2200-garratt` (Chesterfield, p215)
- [ ] `2318-green` (Corinthians, p236)
- [ ] `2319-bell` (Corinthians, p233)
- [ ] `2320-barker` (Corinthians, p236)
- [ ] `2321-moulsdale` (Corinthians, p236)
- [ ] `2383-halleron` (Dumbarton, p293)
- [ ] `2394-sharp` (Clydebank, p179)
- [ ] `2411-lowson` (Lincoln City, p467)
- [ ] `2417-fenwick` (Lincoln City, p466)
- [ ] `2425-mallett` (Woking, p964)
- [ ] `2426-briggs` (Woking, p964)
- [ ] `2427-gibbs` (Woking, p964)
- [ ] `2428-crane` (Woking, p965)
- [ ] `2429-ledger` (Woking, p965)
- [ ] `2430-thayers` (Woking, p965)
- [ ] `2431-harman` (Woking, p965)
- [ ] `2432-stocks` (Woking, p966)
- [ ] `2433-norcott` (Woking, p966)
- [ ] `2434-urpeth` (Woking, p966)
- [ ] `2435-griffin` (Woking, p966)
- [ ] `2436-berry` (Woking, p967)
- [ ] `2458-hosker` (Accrington Stanley, p16b)
- [ ] `2462-whitworth` (Chesterfield, p218)

</details>

<details><summary>no birth line (86)</summary>

- [ ] `0004-hardy-2` (Nottingham Forest, p634)
- [ ] `0135-anderson` (Clyde, p173c)
- [ ] `0167-spencer` (Brighton & Hove, p132a)
- [ ] `0210-ferrier` (Morton, p507)
- [ ] `0246-dickson-2` (Queens Park, p708)
- [ ] `0246-dickson` (Hamilton Acc, p351)
- [ ] `0254-neish` (Clydebank, p176)
- [ ] `0255-goldie` (Clydebank, p176)
- [ ] `0258-hall-3` (Millwall, p560)
- [ ] `0259-martin` (Hamilton Acc, p350)
- [ ] `0268-thomson` (Clyde, p173b)
- [ ] `0304-smith-2` (Swansea Town, p772)
- [ ] `0388-thom` (Queens Park, p709)
- [ ] `0430-feebury` (Crystal Palace, p252a)
- [ ] `0433-stephenson` (Huddersfield Town, p423)
- [ ] `0695-woodhouse` (Preston North End, p702)
- [ ] `0960-butcher` (Corinthians, p236)
- [ ] `1147-brown` (Raith Rovers, p728)
- [ ] `1174-` (Wimbledon, p958)
- [ ] `1188-dickinson` (Barrow, p71d)
- [ ] `1190-charlton` (Crewe Alex, p247a)
- [ ] `1197-harding` (Crewe Alex, p247a)
- [ ] `1245-noble` (Albion Rovers, p31a)
- [ ] `1278-duff` (St Mirren, p782)
- [ ] `1278-gillies` (St Mirren, p781)
- [ ] `1292-young` (Alloa, p41a)
- [ ] `1294-quinn` (Alloa, p41b)
- [ ] `1319-henderson` (Hearts, p356)
- [ ] `1323-sivewright` (Dulwich Hamlet, p281)
- [ ] `1345-mcclure` (Clyde, p173b)
- [ ] `1359-guilliard` (Dulwich Hamlet, p281)
- [ ] `1367-brooker` (Dulwich Hamlet, p281)
- [ ] `1368-goodliffe` (Dulwich Hamlet, p281)
- [ ] `1371-evans` (Dulwich Hamlet, p281)
- [ ] `1372-young` (Dulwich Hamlet, p281)
- [ ] `1373-davis` (Dulwich Hamlet, p281)
- [ ] `1376-kendrick` (Dulwich Hamlet, p281)
- [ ] `1377-nicol` (Dulwich Hamlet, p281)
- [ ] `1399-footballer` (Grimsby Town, p342)
- [ ] `1413-calderwood` (Queens Park, p713)
- [ ] `1418-campbell` (St Mirren, p783)
- [ ] `1424-shaw` (Woking, p964)
- [ ] `1435-hunter` (Dundee, p301a)
- [ ] `1447-brown` (Clyde, p173b)
- [ ] `1452-meikle` (Airdrie, p25)
- [ ] `1524-hunt` (Dulwich Hamlet, p281)
- [ ] `1549-mcgee` (Portsmouth, p696)
- [ ] `1565-gates` (Wycombe Wanderers, p979)
- [ ] `1567-adams` (Wycombe Wanderers, p979)
- [ ] `1568-o-gorman` (Wycombe Wanderers, p979)
- [ ] `1587-howard` (Stalybridge Celtic, p841)
- [ ] `1653-maiden` (Dundee, p298)
- [ ] `1663-mclean` (Ayr Utd, p46c)
- [ ] `1664-nesbit` (Ayr Utd, p46c)
- [ ] `1798-robertson` (Dumbarton, p289)
- [ ] `1812-ross` (Wimbledon, p960)
- [ ] `1844-winn` (Tranmere Rovers, p901)
- [ ] `1960-bond` (Wimbledon, p960)
- [ ] `1977-swan` (Clydebank, p179a)
- [ ] `1978-fleming` (Clydebank, p177)
- [ ] `1979-mcgovern` (Clydebank, p177)
- [ ] `1984-grant` (Clydebank, p178)
- [ ] `2023-mcdonald` (Queens Park, p713)
- [ ] `2032-slader` (Wimbledon, p962)
- [ ] `2057-short` (Rochdale, p761)
- [ ] `2080-brown` (Raith Rovers, p731)
- [ ] `2136-galbraith` (Clapton Orient, p229)
- [ ] `2171-thomson` (Raith Rovers, p732)
- [ ] `2213-milne` (Clydebank, p179a)
- [ ] `2318-green` (Corinthians, p236)
- [ ] `2320-barker` (Corinthians, p236)
- [ ] `2321-moulsdale` (Corinthians, p236)
- [ ] `2394-sharp` (Clydebank, p179)
- [ ] `2411-lowson` (Lincoln City, p467)
- [ ] `2425-mallett` (Woking, p964)
- [ ] `2426-briggs` (Woking, p964)
- [ ] `2427-gibbs` (Woking, p964)
- [ ] `2428-crane` (Woking, p965)
- [ ] `2429-ledger` (Woking, p965)
- [ ] `2430-thayers` (Woking, p965)
- [ ] `2431-harman` (Woking, p965)
- [ ] `2432-stocks` (Woking, p966)
- [ ] `2433-norcott` (Woking, p966)
- [ ] `2434-urpeth` (Woking, p966)
- [ ] `2435-griffin` (Woking, p966)
- [ ] `2436-berry` (Woking, p967)

</details>
<!-- end generated -->

## Done during the migration

A record of what was checked and fixed, for reference.

- [x] Card scans: every scan placed by page order (295) or with a weak OCR match (303) was checked by eye against the name printed on the card. Three pages were wrong: p26b and p222 (fixed in the converter) and p26c, where `1451-reid` and `1255-murdoch` were swapped by hand in `content/img/`. Re-running the converter on p26c would swap them back.
- [x] Scans that look wrong but match the book: `1224-nash` and `1226-denyer` (p880, p881) show each other's names; the page notes the names were swapped when the cards were printed.
- [x] Variants: 207 card numbers appear under two or three clubs with the same player (the same photograph with a different club on the front, e.g. 62 Meredith, Manchester City and Manchester United). Each version is its own checklist entry, and the player pages link to each other.
- [x] Career-only entries: about 650 cards have career rows but no biography in the book (e.g. 327 Nicholls, p826).
- [x] Name lines with decorations ("MM & Bar", "DSC & MC"), asterisks and notes ("Personal data and position unavailable", "Known as Vivian") are split into name and name note.
- [x] Card headings written "Card419", "Card 14 24", a bare "2210", ".Card 822", "ard 875", or with a note ("Card 58 but also shown as Card 1486", p82 and p113a) are recognised; the note goes into the card's collector notes.
- [x] Continuation pages joined to the biography they continue: p71c, p262, p301, p323, p478, p523-525, p867, and p662 (its heading wrongly says "Card 199"; it continues `0198-mcmenemy`).
- [x] 73 biographies that start "Born in..." had replaced the card's birth line; re-parsed.
- [x] Nine cross-reference cards had "Please see page 52 for full bio" as their position; they now link to the full biography.
- [x] Career tables: 128 cards had apps or goals in the wrong cells (a typo in "apps" leaving the number on the club, "40 apps 16 apps" leaving the goals in the note, or a second club with mistyped years in the note). Moved into the right cells; 81 rows split out and 8 international caps moved to the representative honours.

## Notes

Free text for anything that does not fit above.
