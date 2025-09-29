wine_1_examples=[
  {
    "input": "2009年总共生产了多少箱酒，比2007年增长了百分之多少？",
    "query": "SELECT n_2009 , 100.0 * ( n_2009 - n_2007 ) / n_2007 AS growth_rate FROM ( SELECT SUM ( Cases ) AS n_2009 FROM wine WHERE Year = \"2009\" ) JOIN ( SELECT SUM ( Cases ) AS n_2007 FROM wine WHERE Year = \"2007\" )",
    "reasoning_type": "- * /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如2009年没有生产长相思葡萄酒，2009年总共生产了多少箱酒，比2007年增长了百分之多少？",
    "query": "SELECT n_2009 , 100.0 * ( n_2009 - n_2007 ) / n_2007 AS growth_rate FROM ( SELECT SUM ( Cases ) AS n_2009 FROM wine WHERE Year = \"2009\" AND Name != \"Sauvignon Blanc\" ) JOIN ( SELECT SUM ( Cases ) AS n_2007 FROM wine WHERE Year = \"2007\" )",
    "reasoning_type": "- * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "有多少种酒不是产自美国葡萄种植区，比产自美国葡萄种植区的酒多多少？",
    "query": "SELECT no_ava , no_ava - ava AS diff FROM ( SELECT COUNT ( * ) AS no_ava FROM appellations A JOIN wine B ON A.Appelation = B.Appelation WHERE A.isAVA = \"N\" ) JOIN ( SELECT COUNT ( * ) AS ava FROM appellations A JOIN wine B ON A.Appelation = B.Appelation WHERE A.isAVA = \"Y\" )",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如价格比葡萄酒均价低10美元以上的酒都产自非美国葡萄种植区，有多少种酒不是产自美国葡萄种植区，比产自美国葡萄种植区的酒多多少？",
    "query": "SELECT no_ava , no_ava - ava AS diff FROM ( SELECT COUNT ( * ) AS no_ava FROM appellations A JOIN wine B ON A.Appelation = B.Appelation WHERE A.isAVA = \"N\" OR B.Price <= ( SELECT AVG ( Price ) FROM wine ) - 10 ) JOIN ( SELECT COUNT ( * ) AS ava FROM appellations A JOIN wine B ON A.Appelation = B.Appelation WHERE A.isAVA = \"Y\" AND B.Price > ( SELECT AVG ( Price ) FROM wine ) - 10 )",
    "reasoning_type": "- H",
    "commonsense_knowledge": ""
  },
  {
    "input": "2008年红葡萄酒的产量是白葡萄酒的多少倍？",
    "query": "SELECT 1.0 * n_red / n_white AS times FROM ( SELECT SUM ( A.Cases ) AS n_red FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"Red\" AND A.Year = \"2008\" ) JOIN ( SELECT SUM ( A.Cases ) AS n_white FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"White\" AND A.Year = \"2008\" )",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如每种酒的产量都增加100箱，2008年红葡萄酒的产量是白葡萄酒的多少倍？",
    "query": "SELECT 1.0 * n_red / n_white AS times FROM ( SELECT SUM ( A.Cases + 100 ) AS n_red FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"Red\" AND A.Year = \"2008\" ) JOIN ( SELECT SUM ( A.Cases + 100 ) AS n_white FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"White\" AND A.Year = \"2008\" )",
    "reasoning_type": "+ * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "98评分的酒的最高价和最低价相差多少？",
    "query": "SELECT MAX ( Price ) - MIN ( Price ) AS diff FROM wine WHERE Score = \"98\"",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如卡莱尔酒厂的酒全部涨价10%，98评分的酒的最高价和最低价相差多少？",
    "query": "SELECT MAX ( Price ) - MIN ( Price ) AS diff FROM ( SELECT price * ( 1 + 0.1 ) AS price , Score FROM wine WHERE Winery = \"Carlisle\" UNION ALL SELECT price , Score FROM wine WHERE Winery != \"Carlisle\" ) WHERE Score = \"98\"",
    "reasoning_type": "+ - * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "美国葡萄种植区中哪个酒产区的酒总产量没有达到卡拉维拉斯县产区的两倍？",
    "query": "SELECT A.Appelation FROM wine A JOIN appellations B ON A.Appelation = B.Appelation WHERE B.isAVA = \"Y\" GROUP BY A.Appelation HAVING SUM ( A.Cases ) < 2 * ( SELECT SUM ( Cases ) FROM wine WHERE Appelation = \"Calaveras County\" )",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如生产于2009年的酒的产量翻倍，美国葡萄种植区中哪个产区的酒总产量没有达到卡拉维拉斯县产区的两倍？",
    "query": "SELECT A.Appelation FROM (SELECT Appelation, Cases FROM wine WHERE YEAR != \"2009\" UNION ALL SELECT Appelation, 2 * Cases FROM wine WHERE YEAR = \"2009\" ) A JOIN appellations B ON A.Appelation = B.Appelation WHERE B.isAVA = \"Y\" GROUP BY A.Appelation HAVING SUM (A.Cases) < 2 * (SELECT SUM(Cases) FROM (SELECT SUM (Cases) AS Cases FROM wine WHERE Appelation = \"Calaveras County\" AND Year!= 2009 UNION ALL SELECT 2*SUM (Cases) AS Cases FROM wine WHERE Appelation = \"Calaveras County\" AND Year= 2009))",
    "reasoning_type": "* H",
    "commonsense_knowledge": ""
  },
  {
    "input": "价格低于40的酒中，有百分之多少的酒评分高于85？",
    "query": "SELECT 100.0 * n1 / n2 AS ratio FROM ( SELECT COUNT ( * ) AS n1 FROM wine WHERE Price < \"40\" AND Score > \"85\" ) JOIN ( SELECT COUNT ( * ) AS n2 FROM wine WHERE Price < \"40\" )",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如用仙粉黛葡萄酿造的葡萄酒全部涨价15，价格低于40的酒中，有百分之多少的酒评分高于85？",
    "query": "SELECT 100.0 * n1 / n2 AS ratio FROM ( SELECT COUNT ( * ) AS n1 FROM ( SELECT Price , Score FROM wine WHERE Grape != \"Zinfandel\" UNION ALL SELECT Price + 15 , Score FROM wine WHERE Grape = \"Zinfandel\" ) WHERE Price < \"40\" AND Score > \"85\" ) JOIN ( SELECT COUNT ( * ) AS n2 FROM ( SELECT Price , Score FROM wine WHERE Grape != \"Zinfandel\" UNION ALL SELECT Price + 15 , Score FROM wine WHERE Grape = \"Zinfandel\" ) WHERE Price < \"40\" )",
    "reasoning_type": "+ * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "价格最高的酒的产区生产的酒中，有哪些酒的评分比价格最高的酒的最低评分高10分以上？给出它们的编号和名字。",
    "query": "SELECT No, name FROM wine WHERE Appelation IN ( SELECT Appelation FROM wine WHERE Price = ( SELECT MAX ( Price ) FROM wine ) ) AND Score > ( SELECT MIN ( Score ) FROM wine WHERE Price = ( SELECT MAX ( Price ) FROM wine ) ) + 10",
    "reasoning_type": "+",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如2008年生产的酒涨价15%，价格最高的酒的产区生产的酒中，有哪些酒的评分比价格最高的酒的最低评分高10分以上？给出它们的编号和名字。",
    "query": "SELECT No, Name FROM (SELECT No, Name, Appelation, Price, Score FROM wine WHERE YEAR != \"2008\" UNION ALL SELECT No, Name, Appelation, (1 + 0.15) * Price, Score FROM wine WHERE YEAR = \"2008\" ) WHERE Appelation IN (SELECT Appelation FROM (SELECT No, Name, Appelation, Price, Score FROM wine WHERE YEAR != \"2008\" UNION ALL SELECT No, Name, Appelation, (1 + 0.15) * Price, Score FROM wine WHERE YEAR = \"2008\" ) WHERE Price = (SELECT MAX (Price) FROM (SELECT No, Name, Appelation, Price, Score FROM wine WHERE YEAR != \"2008\" UNION ALL SELECT No, Name, Appelation, (1 + 0.15) * Price, Score FROM wine WHERE YEAR = \"2008\" )) ) AND Score > (SELECT MIN (Score) FROM (SELECT No, Name, Appelation, Price, Score FROM wine WHERE YEAR != \"2008\" UNION ALL SELECT No, Name, Appelation, (1 + 0.15) * Price, Score FROM wine WHERE YEAR = \"2008\" ) WHERE Price = (SELECT MAX (Price) FROM (SELECT No, Name, Appelation, Price, Score FROM wine WHERE YEAR != \"2008\" UNION ALL SELECT No, Name, Appelation, (1 + 0.15) * Price, Score FROM wine WHERE YEAR = \"2008\" )) ) + 10",
    "reasoning_type": "+ * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "酿造一瓶红葡萄酒需要1.2千克的葡萄。2005年生产的红葡萄酒用了多少吨葡萄？",
    "query": "SELECT 1.2 * SUM ( A.Cases ) * 12 / 1000 AS tons FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE A.Year = \"2005\" AND B.Color = \"Red\"",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "1 case equals to 12 bottles and 1 ton equals to 1000 kilograms."
  },
  {
    "input": "酿造一瓶红葡萄酒需要1.2千克的葡萄。假如帕洛玛酒厂2005年没有生产葡萄酒，2005年生产的红葡萄酒用了多少吨葡萄？",
    "query": "SELECT 1.2 * SUM ( A.Cases ) * 12 / 1000 AS tons FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE A.Year = \"2005\" AND B.Color = \"Red\" AND A.Winery != \"Paloma\"",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "1 case equals to 12 bottles and 1 ton equals to 1000 kilograms."
  },
  {
    "input": "酿造一瓶葡萄酒需要1.2千克的葡萄。在纳帕县生产的葡萄酒一共用了多少吨红葡萄，多少吨白葡萄？",
    "query": "SELECT * FROM ( SELECT 1.2 * SUM ( A.Cases ) * 12 / 1000 AS tons_red FROM wine A JOIN grapes B ON A.Grape = B.Grape JOIN appellations C ON A.Appelation = C.Appelation WHERE C.County = \"Napa\" AND B.Color = \"Red\" ) JOIN ( SELECT 1.2 * SUM ( A.Cases ) * 12 / 1000 AS tons_while FROM wine A JOIN grapes B ON A.Grape = B.Grape JOIN appellations C ON A.Appelation = C.Appelation WHERE C.County = \"Napa\" AND B.Color = \"White\" )",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "1 case equals to 12 bottles and 1 ton equals to 1000 kilograms."
  },
  {
    "input": "酿造一瓶葡萄酒需要1.2千克的葡萄。假如所有卡内罗斯葡萄酒的产区都不在纳帕县，产区在纳帕县的葡萄酒一共用了多少吨红葡萄，多少吨白葡萄？",
    "query": "SELECT * FROM ( SELECT 1.2 * SUM ( A.Cases ) * 12 / 1000 AS tons_red FROM wine A JOIN grapes B ON A.Grape = B.Grape JOIN appellations C ON A.Appelation = C.Appelation WHERE C.County = \"Napa\" AND B.Color = \"Red\" AND A.Appelation != \"Carneros\" ) JOIN ( SELECT 1.2 * SUM ( A.Cases ) * 12 / 1000 AS tons_while FROM wine A JOIN grapes B ON A.Grape = B.Grape JOIN appellations C ON A.Appelation = C.Appelation WHERE C.County = \"Napa\" AND B.Color = \"White\" AND A.Appelation != \"Carneros\" )",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "1 case equals to 12 bottles and 1 ton equals to 1000 kilograms."
  },
  {
    "input": "评分最高的赤霞珠葡萄酒来自哪些酒厂，它们的价格比赤霞珠葡萄酒的平均价高多少？",
    "query": "SELECT Winery , Price - ( SELECT AVG ( Price ) FROM wine WHERE name = \"Cabernet Sauvignon\" ) AS diff FROM wine WHERE name = \"Cabernet Sauvignon\" AND Score = ( SELECT MAX ( Score ) FROM wine WHERE name = \"Cabernet Sauvignon\" )",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如2005年生产的全部酒的评分下降10分，评分最高的赤霞珠葡萄酒来自哪些酒厂，它们的价格比赤霞珠葡萄酒的平均价高多少？",
    "query": "SELECT Winery , Price - ( SELECT AVG ( Price ) FROM wine WHERE name = \"Cabernet Sauvignon\" ) AS diff FROM ( SELECT Winery , Price , Score - 10 AS Score , Name FROM wine WHERE Year = \"2005\" UNION ALL SELECT Winery , Price , Score , Name FROM wine WHERE Year != \"2005\" ) WHERE name = \"Cabernet Sauvignon\" AND Score = ( SELECT MAX ( Score ) FROM ( SELECT Winery , Price , Score - 10 AS Score , Name FROM wine WHERE Year = \"2005\" UNION ALL SELECT Winery , Price , Score , Name FROM wine WHERE Year != \"2005\" ) WHERE name = \"Cabernet Sauvignon\" )",
    "reasoning_type": "- H",
    "commonsense_knowledge": ""
  },
  {
    "input": "最贵的红葡萄酒比最贵的白葡萄酒贵多少？",
    "query": "SELECT max_red - max_white AS diff FROM ( SELECT MAX ( A.Price ) AS max_red FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"Red\" ) JOIN ( SELECT MAX ( A.Price ) AS max_white FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"White\" )",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如安培洛斯酒厂的酒降价20%，最贵的红葡萄酒比最贵的白葡萄酒贵多少？",
    "query": "SELECT max_red - max_white AS diff FROM ( SELECT MAX ( Price ) AS max_red FROM ( SELECT B.Color , A.Price * ( 1 - 0.2 ) AS Price FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE A.Winery = \"Ampelos\" UNION ALL SELECT B.Color , A.Price FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE A.Winery != \"Ampelos\" ) WHERE Color = \"Red\" ) JOIN ( SELECT MAX ( Price ) AS max_white FROM ( SELECT B.Color , A.Price * ( 1 - 0.2 ) AS Price FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE A.Winery = \"Ampelos\" UNION ALL SELECT B.Color , A.Price FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE A.Winery != \"Ampelos\" ) WHERE Color = \"White\" )",
    "reasoning_type": "- * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "如果一个酒厂能做到连续3年生产的酒评分从未低于90，它就会被评为“优质酒厂”。有百分之多少的酒厂是优质酒厂？",
    "query": "SELECT 100.0 * COUNT ( DISTINCT ( Winery ) ) / ( SELECT COUNT ( DISTINCT ( Winery ) ) FROM wine ) AS percent FROM ( SELECT A.Winery , A.No , A.Year , A.Score , B.No , B.Year , B.Score , C.No , C.Year , C.Score FROM wine A JOIN wine B ON A.Winery = B.Winery JOIN wine C ON A.Winery = C.Winery WHERE A.Score >= 90 AND B.Score >= 90 AND C.Score >= 90 AND B.Year - A.Year = 1 AND C.Year - B.Year = 1 )",
    "reasoning_type": "- * /",
    "commonsense_knowledge": ""
  },
  {
    "input": "如果一个酒厂能做到连续3年生产的酒评分从未低于90，它就会被评为“优质酒厂”。假如用黑比诺葡萄酿造的葡萄酒评分下降5分，有百分之多少的酒厂是优质酒厂？",
    "query": "SELECT 100.0 * COUNT ( DISTINCT ( Winery ) ) / ( SELECT COUNT ( DISTINCT ( Winery ) ) FROM wine ) AS percent FROM ( SELECT A.Winery , A.No , A.Year , A.Score , B.No , B.Year , B.Score , C.No , C.Year , C.Score FROM ( SELECt Winery , No , Year , Score - 5 AS Score FROM wine WHERE Grape = \"Pinot Noir\" UNION ALL SELECt Winery , No , Year , Score FROM wine WHERE Grape != \"Pinot Noir\" ) A JOIN ( SELECt Winery , No , Year , Score - 5 AS Score FROM wine WHERE Grape = \"Pinot Noir\" UNION ALL SELECt Winery , No , Year , Score FROM wine WHERE Grape != \"Pinot Noir\" ) B ON A.Winery = B.Winery JOIN ( SELECt Winery , No , Year , Score - 5 AS Score FROM wine WHERE Grape = \"Pinot Noir\" UNION ALL SELECt Winery , No , Year , Score FROM wine WHERE Grape != \"Pinot Noir\" ) C ON A.Winery = C.Winery WHERE A.Score >= 90 AND B.Score >= 90 AND C.Score >= 90 AND B.Year - A.Year = 1 AND C.Year - B.Year = 1 )",
    "reasoning_type": "- * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "哪年白葡萄酒的产量最高，比当年红葡萄酒的产量高多少？",
    "query": "SELECT Year , cases_white - cases_red AS diff FROM ( SELECT A.Year , SUM ( A.Cases ) AS cases_white FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"White\" GROUP BY A.Year ORDER BY SUM ( A.Cases ) DESC LIMIT 1 ) JOIN ( SELECT SUM ( A.Cases ) AS cases_red FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"Red\" AND Year = ( SELECT A.Year FROM wine A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"White\" GROUP BY A.Year ORDER BY SUM ( A.Cases ) DESC LIMIT 1 ) )",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如贝灵哲酒厂的全部酒产量翻倍，哪年白葡萄酒的产量最高，比当年红葡萄酒的产量高多少？",
    "query": "SELECT Year , cases_white - cases_red AS diff FROM ( SELECT A.Year , SUM ( A.Cases ) AS cases_white FROM ( SELECT Grape , Year , 2 * Cases AS Cases FROM wine WHERE Winery = \"Beringer\" UNION ALL SELECT Grape , Year , Cases AS Cases FROM wine WHERE Winery != \"Beringer\" ) A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"White\" GROUP BY A.Year ORDER BY SUM ( A.Cases ) DESC LIMIT 1 ) JOIN ( SELECT SUM ( A.Cases ) AS cases_red FROM ( SELECT Grape , Year , 2 * Cases AS Cases FROM wine WHERE Winery = \"Beringer\" UNION ALL SELECT Grape , Year , Cases AS Cases FROM wine WHERE Winery != \"Beringer\" ) A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"Red\" AND Year = ( SELECT A.Year FROM ( SELECT Grape , Year , 2 * Cases AS Cases FROM wine WHERE Winery = \"Beringer\" UNION ALL SELECT Grape , Year , Cases AS Cases FROM wine WHERE Winery != \"Beringer\" ) A JOIN grapes B ON A.Grape = B.Grape WHERE B.Color = \"White\" GROUP BY A.Year ORDER BY SUM ( A.Cases ) DESC LIMIT 1 ) )",
    "reasoning_type": "* - H",
    "commonsense_knowledge": ""
  }
]