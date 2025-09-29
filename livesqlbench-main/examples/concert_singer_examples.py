concert_singer_examples =[
  {
    "input": "列出每个歌手的名字以及其在歌曲“Gentleman”发布的时候的年龄？",
    "query": "SELECT Name, Age + (SELECT Song_release_year FROM singer WHERE Song_Name = 'Gentleman') - strftime('%Y', 'now') AS target_age FROM singer",
    "reasoning_type": "- + C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如“Gentleman”这首歌是21世纪的第一年发布的，列出每个歌手的名字以及其在歌曲“Gentleman”发布的时候的年龄？",
    "query": "SELECT Name, Age + 2001 - strftime('%Y', 'now') AS target_age FROM singer",
    "reasoning_type": "- + C H",
    "commonsense_knowledge": "21st century began on 1 January 2001. Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "主题为“Free choice”的音乐会的参演歌手的名字分别是什么？他们当时多少岁？",
    "query": "SELECT C.Name, C.Age + (A.Year - strftime('%Y', 'now')) AS age_at_concert FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID WHERE A.Theme = 'Free choice'",
    "reasoning_type": "- + C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如1985年前出生的歌手都参加过主题为“Free choice”的音乐会，主题为“Free choice”的音乐会的参演歌手参演时多少岁？他们的名字分别是什么？",
    "query": "SELECT C.Name, C.Age + ((SELECT Year FROM concert WHERE Theme = 'Free choice') - strftime('%Y', 'now')) AS age_at_concert FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID WHERE A.Theme = 'Free choice' OR strftime('%Y', 'now') - C.Age < 1985 GROUP BY C.Name",
    "reasoning_type": "- + C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "最早的一次音乐会距今多少年了？",
    "query": "SELECT strftime('%Y', 'now') - MIN(Year) AS years FROM concert",
    "reasoning_type": "- C",
    "commonsense_knowledge": "The time duration is calculated by subtracting the start time from the end time."
  },
  {
    "input": "假如主题为“Wide Awake”的音乐会提前三年举办，最早的一次音乐会距今多少年了？",
    "query": "SELECT strftime('%Y', 'now') - MIN(Year) AS years FROM (SELECT Year - 3 AS Year FROM concert WHERE Theme = 'Wide Awake' UNION ALL SELECT Year FROM concert WHERE Theme != 'Wide Awake')",
    "reasoning_type": "- C H",
    "commonsense_knowledge": "The time duration is calculated by subtracting the start time from the end time."
  },
  {
    "input": "“Home Visits”音乐会20周年的时候，它的参演歌手多少岁了？同时给出参演歌手的名字。",
    "query": "SELECT C.Name, A.Year - strftime('%Y', 'now') + C.Age + 20 AS target_age FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID WHERE A.concert_Name = 'Home Visits'",
    "reasoning_type": "- + C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如参加过在斯塔克公园举行的音乐会的歌手全都参加过“Home Visits”音乐会，“Home Visits”音乐会20周年的时候，它的参演歌手都多少岁了？同时给出他们的名字。",
    "query": "SELECT C.Name, (SELECT Year FROM concert WHERE concert_Name = 'Home Visits') - strftime('%Y', 'now') + C.Age + 20 AS target_age FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID WHERE A.concert_Name = 'Home Visits' OR B.Singer_ID IN (SELECT C.Singer_ID FROM concert A JOIN stadium B ON A.Stadium_ID = B.Stadium_ID JOIN singer_in_concert C ON A.concert_ID = C.concert_ID WHERE B.Name = 'Stark''s Park') GROUP BY B.Singer_ID",
    "reasoning_type": "- + C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "巴尔穆尔场馆票价一张20美元，汉普登公园场馆票价一张5.5美元。满座的时候，巴尔穆尔场馆和汉普登公园场馆卖票一共能挣多少钱？",
    "query": "SELECT Capacity * 20 + (SELECT Capacity * 5.5 FROM stadium WHERE Name = 'Hampden Park') AS total FROM stadium WHERE Name = 'Balmoor'",
    "reasoning_type": "+ * C",
    "commonsense_knowledge": "Total price is calculated by multiplying quantity to unit price."
  },
  {
    "input": "巴尔穆尔场馆票价一张20美元，汉普登公园场馆票价一张5.5美元。假如汉普登公园场馆的容量是巴尔穆尔场馆的两倍，满座的时候，巴尔穆尔场馆和汉普登公园场馆卖票一共能挣多少钱？",
    "query": "SELECT Capacity * 20 + 2 * Capacity * 5.5 AS total FROM stadium WHERE Name = 'Balmoor'",
    "reasoning_type": "+ * C H",
    "commonsense_knowledge": "Total price is calculated by multiplying quantity to unit price."
  },
  {
    "input": "1980年前出生的歌手出演一场音乐会薪酬355美元，1980年及以后出生的歌手出演一场音乐会薪酬228美元。在萨默塞特公园场馆举办的音乐会给歌手付薪酬一共花了多少钱？",
    "query": "SELECT p1 + p2 AS cost FROM (SELECT 355 * (COUNT(*)) AS p1 FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON A.Stadium_ID = D.Stadium_ID WHERE D.Name = 'Somerset Park' AND strftime('%Y', 'now') - C.Age < 1980) JOIN (SELECT 228 * (COUNT(*)) AS p2 FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON A.Stadium_ID = D.Stadium_ID WHERE D.Name = 'Somerset Park' AND strftime('%Y', 'now') - C.Age >= 1980)",
    "reasoning_type": "- + * C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "1980年前出生的歌手出演一场音乐会薪酬355美元，1980年及以后出生的歌手出演一场音乐会薪酬228美元。假如贾斯汀·布朗比约翰·尼西尼克大3岁，在萨默塞特公园场馆举办的音乐会给歌手付薪酬一共花了多少？",
    "query": "SELECT p1 + p2 AS cost FROM (SELECT 355 * (COUNT(*)) AS p1 FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN (SELECT Singer_ID, Name, strftime('%Y', 'now') - Age AS birth_year FROM singer WHERE Name != 'Justin Brown' UNION ALL SELECT Singer_ID, Name, (SELECT strftime('%Y', 'now') - Age FROM singer WHERE Name = 'John Nizinik') - 3 AS birth_year FROM singer WHERE Name = 'Justin Brown') C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON A.Stadium_ID = D.Stadium_ID WHERE D.Name = 'Somerset Park' AND C.birth_year < 1980) JOIN (SELECT 228 * (COUNT(*)) AS p2 FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN (SELECT Singer_ID, Name, strftime('%Y', 'now') - Age AS birth_year FROM singer WHERE Name != 'Justin Brown' UNION ALL SELECT Singer_ID, Name, (SELECT strftime('%Y', 'now') - Age FROM singer WHERE Name = 'John Nizinik') - 3 AS birth_year FROM singer WHERE Name = 'Justin Brown') C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON A.Stadium_ID = D.Stadium_ID WHERE D.Name = 'Somerset Park' AND C.birth_year >= 1980)",
    "reasoning_type": "- + * C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "平均入座率最低和最高的场馆分别是哪个，它们分别开过几场音乐会？",
    "query": "SELECT * FROM (SELECT Name AS highest_name FROM stadium GROUP BY Stadium_ID ORDER BY 100.0 * Average / Capacity DESC LIMIT 1) JOIN (SELECT COUNT(*) AS concerts_in_highest_stadium FROM stadium A JOIN concert B ON A.Stadium_ID = B.Stadium_ID WHERE A.Stadium_ID = (SELECT Stadium_ID FROM stadium GROUP BY Stadium_ID ORDER BY 100.0 * Average / Capacity DESC LIMIT 1)) JOIN (SELECT Name AS lowest_name FROM stadium GROUP BY Stadium_ID ORDER BY 100.0 * Average / Capacity ASC LIMIT 1) JOIN (SELECT COUNT(*) AS concerts_in_lowest_stadium FROM stadium A JOIN concert B ON A.Stadium_ID = B.Stadium_ID WHERE A.Stadium_ID = (SELECT Stadium_ID FROM stadium GROUP BY Stadium_ID ORDER BY 100.0 * Average / Capacity ASC LIMIT 1))",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Attendance rate is calculated by dividing attendance amount by the capacity of the stadium."
  },
  {
    "input": "假如盖菲尔德公园场馆的容量是汉普登公园场馆的十分之一，平均入座率最低和最高的场馆分别是哪个，它们分别开过几场音乐会？",
    "query": "SELECT * FROM (SELECT Name AS highest_name FROM (SELECT Stadium_ID, Name, (SELECT Capacity FROM stadium WHERE Name = 'Hampden Park') / 10 AS Capacity, Average FROM stadium WHERE Name = 'Gayfield Park' UNION ALL SELECT Stadium_ID, Name, Capacity, Average FROM stadium WHERE Name != 'Gayfield Park') GROUP BY Stadium_ID ORDER BY 100.0 * Average / Capacity DESC LIMIT 1) JOIN (SELECT COUNT(*) AS concerts_in_highest_stadium FROM stadium A JOIN concert B ON A.Stadium_ID = B.Stadium_ID WHERE A.Stadium_ID = (SELECT Stadium_ID FROM (SELECT Stadium_ID, Name, (SELECT Capacity FROM stadium WHERE Name = 'Hampden Park') / 10 AS Capacity, Average FROM stadium WHERE Name = 'Gayfield Park' UNION ALL SELECT Stadium_ID, Name, Capacity, Average FROM stadium WHERE Name != 'Gayfield Park') GROUP BY Stadium_ID ORDER BY 100.0 * Average / Capacity DESC LIMIT 1)) JOIN (SELECT Name AS lowest_name FROM (SELECT Stadium_ID, Name, (SELECT Capacity FROM stadium WHERE Name = 'Hampden Park') / 10 AS Capacity, Average FROM stadium WHERE Name = 'Gayfield Park' UNION ALL SELECT Stadium_ID, Name, Capacity, Average FROM stadium WHERE Name != 'Gayfield Park') GROUP BY Stadium_ID ORDER BY 100.0 * Average / Capacity ASC LIMIT 1) JOIN (SELECT COUNT(*) AS concerts_in_lowest_stadium FROM stadium A JOIN concert B ON A.Stadium_ID = B.Stadium_ID WHERE A.Stadium_ID = (SELECT Stadium_ID FROM (SELECT Stadium_ID, Name, (SELECT Capacity FROM stadium WHERE Name = 'Hampden Park') / 10 AS Capacity, Average FROM stadium WHERE Name = 'Gayfield Park' UNION ALL SELECT Stadium_ID, Name, Capacity, Average FROM stadium WHERE Name != 'Gayfield Park') GROUP BY Stadium_ID ORDER BY 100.0 * Average / Capacity ASC LIMIT 1))",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "Attendance rate is calculated by dividing attendance amount by the capacity of the stadium."
  },
  {
    "input": "在萨默塞特公园场馆举办的每个音乐会的ID和名字分别是什么？每场音乐会中有百分之多少的歌手是女歌手？",
    "query": "SELECT t1.concert_ID, t1.concert_Name, 100.0 * n_female / n AS female_proportion FROM (SELECT A.concert_ID, A.concert_Name, COUNT(*) AS n_female FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON D.Stadium_ID = A.Stadium_ID WHERE D.Name = 'Somerset Park' AND C.Is_male = 'F' GROUP BY A.concert_ID UNION ALL SELECT A.concert_ID, A.concert_Name, 0 AS n_female FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON D.Stadium_ID = A.Stadium_ID WHERE D.Name = 'Somerset Park' AND A.concert_ID NOT IN (SELECT A.concert_ID FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON D.Stadium_ID = A.Stadium_ID WHERE D.Name = 'Somerset Park' AND C.Is_male = 'F' GROUP BY A.concert_ID) GROUP BY A.concert_ID) t1 JOIN (SELECT A.concert_ID, A.concert_Name, COUNT(*) AS n FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON D.Stadium_ID = A.Stadium_ID WHERE D.Name = 'Somerset Park' GROUP BY A.concert_ID) t2 ON t1.concert_ID = t2.concert_ID",
    "reasoning_type": "+ * /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如“Week 2”音乐会在萨默塞特公园场馆举办，在萨默塞特公园场馆举办的每个音乐会的ID和名字是什么，其中有百分之多少的歌手是女歌手？",
    "query": "SELECT t1.concert_ID, t1.concert_Name, 100.0 * n_female / n AS female_proportion FROM (SELECT A.concert_ID, A.concert_Name, COUNT(*) AS n_female FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON D.Stadium_ID = A.Stadium_ID WHERE (D.Name = 'Somerset Park' OR A.concert_Name = 'Week 2') AND C.Is_male = 'F' GROUP BY A.concert_ID UNION ALL SELECT A.concert_ID, A.concert_Name, 0 AS n_female FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON D.Stadium_ID = A.Stadium_ID WHERE (D.Name = 'Somerset Park' OR A.concert_Name = 'Week 2') AND A.concert_ID NOT IN (SELECT A.concert_ID FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON D.Stadium_ID = A.Stadium_ID WHERE (D.Name = 'Somerset Park' OR A.concert_Name = 'Week 2') AND C.Is_male = 'F' GROUP BY A.concert_ID) GROUP BY A.concert_ID) t1 JOIN (SELECT A.concert_ID, A.concert_Name, COUNT(*) AS n FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN singer C ON B.Singer_ID = C.Singer_ID JOIN stadium D ON D.Stadium_ID = A.Stadium_ID WHERE (D.Name = 'Somerset Park' OR A.concert_Name = 'Week 2') GROUP BY A.concert_ID) t2 ON t1.concert_ID = t2.concert_ID",
    "reasoning_type": "+ * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "总共有百分之多少的音乐会是在平均入座率前三的场馆举办的？",
    "query": "SELECT 100.0 * COUNT(*) / (SELECT COUNT(*) FROM concert) AS percent FROM concert WHERE Stadium_ID IN (SELECT Stadium_ID FROM stadium ORDER BY 100.0 * Average / Capacity DESC LIMIT 3)",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Attendance rate is calculated by dividing attendance amount by the capacity of the stadium."
  },
  {
    "input": "假如主题为“Bleeding Love”的音乐会在格里公园举办，总共有百分之多少的音乐会是在平均入座率前三的场馆举办的？",
    "query": "SELECT 100.0 * COUNT(*) / (SELECT COUNT(*) FROM concert) AS percent FROM (SELECT Stadium_ID FROM stadium WHERE Name = 'Glebe Park' UNION ALL SELECT Stadium_ID FROM concert WHERE Theme != 'Bleeding Love') WHERE Stadium_ID IN (SELECT Stadium_ID FROM stadium ORDER BY 100.0 * Average / Capacity DESC LIMIT 3)",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "Attendance rate is calculated by dividing attendance amount by the capacity of the stadium."
  },
  {
    "input": "哪个场馆去演唱过的歌手数量不少于去格里公园场馆唱过的歌手数量的三倍？",
    "query": "SELECT C.Name FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN stadium C ON A.Stadium_ID = C.Stadium_ID GROUP BY C.Stadium_ID HAVING COUNT(DISTINCT(B.Singer_ID)) >= 3 * (SELECT COUNT(DISTINCT(B.Singer_ID)) FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN stadium C ON A.Stadium_ID = C.Stadium_ID WHERE C.Name = 'Glebe Park')",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如去过萨默塞特公园场馆演唱的歌手都去过巴尔穆尔场馆，哪个场馆去演唱过歌手数量不少于格里公园场馆的三倍？列出这些场馆的名字。",
    "query": "SELECT Name FROM (SELECT C.Stadium_ID, B.Singer_ID, C.Name FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN stadium C ON A.Stadium_ID = C.Stadium_ID UNION ALL SELECT (SELECT Stadium_ID FROM stadium WHERE Name = 'Balmoor'), B.Singer_ID, C.Name FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN stadium C ON A.Stadium_ID = C.Stadium_ID WHERE C.Name = 'Somerset Park') GROUP BY Stadium_ID HAVING COUNT(DISTINCT(Singer_ID)) >= 3 * (SELECT COUNT(DISTINCT(B.Singer_ID)) FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID JOIN stadium C ON A.Stadium_ID = C.Stadium_ID WHERE C.Name = 'Glebe Park')",
    "reasoning_type": "* H",
    "commonsense_knowledge": ""
  },
  {
    "input": "哪个场馆的最高入座率比巴尔穆尔场馆的最高入座率两倍还多？列出这些场馆的名字。",
    "query": "SELECT Name FROM stadium WHERE 100.0 * Highest / Capacity > 2 * (SELECT 100.0 * Highest / Capacity FROM stadium WHERE Name = 'Balmoor')",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Attendance rate is calculated by dividing attendance amount by the capacity of the stadium."
  },
  {
    "input": "假如巴尔穆尔场馆的容量是5600，哪个场馆的最高入座率比巴尔穆尔场馆的最高入座率两倍还多？列出这些场馆的名字。",
    "query": "SELECT Name FROM stadium WHERE 100.0 * Highest / Capacity > 2 * (SELECT 100.0 * Highest / 5600 FROM stadium WHERE Name = 'Balmoor')",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "Attendance rate is calculated by dividing attendance amount by the capacity of the stadium."
  },
  {
    "input": "哪场2012年后举办的音乐会的歌手数量比“Happy Tonight”主题音乐会歌手数量多，是它的多少倍？同时给出音乐会的ID和全名。",
    "query": "SELECT A.concert_ID, A.concert_Name, 1.0 * COUNT(DISTINCT(B.Singer_ID)) / (SELECT COUNT(DISTINCT(B.Singer_ID)) FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID WHERE A.Theme = 'Happy Tonight') AS times FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID WHERE A.Year > 2012 GROUP BY A.concert_ID HAVING COUNT(DISTINCT(B.Singer_ID)) > (SELECT COUNT(DISTINCT(B.Singer_ID)) FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID WHERE A.Theme = 'Happy Tonight')",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如每场音乐会都有歌手乔·夏普，哪场2012年后举办的音乐会的歌手数量比“Happy Tonight”主题音乐会歌手数量多，是它的多少倍？同时给出这些音乐会的ID和全名。",
    "query": "SELECT A.concert_ID, A.concert_Name, 1.0 * (COUNT(DISTINCT(B.Singer_ID)) + 1) / (SELECT COUNT(DISTINCT(B.Singer_ID)) + 1 FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID WHERE A.Theme = 'Happy Tonight' AND B.Singer_ID != (SELECT Singer_ID FROM singer WHERE Name = 'Joe Sharp')) AS times FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID WHERE A.Year > 2012 AND B.Singer_ID != (SELECT Singer_ID FROM singer WHERE Name = 'Joe Sharp') GROUP BY A.concert_ID HAVING (COUNT(DISTINCT(B.Singer_ID)) + 1) > (SELECT COUNT(DISTINCT(B.Singer_ID)) + 1 FROM concert A JOIN singer_in_concert B ON A.concert_ID = B.concert_ID WHERE A.Theme = 'Happy Tonight' AND B.Singer_ID != (SELECT Singer_ID FROM singer WHERE Name = 'Joe Sharp'))",
    "reasoning_type": "+ * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "“Love”这首歌发布的时候哪些歌手的年龄比这首歌的演唱者的两倍还大？列出这些歌手的名字。",
    "query": "SELECT Name FROM singer WHERE (SELECT Song_release_year FROM singer WHERE Song_Name = 'Love') - (strftime('%Y', 'now') - Age) > 2 * (SELECT Age - (strftime('%Y', 'now') - Song_release_year) FROM singer WHERE Song_Name = 'Love')",
    "reasoning_type": "- * C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如“Love”发布于2010年，“Love”这首歌发布的时候哪些歌手的年龄比这首歌的演唱者的两倍还大？列出这些歌手的名字。",
    "query": "SELECT Name FROM singer WHERE 2010 - (strftime('%Y', 'now') - Age) > 2 * (SELECT Age - (strftime('%Y', 'now') - 2010) FROM singer WHERE Song_Name = 'Love')",
    "reasoning_type": "- * C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  }
]