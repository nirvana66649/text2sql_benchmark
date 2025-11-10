formula_1_examples=[
  {
    "input": "五年后，刘易斯·汉密尔顿多大了？",
    "query": "SELECT strftime('%Y', 'now') + 5 - substr(dob, 7, 4) + (strftime('%m', 'now') > substr(dob, 4, 2) OR (strftime('%m', 'now') = substr(dob, 4, 2) AND strftime('%d', 'now') >= substr(dob, 1, 2))) AS age FROM drivers WHERE forename = 'Lewis' AND surname = 'Hamilton'",
    "reasoning_type": "+ - C",
    "commonsense_knowledge": "Age is computed by subtracting the date of birth from the given date."
  },
  {
    "input": "五年后，刘易斯·汉密尔顿多大了，假如他出生于2020年1月1日？",
    "query": "SELECT strftime('%Y', 'now') + 5 - 2020 + (strftime('%m', 'now') > '01' OR (strftime('%m', 'now') = '01' AND strftime('%d', 'now') >= '01')) AS age FROM drivers WHERE forename = 'Lewis' AND surname = 'Hamilton'",
    "reasoning_type": "+ - C H",
    "commonsense_knowledge": "Age is computed by subtracting the date of birth from the given date."
  },
  {
    "input": "在2009年澳大利亚大奖赛资格赛中，排名第一的车手在三场比赛中的平均圈速是多少？",
    "query": "SELECT time((strftime('%s', '00:0' || q1) + strftime('%s', '00:0' || q2) + strftime('%s', '00:0' || q3)) / 3.0, 'unixepoch') AS avg_lap FROM qualifying A JOIN races B ON A.raceId = B.raceId WHERE B.name = 'Australian Grand Prix' AND B.year = '2009' AND A.position = '1'",
    "reasoning_type": "+ /",
    "commonsense_knowledge": ""
  },
  {
    "input": "在2009年澳大利亚大奖赛资格赛中，排名第一的车手在三场比赛中的平均圈速是多少，假设他在q1中的圈速是1:26.026？",
    "query": "SELECT time((strftime('%s', '00:01:26.026') + strftime('%s', '00:0' || q2) + strftime('%s', '00:0' || q3)) / 3.0, 'unixepoch') AS avg_lap FROM qualifying A JOIN races B ON A.raceId = B.raceId WHERE B.name = 'Australian Grand Prix' AND B.year = '2009' AND A.position = '1'",
    "reasoning_type": "+ / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "最靠近北回归线的赛道的名称和位置是什么？",
    "query": "SELECT name, location FROM circuits ORDER BY ABS(lat - 23.4394) ASC LIMIT 1",
    "reasoning_type": "- C",
    "commonsense_knowledge": "The Tropic of Cancer lies at 23.4394 degrees north of the Equator. The north latitude is positive, and the south latitude is negative."
  },
  {
    "input": "离南回归线最远的赛道叫什么名字？",
    "query": "SELECT name FROM circuits ORDER BY ABS(lat - (-23.4394)) DESC LIMIT 1",
    "reasoning_type": "- C",
    "commonsense_knowledge": "The Tropic of Capricorn lies at 23.4394 degrees south of the Equator. The north latitude is positive, and the south latitude is negative."
  },
  {
    "input": "2009年和2010年分别举行了多少场比赛？它们相差多少？",
    "query": "SELECT n_2009, n_2010, ABS(n_2009 - n_2010) AS diff FROM (SELECT COUNT(*) AS n_2009 FROM races WHERE year = '2009') JOIN (SELECT COUNT(*) AS n_2010 FROM races WHERE year = '2010')",
    "reasoning_type": "- C",
    "commonsense_knowledge": "Difference between two values should be an absolute value."
  },
  {
    "input": "2009年和2010年分别举行了多少场比赛？它们相差多少假如2010年再多举行了5场比赛？",
    "query": "SELECT n_2009, n_2010 + 5, ABS(n_2010 + 5 - n_2009) AS diff FROM (SELECT COUNT(*) AS n_2009 FROM races WHERE year = '2009') JOIN (SELECT COUNT(*) AS n_2010 FROM races WHERE year = '2010')",
    "reasoning_type": "- + C H",
    "commonsense_knowledge": "Difference between two values should be an absolute value."
  },
  {
    "input": "法国比意大利多举行了多少场比赛？",
    "query": "SELECT n_france - n_italy FROM (SELECT COUNT(*) AS n_france FROM races A JOIN circuits B ON A.circuitId = B.circuitId WHERE B.country = 'France') JOIN (SELECT COUNT(*) AS n_italy FROM races A JOIN circuits B ON A.circuitId = B.circuitId WHERE B.country = 'Italy')",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "北半球和南半球分别举行了多少场比赛？它们相差多少？",
    "query": "SELECT n_north, n_south, n_north - n_south FROM (SELECT COUNT(*) AS n_north FROM races A JOIN circuits B ON A.circuitId = B.circuitId WHERE B.lat > 0) JOIN (SELECT COUNT(*) AS n_south FROM races A JOIN circuits B ON A.circuitId = B.circuitId WHERE B.lat < 0)",
    "reasoning_type": "- C",
    "commonsense_knowledge": "The Northern Hemisphere runs from 0 degree latitude to 90 degrees North and the Southern Hemisphere from 0 degree latitude to 90 degree South. The north latitude is positive, and the south latitude is negative."
  },
  {
    "input": "在2006年英国大奖赛资格赛第一轮比赛中，给出速度最快、最慢的车手的姓，名，以及他们圈速的差距。",
    "query": "SELECT forename_slowest, surname_slowest, forename_fastest, surname_fastest, time((strftime('%s', '00:0' || slowest_q1) - strftime('%s', '00:0' || fastest_q1)), 'unixepoch') AS diff FROM (SELECT MAX(A.q1) AS slowest_q1, D.forename AS forename_slowest, D.surname AS surname_slowest FROM qualifying A JOIN races B ON A.raceId = B.raceId JOIN drivers D ON A.driverId = D.driverId WHERE B.name = 'British Grand Prix' AND B.year = '2006') JOIN (SELECT MIN(A.q1) AS fastest_q1, D.forename AS forename_fastest, D.surname AS surname_fastest FROM qualifying A JOIN races B ON A.raceId = B.raceId JOIN drivers D ON A.driverId = D.driverId WHERE B.name = 'British Grand Prix' AND B.year = '2006' AND A.q1 != '')",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "哪些国家的赛道数量是日本的两倍多？",
    "query": "SELECT B.country FROM circuits B, (SELECT COUNT(*) AS n_japan FROM circuits WHERE country = 'Japan') GROUP BY B.country HAVING COUNT(*) > 2 * n_japan",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "假设日本有2条赛道，那么哪些国家的赛道数量是日本的两倍多？",
    "query": "SELECT country FROM circuits GROUP BY country HAVING COUNT(*) > 2 * 2",
    "reasoning_type": "* H",
    "commonsense_knowledge": ""
  },
  {
    "input": "列出圈速超过最低圈速记录1.5倍的车手的姓和名。",
    "query": "SELECT DISTINCT B.forename, B.surname FROM results A JOIN drivers B ON A.driverId = B.driverId WHERE milliseconds != '' AND CAST(milliseconds AS INTEGER) > 1.5 * (SELECT MIN(CAST(milliseconds AS INTEGER)) FROM results WHERE milliseconds != '')",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "假设最低圈速记录为93000毫秒，请列出圈速超过最低圈速记录1.5倍的驾驶员姓和名。",
    "query": "SELECT DISTINCT B.forename, B.surname FROM results A JOIN drivers B ON A.driverId = B.driverId WHERE CAST(milliseconds AS INTEGER) > 1.5 * 93000",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "列出比赛次数比葡萄牙首都的比赛次数的三倍多的地点和比赛次数。",
    "query": "SELECT B.location, COUNT(*) AS num_races FROM races A JOIN circuits B ON A.circuitId = B.circuitId GROUP BY B.location HAVING COUNT(*) > 3 * (SELECT COUNT(*) FROM races A JOIN circuits B ON A.circuitId = B.circuitId WHERE B.location = 'Lisbon')",
    "reasoning_type": "* C",
    "commonsense_knowledge": "Lisbon is the capital of Portugal."
  },
  {
    "input": "如果在里斯本举行了5场比赛，列出比赛次数比葡萄牙首都的比赛次数的三倍多的地点和比赛次数。",
    "query": "SELECT B.location, COUNT(*) AS num_races FROM races A JOIN circuits B ON A.circuitId = B.circuitId GROUP BY B.location HAVING COUNT(*) > 3 * 5",
    "reasoning_type": "* C H",
    "commonsense_knowledge": "Lisbon is the capital of Portugal."
  },
  {
    "input": "刘易斯·汉密尔顿参加了多少场比赛？他有多少次获得了第一名？他获得第一名的概率是多少？",
    "query": "SELECT num_matches, num_no1, 1.0 * num_no1 / num_matches AS possibility FROM (SELECT COUNT(*) AS num_matches FROM results A JOIN drivers B ON A.driverId = B.driverId WHERE B.surname = 'Hamilton' AND B.forename = 'Lewis') JOIN (SELECT COUNT(*) AS num_no1 FROM results A JOIN drivers B ON A.driverId = B.driverId WHERE B.surname = 'Hamilton' AND B.forename = 'Lewis' AND A.rank = '1')",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Probability is calculated by dividing the number of ways the event can occur by the total number of outcomes."
  },
  {
    "input": "美国的赛道数量是世界上陆地面积最大的国家的多少倍？",
    "query": "SELECT 1.0 * (SELECT COUNT(*) FROM circuits WHERE country = 'USA') / COUNT(*) AS ratio FROM circuits WHERE country = 'Russia'",
    "reasoning_type": "/ * C",
    "commonsense_knowledge": "The largest country in the world is Russia."
  },
  {
    "input": "假设美国有2个赛道，美国的赛道数量是世界上陆地面积最大的国家的多少倍？",
    "query": "SELECT 1.0 * 2 / COUNT(*) AS ratio FROM circuits WHERE country = 'Russia'",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "The largest country in the world is Russia."
  },
  {
    "input": "在与著名足球运动员克里斯蒂亚诺·罗纳尔多拥有相同国籍的车手中，参加过2006年美国大奖赛的选手是没有参加过的选手的多少倍？",
    "query": "SELECT 1.0 * n_p / (n_all - n_p) FROM (SELECT COUNT(DISTINCT A.driverId) AS n_p FROM drivers A JOIN results B ON A.driverId = B.driverId JOIN races C ON B.raceId = C.raceId WHERE A.nationality = 'Portuguese' AND C.name = 'United States Grand Prix' AND C.year = '2006') JOIN (SELECT COUNT(DISTINCT A.driverId) AS n_all FROM drivers A WHERE A.nationality = 'Portuguese')",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Cristiano Ronaldo is a Portuguese professional footballer."
  },
  {
    "input": "在乔治·W·布什担任总统期间，美国举办了多少场比赛？是英国举办的比赛的多少倍？",
    "query": "SELECT COUNT(*) AS usa_races, 1.0 * COUNT(*) / (SELECT COUNT(*) FROM races A JOIN circuits B ON A.circuitId = B.circuitId WHERE A.year BETWEEN 2001 AND 2009 AND country = 'UK') AS ratio FROM races A JOIN circuits B ON A.circuitId = B.circuitId WHERE A.year BETWEEN 2001 AND 2009 AND country = 'USA'",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "George W. Bush's tenure as the 43rd president of the United States began with his first inauguration on January 20, 2001, and ended on January 20, 2009."
  },
  {
    "input": "在乔治·布什担任总统期间，美国举办了多少场比赛？是英国举办的比赛的多少倍，假如英国那段时间举办了10次比赛？",
    "query": "SELECT COUNT(*) AS usa_races, 1.0 * COUNT(*) / 10 AS ratio FROM races A JOIN circuits B ON A.circuitId = B.circuitId WHERE A.year BETWEEN 2001 AND 2009 AND country = 'USA'",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "George W. Bush's tenure as the 43rd president of the United States began with his first inauguration on January 20, 2001, and ended on January 20, 2009."
  },
  {
    "input": "请提供参加过的比赛次数至少是艾伦·伯格的两倍且与著名的歌手迈克尔·杰克逊具有相同国籍的车手的ID、名字、比赛次数。",
    "query": "SELECT A.driverId, forename AS first_name, COUNT(*) AS n_races FROM drivers A JOIN results B ON A.driverId = B.driverId WHERE A.nationality = 'American' GROUP BY A.driverId HAVING COUNT(*) >= 2 * (SELECT COUNT(*) FROM drivers A JOIN results B ON A.driverId = B.driverId WHERE A.forename = 'Allen' AND A.surname = 'Berg')",
    "reasoning_type": "* C",
    "commonsense_knowledge": "Michael Joseph Jackson was an American singer, songwriter, dancer, and philanthropist."
  },
  {
    "input": "假设艾伦·伯格参加了10场比赛，请提供参加过的比赛次数至少是艾伦·伯格的两倍且与著名的歌手迈克尔·约瑟夫·杰克逊具有相同国籍的车手的ID、名字、比赛次数。",
    "query": "SELECT A.driverId, forename AS first_name, COUNT(*) AS n_races FROM drivers A JOIN results B ON A.driverId = B.driverId WHERE A.nationality = 'American' GROUP BY A.driverId HAVING COUNT(*) >= 2 * 10",
    "reasoning_type": "* C H",
    "commonsense_knowledge": "Michael Joseph Jackson was an American singer, songwriter, dancer, and philanthropist."
  }
]