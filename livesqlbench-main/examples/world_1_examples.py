world_1_examples=[
  {
    "input": "人均国民生产总值最高的国家在哪个大洲？",
    "query": "SELECT Continent FROM country ORDER BY 1.0 * GNP / Population DESC LIMIT 1",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "GNP per capita is computed by dividing the GNP by the population."
  },
  {
    "input": "假如库尔勒市所在的国家国民生产总值为1982268，人均国民生产总值最高的国家在哪个大洲？",
    "query": "SELECT Continent FROM (SELECT \"1982268.0\" AS GNP, Population, Continent FROM country WHERE name = (SELECT A.name FROM country A JOIN city B ON A.Code = B.CountryCode WHERE B.name = \"Korla\" ) UNION ALL SELECT GNP, Population, Continent FROM country WHERE name != (SELECT A.name FROM country A JOIN city B ON A.Code = B.CountryCode WHERE B.name = \"Korla\" ) ) ORDER BY 1.0 * GNP / Population DESC LIMIT 1",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "GNP per capita is computed by dividing the GNP by the population."
  },
  {
    "input": "1979年后独立的国家中，哪个国家的国民生产总值增长率最高？",
    "query": "SELECT Name FROM country WHERE IndepYear > 1979 ORDER BY 1.0 * ( GNP - GNPOld ) / GNPOld DESC LIMIT 1",
    "reasoning_type": "- * /",
    "commonsense_knowledge": ""
  },
  {
    "input": "1979年后独立的国家中，哪个国家的国民生产总值增长率最高假如大洋洲所有国家现在的国民生产总值增加1000000？",
    "query": "SELECT name FROM ( SELECT name , GNP + 1000000 AS GNP , GNPOld , IndepYear FROM country WHERE Continent = \"Oceania\" UNION ALL SELECT name , GNP , GNPOld , IndepYear FROM country WHERE Continent != \"Oceania\" ) WHERE IndepYear > 1979 ORDER BY 1.0 * ( GNP - GNPOld ) / GNPOld DESC LIMIT 1",
    "reasoning_type": "+ - * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "哪个绝大多数人说英语的国家的人口密度最高，是人口密度最低的国家的多少倍？",
    "query": "SELECT Name , ( 100.0 * Population / SurfaceArea ) / ( SELECT MIN ( 100.0 * Population / SurfaceArea ) FROM country WHERE 100.0 * Population / SurfaceArea > 0 ) AS times FROM country WHERE Code IN ( SELECT CountryCode FROM ( SELECT * , MAX ( Percentage ) FROM countrylanguage GROUP BY CountryCode ) WHERE Language = \"English\" ) ORDER BY 100.0 * Population / SurfaceArea DESC LIMIT 1",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "The density of population is the ratio between the numbers of people to the size of land."
  },
  {
    "input": "假如爱尔兰没有一个人说英语，哪个绝大多数人说英语的国家的人口密度最高，是人口密度最低的国家的多少倍？",
    "query": "SELECT Name , ( 100.0 * Population / SurfaceArea ) / ( SELECT MIN ( 100.0 * Population / SurfaceArea ) FROM country WHERE 100.0 * Population / SurfaceArea > 0 ) AS times FROM country WHERE Code IN ( SELECT CountryCode FROM ( SELECT * , MAX ( Percentage ) FROM countrylanguage A JOIN country B ON A.CountryCode = B.Code WHERE B.name != \"Ireland\" GROUP BY A.CountryCode ) WHERE Language = \"English\" ) ORDER BY 100.0 * Population / SurfaceArea DESC LIMIT 1",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "The density of population is the ratio between the numbers of people to the size of land."
  },
  {
    "input": "阿拉伯语不是官方语言的国家中，哪个国家的国民生产总值的增长幅度最大？",
    "query": "SELECT Name FROM country WHERE Code NOT IN ( SELECT CountryCode FROM countrylanguage WHERE Language = \"Arabic\" AND IsOfficial = \"T\" ) ORDER BY 100.0 * ( GNP - GNPOld ) / GNPOld DESC LIMIT 1",
    "reasoning_type": "- * /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如南美洲所有国家过去的国民生产总值增加9999，在阿拉伯语不是官方语言的国家中，哪个国家的国民生产总值的增长幅度最大？",
    "query": "SELECT Name FROM ( SELECT Name , Code , GNP , GNPOld + 9999.0 AS GNPOld FROM country WHERE Continent = \"South America\" UNION ALL SELECT Name , Code , GNP , GNPOld FROM country WHERE Continent != \"South America\" ) WHERE Code NOT IN ( SELECT CountryCode FROM countrylanguage WHERE Language = \"Arabic\" AND IsOfficial = \"T\" ) ORDER BY 100.0 * ( GNP - GNPOld ) / GNPOld DESC LIMIT 1",
    "reasoning_type": "- + * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "北美洲哪个城市的人口数量至少是江原道行政区的两倍？",
    "query": "SELECT B.name FROM country A JOIN city B ON A.Code = B.CountryCode WHERE A.Continent = \"North America\" AND B.Population >= 2 * ( SELECT SUM ( Population ) FROM city WHERE District = \"Kang-won\" )",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如北美洲以英语为官方语言的国家的城市人口增加1%，北美洲哪个城市的人口数量至少是江原道行政区的两倍？",
    "query": "SELECT DISTINCT ( name ) FROM ( SELECT B.name , B.Population * ( 1 + 0.01 ) AS Population FROM country A JOIN city B ON A.Code = B.CountryCode JOIN countrylanguage C ON A.Code = C.CountryCode WHERE A.Continent = \"North America\" AND C.Language = \"English\" AND C.IsOfficial = \"T\" UNION ALL SELECT B.name , B.Population FROM country A JOIN city B ON A.Code = B.CountryCode JOIN countrylanguage C ON A.Code = C.CountryCode WHERE A.Continent = \"North America\" AND NOT ( C.Language = \"English\" AND C.IsOfficial = \"T\" ) ) WHERE Population >= 2 * ( SELECT SUM ( Population ) FROM city WHERE District = \"Kang-won\" )",
    "reasoning_type": "* + H",
    "commonsense_knowledge": ""
  },
  {
    "input": "哪个大洲的国民生产总值增长率至少是非洲的1.5倍？",
    "query": "SELECT Continent FROM country GROUP BY Continent HAVING 100.0 * ( SUM ( GNP ) - SUM ( GNPOld ) ) / SUM ( GNPOld ) > 1.5 * ( SELECT 100.0 * ( SUM ( GNP ) - SUM ( GNPOld ) ) / SUM ( GNPOld ) FROM country WHERE Continent = \"Africa\" )",
    "reasoning_type": "- * /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如绝大多数人说捷克语的国家现在的国民生产总值增加0.5%，哪个大洲的国民生产总值增长率至少是非洲的1.5倍？",
    "query": "SELECT Continent FROM ( SELECT Code , GNP * ( 1 + 0.005 ) AS GNP , GNPOld , Continent FROM country WHERE Code IN ( SELECT CountryCode FROM ( SELECT CountryCode , Language , MAX ( Percentage ) FROM countrylanguage GROUP BY CountryCode ) WHERE Language = \"Czech\" ) UNION ALL SELECT Code , GNP , GNPOld , Continent FROM country WHERE Code NOT IN ( SELECT CountryCode FROM ( SELECT CountryCode , Language , MAX ( Percentage ) FROM countrylanguage GROUP BY CountryCode ) WHERE Language = \"Czech\" ) ) GROUP BY Continent HAVING 100.0 * ( SUM ( GNP ) - SUM ( GNPOld ) ) / SUM ( GNPOld ) > 1.5 * ( SELECT 100.0 * ( SUM ( GNP ) - SUM ( GNPOld ) ) / SUM ( GNPOld ) FROM country WHERE Continent = \"Africa\" )",
    "reasoning_type": "+ - * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "哪个国家的人口预期寿命不低于赞比亚的1.5倍？",
    "query": "SELECT Name FROM country WHERE LifeExpectancy >= 1.5 * ( SELECT LifeExpectancy FROM country WHERE name = \"Zambia\" )",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如人均国民生产总值是全球前20的国家的人口预期寿命都是90，哪个国家的人口预期寿命不低于赞比亚的1.5倍？",
    "query": "SELECT Name FROM ( SELECT Name , 90 AS LifeExpectancy FROM country WHERE Code IN ( SELECT Code FROM country ORDER BY 1.0 * GNP / Population DESC LIMIT 20 ) UNION ALL SELECT Name , LifeExpectancy FROM country WHERE Code NOT IN ( SELECT Code FROM country ORDER BY 1.0 * GNP / Population DESC LIMIT 20 ) ) WHERE LifeExpectancy >= 1.5 * ( SELECT LifeExpectancy FROM country WHERE name = \"Zambia\" )",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "GNP per capita is computed by dividing the GNP by the population."
  },
  {
    "input": "荷兰语不是最主要语言的国家中，哪个国家的国民生产总值的减少量最大？",
    "query": "SELECT Name FROM country WHERE Code NOT IN ( SELECT CountryCode FROM ( SELECT CountryCode , Language , MAX ( Percentage ) FROM countrylanguage GROUP BY CountryCode ) WHERE Language = \"Dutch\" ) ORDER BY GNPOld - GNP DESC LIMIT 1",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如阿鲁巴岛所有人都说荷兰语，荷兰语不是最主要语言的国家中，哪个国家的国民生产总值的减少量最大？",
    "query": "SELECT Name FROM country WHERE Code NOT IN ( SELECT CountryCode FROM ( SELECT CountryCode , Language , MAX ( Percentage ) FROM countrylanguage GROUP BY CountryCode ) WHERE Language = \"Dutch\" UNION SELECT Code FROM country WHERE name = \"Aruba\" ) ORDER BY GNPOld - GNP DESC LIMIT 1",
    "reasoning_type": "- H",
    "commonsense_knowledge": ""
  },
  {
    "input": "北美洲洲国民生产总值呈下降趋势的国家比南美洲多多少？",
    "query": "SELECT COUNT ( * ) - ( SELECT COUNT ( * ) FROM country WHERE GNP < GNPOld AND Continent = \"South America\" ) AS diff FROM country WHERE GNP < GNPOld AND Continent = \"North America\"",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如北美洲人口最多的前两个国家当前的国民生产总值增加2%，北美洲洲国民生产总值呈下降趋势的国家比南美洲多多少？",
    "query": "SELECT COUNT ( * ) - ( SELECT COUNT ( * ) FROM country WHERE GNP < GNPOld AND Continent = \"South America\" ) AS diff FROM ( SELECT Name , GNP * ( 1 + 0.02 ) AS GNP , GNPOld , Continent FROM country WHERE Continent = \"North America\" AND Code IN ( SELECT Code FROM country WHERE Continent = \"North America\" ORDER BY Population DESC LIMIT 2 ) UNION ALL SELECT Name , GNP , GNPOld , Continent FROM country WHERE Continent = \"North America\" AND Code NOT IN ( SELECT Code FROM country WHERE Continent = \"North America\" ORDER BY Population DESC LIMIT 2 ) ) WHERE GNP < GNPOld AND Continent = \"North America\"",
    "reasoning_type": "+ - * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "哪个大洲的人均国民生产总值增长率比欧洲高至少两个点？",
    "query": "SELECT Continent FROM country GROUP BY Continent HAVING 1.0 * ( SUM ( GNP ) / SUM ( Population ) - SUM ( GNPOld ) / SUM ( Population ) ) / ( SUM ( GNPOld ) / SUM ( Population ) ) >= ( SELECT 1.0 * ( SUM ( GNP ) / SUM ( Population ) - SUM ( GNPOld ) / SUM ( Population ) ) / ( SUM ( GNPOld ) / SUM ( Population ) ) FROM country WHERE Continent = \"Europe\" ) + 0.02",
    "reasoning_type": "+ - * / C",
    "commonsense_knowledge": "GNP per capita is computed by dividing the GNP by the population."
  },
  {
    "input": "假如人口预期寿命最长的前3个国家国民生产总值减少2%，哪个大洲的人均国民生产总值增长率比欧洲高至少两个点？",
    "query": "SELECT Continent FROM ( SELECT name , Continent , GNP * ( 1 - 0.02 ) AS GNP , Population , GNPOld FROM country WHERE Code IN ( SELECT Code FROM country ORDER BY LifeExpectancy DESC LIMIT 3 ) UNION ALL SELECT name , Continent , GNP , Population , GNPOld FROM country WHERE Code NOT IN ( SELECT Code FROM country ORDER BY LifeExpectancy DESC LIMIT 3 ) ) GROUP BY Continent HAVING 1.0 * ( SUM ( GNP ) / SUM ( Population ) - SUM ( GNPOld ) / SUM ( Population ) ) / ( SUM ( GNPOld ) / SUM ( Population ) ) >= ( SELECT 1.0 * ( SUM ( GNP ) / SUM ( Population ) - SUM ( GNPOld ) / SUM ( Population ) ) / ( SUM ( GNPOld ) / SUM ( Population ) ) FROM country WHERE Continent = \"Europe\" ) + 0.02",
    "reasoning_type": "+ - * / C H",
    "commonsense_knowledge": "GNP per capita is computed by dividing the GNP by the population."
  },
  {
    "input": "如果增长幅度保持不变，列出亚洲每个国家的名字、过去的国民生产总值、现在的国民生产总值，并预估一下未来的国民生产总值。",
    "query": "SELECT name , GNPOld , GNP , GNP + ( GNP - GNPOld ) AS GNPFuture FROM country WHERE Continent = \"Asia\"",
    "reasoning_type": "+ -",
    "commonsense_knowledge": ""
  },
  {
    "input": "如果增长幅度保持不变且以中文为主要语言的国家现在的国民生产总值是1000000.0，列出亚洲每个国家的名字、过去的国民生产总值、现在的国民生产总值，并预估一下未来的国民生产总值？",
    "query": "SELECT name , GNPOld , GNP , GNP + ( GNP - GNPOld ) AS GNPFuture FROM ( SELECT name , GNPOld , 1000000.0 AS GNP , Continent FROM country WHERE Code IN ( SELECT CountryCode FROM ( SELECT CountryCode , Language , MAX ( Percentage ) FROM countrylanguage GROUP BY CountryCode ) WHERE Language = \"Chinese\" ) UNION ALL SELECT name , GNPOld , GNP , Continent FROM country WHERE Code NOT IN ( SELECT CountryCode FROM ( SELECT CountryCode , Language , MAX ( Percentage ) FROM countrylanguage GROUP BY CountryCode ) WHERE Language = \"Chinese\" ) ) WHERE Continent = \"Asia\"",
    "reasoning_type": "+ - H",
    "commonsense_knowledge": ""
  },
  {
    "input": "英国的人口年增长率是0.4%，1年后英国的人口数量是多少？",
    "query": "SELECT Population * ( 1 + 0.004 ) AS population_in_1year FROM country WHERE name = \"United Kingdom\"",
    "reasoning_type": "+ *",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如欧洲人口预期寿命大于75的国家的人口数量为103000，英国的人口年增长率是0.4%，1年后英国的人口数量是多少？",
    "query": "SELECT Population * ( 1 + 0.004 ) AS population_in_1year FROM ( SELECT Continent , name , 103000 AS Population FROM country WHERE Continent = \"Europe\" AND LifeExpectancy > 75 UNION SELECT Continent , name , Population FROM country WHERE Continent = \"Europe\" AND LifeExpectancy <= 75 ) WHERE name = \"United Kingdom\"",
    "reasoning_type": "+ * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "按照赞比亚的预期寿命，出生于赞比亚独立那年的人的预期死亡年份是哪年？",
    "query": "SELECT CAST ( IndepYear + LifeExpectancy AS INT ) AS death_year FROM country WHERE name = \"Zambia\"",
    "reasoning_type": "+ C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如人均国民生产总值大于欧洲所有国家的平均人均国民生产总值的国家的人口预期寿命增加10年，按照赞比亚的预期寿命，出生于赞比亚独立那年的人的预期死亡年份是哪年？",
    "query": "SELECT CAST ( IndepYear + LifeExpectancy AS INT ) AS death_year FROM ( SELECT name , IndepYear , LifeExpectancy + 10 AS LifeExpectancy FROM country WHERE 1.0 * GNP / Population > ( SELECT 1.0 * SUM ( GNP ) / SUM ( Population ) FROM country WHERE Continent = \"Europe\" ) UNION ALL SELECT name , IndepYear , LifeExpectancy FROM country WHERE NOT ( 1.0 * GNP / Population > ( SELECT 1.0 * SUM ( GNP ) / SUM ( Population ) FROM country WHERE Continent = \"Europe\" ) ) ) WHERE name = \"Zambia\"",
    "reasoning_type": "+ * / C H",
    "commonsense_knowledge": "GNP per capita is computed by dividing the GNP by the population.  Age is calculated by subtracting date of birth from a given date."
  }
]