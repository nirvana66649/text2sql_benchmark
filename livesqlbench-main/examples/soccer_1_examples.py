soccer_1_examples=[
  {
    "input": "传球得分包括5%的弧线球、5%的任意球精度、15%的长传、20%的传中、20%的视野和35%的短传。列出传球得分最高的前10名球员的姓名和当前年龄。",
    "query": "SELECT name , age FROM ( SELECT B.player_name AS name , MAX ( 0.05 * A.curve + 0.05 * A.free_kick_accuracy + 0.15 * A.long_passing + 0.2 * A.crossing + 0.2 * A.vision + 0.35 * A.short_passing ) AS passing_rating , DATE ( \"now\" ) - strftime ( \"%Y-%m-%d\" , B.birthday ) AS age FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id GROUP BY B.player_name ORDER BY passing_rating DESC LIMIT 10 )",
    "reasoning_type": "+ - * C",
    "commonsense_knowledge": "Current age is computed by substracting the date of birth from current date."
  },
  {
    "input": "传球得分包括5%的弧线球、5%的任意球精度、15%的长传、20%的传中、20%的视野和35%的短传。假如所有球员的视野都是80分，列出传球得分最高的前10名球员的姓名和当前年龄。",
    "query": "SELECT name , age FROM ( SELECT B.player_name AS name , MAX ( 0.05 * A.curve + 0.05 * A.free_kick_accuracy + 0.15 * A.long_passing + 0.2 * A.crossing + 0.2 * 80 + 0.35 * A.short_passing ) AS passing_rating , DATE ( \"now\" ) - strftime ( \"%Y-%m-%d\" , B.birthday ) AS age FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id GROUP BY B.player_name ORDER BY passing_rating DESC LIMIT 10 )",
    "reasoning_type": "+ - * C H",
    "commonsense_knowledge": "Current age is computed by substracting the date of birth from current date."
  },
  {
    "input": "速度评分包括45%的加速评分和55%的冲刺速度评分。列出速度排名前三的选手的名字，并列出他们的身高、体重和体重指数。",
    "query": "SELECT player_name , height , weight , BMI FROM ( SELECT B.player_name , MAX ( 0.45 * A.acceleration + 0.55 * A.sprint_speed ) AS pace_rating , B.height , B.weight , B.weight * 0.45 / ( ( 1.0 * B.height / 100 ) * ( 1.0 * B.height / 100 ) ) AS BMI FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id GROUP BY B.player_name ) ORDER BY pace_rating DESC LIMIT 3",
    "reasoning_type": "+ * / C",
    "commonsense_knowledge": "Body mass index is weight in pounds divided by height in meters squared and multiplying by a conversion factor 0.45."
  },
  {
    "input": "速度评分包括45%的加速评分和55%的冲刺速度评分。假如所有球员的加速评分都是75分，列出速度排名前三的球员的名字，并列出他们的身高、体重和体重指数。",
    "query": "SELECT player_name , height , weight , BMI FROM ( SELECT B.player_name , MAX ( 0.45 * 75 + 0.55 * A.sprint_speed ) AS pace_rating , B.height , B.weight , B.weight * 0.45 / ( ( 1.0 * B.height / 100 ) * ( 1.0 * B.height / 100 ) ) AS BMI FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id GROUP BY B.player_name ) ORDER BY pace_rating DESC LIMIT 3",
    "reasoning_type": "+ * / C H",
    "commonsense_knowledge": "Body mass index is weight in pounds divided by height in meters squared and multiplying by a conversion factor 0.45."
  },
  {
    "input": "列出整体评分和潜在能力差异最大的前三名球员的名字，并列出差异。",
    "query": "SELECT B.player_name , MAX ( ABS ( A.potential - A.overall_rating ) ) AS difference FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id GROUP BY B.player_name ORDER BY difference DESC LIMIT 3",
    "reasoning_type": "- C",
    "commonsense_knowledge": "Diffenrence between two values should be an absolute value."
  },
  {
    "input": "假如总评分低于70的球员的总评分增加了5分，列出总评分和潜在能力差异最大的前三名球员的名字。",
    "query": "SELECT player_name , MAX ( difference ) FROM ( SELECT B.player_name , ABS ( A.overall_rating - A.potential ) AS difference FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.overall_rating >= 70 UNION SELECT B.player_name , ABS ( A.overall_rating + 5 - A.potential ) AS difference FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.overall_rating < 70 ) GROUP BY player_name ORDER BY difference DESC LIMIT 3",
    "reasoning_type": "+ - C H",
    "commonsense_knowledge": "Diffenrence between two values should be an absolute value."
  },
  {
    "input": "评分80到89分表示非常好。在过人不失球能力非常好的球员中，左脚球员有多少，右脚球员有多少，相差多少？",
    "query": "SELECT left_footed , right_footed , ABS ( left_footed - right_footed ) AS difference FROM ( SELECT COUNT ( DISTINCT ( B.player_name ) ) AS left_footed FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.dribbling BETWEEN 80 AND 89 AND A.preferred_foot = \"left\" ) JOIN ( SELECT COUNT ( DISTINCT ( B.player_name ) ) AS right_footed FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.dribbling BETWEEN 80 AND 89 AND A.preferred_foot = \"right\" )",
    "reasoning_type": "- C",
    "commonsense_knowledge": "(1) Dribbling attribute describes how well a player can pass without conceding the ball and (2) diffenrence between two values should be an absolute value."
  },
  {
    "input": "就干净接球和扑救时正确站位的能力而言，哪名守门员的总得分最高？给出他的名字。",
    "query": "SELECT player_name FROM ( SELECT B.player_name , MAX ( A.positioning + A.gk_handling ) AS goalkeeper_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id GROUP BY B.player_name ) ORDER BY goalkeeper_rating DESC LIMIT 1",
    "reasoning_type": "+ C",
    "commonsense_knowledge": "Position attribute for a goalkeeper is the ability to position correctly for saves. Handling is an exclusive goalkeeper attribute used to measure how clean he catches the ball."
  },
  {
    "input": "在比赛中累得最快的球员的名字是什么，他在远射准确度和射门力量方面的总得分是多少？",
    "query": "SELECT B.player_name , A.long_shots + A.shot_power AS total_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE NOT ( A.stamina IS NULL ) ORDER BY A.stamina ASC LIMIT 1",
    "reasoning_type": "+ C",
    "commonsense_knowledge": "Stamina attribute determines the rate at which a player will tire during a game."
  },
  {
    "input": "在比赛中累得最快的球员的名字是什么，如果他的远射准确度评分是90，他在远射准确度和射门力量方面的总得分是多少？",
    "query": "SELECT B.player_name , 90 + A.shot_power AS total_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE NOT ( A.stamina IS NULL ) ORDER BY A.stamina ASC LIMIT 1",
    "reasoning_type": "+ C H",
    "commonsense_knowledge": "Stamina attribute determines the rate at which a player will tire during a game."
  },
  {
    "input": "防守评分由压力、侵略性和球队宽度的评分组成。提供防守得分最高和最低的球队的缩写。",
    "query": "SELECT best_team_name , lowest_team_name FROM ( SELECT B.team_short_name AS best_team_name , A.defencePressure + A.defenceAggression + A.defenceTeamWidth AS defensive_rating FROM Team_Attributes A JOIN Team B ON A.team_fifa_api_id = B.team_fifa_api_id ORDER BY defensive_rating DESC LIMIT 1 ) JOIN ( SELECT B.team_short_name AS lowest_team_name , A.defencePressure + A.defenceAggression + A.defenceTeamWidth AS defensive_rating FROM Team_Attributes A JOIN Team B ON A.team_fifa_api_id = B.team_fifa_api_id ORDER BY defensive_rating ASC LIMIT 1 )",
    "reasoning_type": "+",
    "commonsense_knowledge": ""
  },
  {
    "input": "在使用自由式创造机会位置战术的球队中，哪支球队在进攻速度和盘带方面的综合得分最高？请提供球队的全名和综合得分。",
    "query": "SELECT B.team_long_name , A.buildUpPlaySpeed + A.buildUpPlayDribbling AS combined_rating FROM Team_Attributes A JOIN Team B ON A.team_fifa_api_id = B.team_fifa_api_id WHERE A.chanceCreationPositioningClass = \"Free Form\" ORDER BY A.buildUpPlaySpeed + A.buildUpPlayDribbling DESC LIMIT 1",
    "reasoning_type": "+",
    "commonsense_knowledge": ""
  },
  {
    "input": "在使用自由式创造机会位置战术的球队中，哪支球队在进攻速度和盘带方面的综合得分最高，假设所有球队盘带方面的得分是60？请提供球队的全名和综合得分。",
    "query": "SELECT B.team_long_name , A.buildUpPlaySpeed + 60 AS combined_rating FROM Team_Attributes A JOIN Team B ON A.team_fifa_api_id = B.team_fifa_api_id WHERE A.chanceCreationPositioningClass = \"Free Form\" ORDER BY A.buildUpPlaySpeed + 60 DESC LIMIT 1",
    "reasoning_type": "+ H",
    "commonsense_knowledge": ""
  },
  {
    "input": "射门评分由6个属性组成，包括45%的射门精度、20%的远射、5%的点球、5%的跑位、20%的射门力量和5%的凌空射门。射门评分最高的球员的名字和评分是多少？",
    "query": "SELECT B.player_name , 0.45 * A.finishing + 0.2 * A.long_shots + 0.05 * penalties + 0.05 * positioning + 0.2 * shot_power + 0.05 * volleys AS shooting_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id ORDER BY shooting_rating DESC LIMIT 1",
    "reasoning_type": "+ *",
    "commonsense_knowledge": ""
  },
  {
    "input": "射门评分由5个属性组成，包括45%的射门精度、20%的远射、5%的点球、5%的跑位、20%的射门力量和5%的凌空射门。如果把所有球员射门属性中的最薄弱一项提高五分，那么射门评分最高的球员的名字和评分是多少？",
    "query": "SELECT player_name , MAX ( shooting_rating ) FROM ( SELECT B.player_name , MAX ( 0.45 * ( finishing + 5 ) + 0.2 * long_shots + 0.05 * penalties + 0.05 * positioning + 0.2 * shot_power + 0.05 * volleys ) AS shooting_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE finishing <= long_shots AND finishing <= penalties AND finishing <= positioning AND finishing <= shot_power AND finishing <= volleys UNION ALL SELECT B.player_name , MAX ( 0.45 * finishing + 0.2 * ( long_shots + 5 ) + 0.05 * penalties + 0.05 * positioning + 0.2 * shot_power + 0.05 * volleys ) AS shooting_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE long_shots <= finishing AND long_shots <= penalties AND long_shots <= positioning AND long_shots <= shot_power AND long_shots <= volleys UNION ALL SELECT B.player_name , MAX ( 0.45 * finishing + 0.2 * long_shots + 0.05 * ( penalties + 5 ) + 0.05 * positioning + 0.2 * shot_power + 0.05 * volleys ) AS shooting_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE penalties <= finishing AND penalties <= long_shots AND penalties <= positioning AND penalties <= shot_power AND penalties <= volleys UNION ALL SELECT B.player_name , MAX ( 0.45 * finishing + 0.2 * long_shots + 0.05 * penalties + 0.05 * ( positioning + 5 ) + 0.2 * shot_power + 0.05 * volleys ) AS shooting_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE positioning <= finishing AND positioning <= long_shots AND positioning <= penalties AND positioning <= shot_power AND positioning <= volleys UNION ALL SELECT B.player_name , MAX ( 0.45 * finishing + 0.2 * long_shots + 0.05 * penalties + 0.05 * positioning + 0.2 * ( shot_power + 5 ) + 0.05 * volleys ) AS shooting_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE shot_power <= finishing AND shot_power <= long_shots AND shot_power <= penalties AND shot_power <= positioning AND shot_power <= volleys UNION ALL SELECT B.player_name , MAX ( 0.45 * finishing + 0.2 * long_shots + 0.05 * penalties + 0.05 * positioning + 0.2 * shot_power + 0.05 * ( volleys + 5 ) ) AS shooting_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE volleys <= finishing AND volleys <= long_shots AND volleys <= penalties AND volleys <= positioning AND volleys <= shot_power )",
    "reasoning_type": "+ * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "对周围队友和对手的位置认知最好和最差的球员的长传得分是多少？他们相差多少？",
    "query": "SELECT best_vision_long_passing , worst_vision_long_passing , ABS ( worst_vision_long_passing - best_vision_long_passing ) AS diff FROM ( SELECT A.long_passing AS best_vision_long_passing , MAX ( A.vision ) FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id ) JOIN ( SELECT A.long_passing AS worst_vision_long_passing , MIN ( A.vision ) FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id )",
    "reasoning_type": "- C",
    "commonsense_knowledge": "(1) Vision ranks the player’s awareness of the position of his teammates and opponents around him and (2) diffenrence between two values should be an absolute value."
  },
  {
    "input": "在进攻得分中等的球员中，身体强壮程度指标的最高得分和最低得分之间的比例是多少？",
    "query": "SELECT 1.0 * max_strength / min_strength AS ratio FROM ( SELECT MAX ( A.strength ) AS max_strength FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.attacking_work_rate = \"medium\" ) JOIN ( SELECT MIN ( A.strength ) AS min_strength FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.attacking_work_rate = \"medium\" )",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Strength is about the quality or state of physical strength."
  },
  {
    "input": "评分在80到89分之间意味着非常好。评分在70到79分之间表示良好。罚球区内射门准确度非常好的球员数量与准确度良好的球员数量的比例是多少？",
    "query": "SELECT 1.0 * very_good / good AS proportion FROM ( SELECT COUNT ( * ) AS very_good FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.penalties BETWEEN 80 AND 89 ) JOIN ( SELECT COUNT ( * ) AS good FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.penalties BETWEEN 70 AND 79 )",
    "reasoning_type": "/ * C",
    "commonsense_knowledge": "Penalties attribute measures the accuracy of shots from inside the penalty area."
  },
  {
    "input": "最高的选手比最矮的选手重多少倍？",
    "query": "SELECT 1.0 * highest_weight / lowest_weight AS times FROM ( SELECT weight AS highest_weight , MAX ( height ) FROM Player ) JOIN ( SELECT weight AS lowest_weight , MIN ( height ) FROM Player )",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "最高的选手比最矮的选手重多少倍，假如最高的选手重170磅？",
    "query": "SELECT 170.0 / lowest_weight AS times FROM ( SELECT weight AS lowest_weight , MIN ( height ) FROM Player )",
    "reasoning_type": "/ H",
    "commonsense_knowledge": ""
  },
  {
    "input": "列出体重指数最高的球员的姓名、身高、体重和整体评分。",
    "query": "SELECT B.player_name , B.height , B.weight , A.overall_rating FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id JOIN ( SELECT B.player_fifa_api_id , B.weight * 0.45 / ( ( B.height / 100 ) * ( B.height / 100 ) ) AS BMI FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id ) AS C ON A.player_fifa_api_id = C.player_fifa_api_id ORDER BY C.BMI DESC LIMIT 1",
    "reasoning_type": "/ * C",
    "commonsense_knowledge": "Body mass index is weight in pounds divided by height in meters squared and multiplying by a conversion factor 0.45."
  },
  {
    "input": "在进攻和防守工作率都“低”的球员中，有多少球员是右脚球员，有多少是左脚球员，相差多少？",
    "query": "SELECT left_count , right_count , ABS ( left_count - right_count ) FROM ( SELECT COUNT ( DISTINCT ( B.player_name ) ) AS left_count FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.attacking_work_rate = \"low\" and A.defensive_work_rate = \"low\" and A.preferred_foot = \"left\" ) JOIN ( SELECT COUNT ( DISTINCT ( B.player_name ) ) AS right_count FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.attacking_work_rate = \"low\" and A.defensive_work_rate = \"low\" and A.preferred_foot = \"right\" )",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "提供一份球员名单、他们的总体评分、以及他们的属性记录日期，且这些球员的传中评分超过了2007年8月30日记录的法比奥·卡纳瓦罗的传中评分的两倍。",
    "query": "SELECT B.player_name , A.overall_rating , A.date FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id , ( SELECT A.crossing AS FC_crossing FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE B.player_name = \"Fabio Cannavaro\" and date ( A.date ) = \"2007-08-30\" ) WHERE A.crossing > 2.0 * FC_crossing",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如2007年8月30日法比奥·卡纳瓦罗获得的传中评分是45，提供一份球员名单、他们的总体评分、以及他们的属性记录日期，且这些球员的传中评分超过了2007年8月30日记录的法比奥·卡纳瓦罗的传中评分的两倍。",
    "query": "SELECT B.player_name , A.overall_rating , A.date FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.crossing > 2.0 * 45",
    "reasoning_type": "* H",
    "commonsense_knowledge": ""
  },
  {
    "input": "乔纳森·莱科的体重指数是多少？",
    "query": "SELECT weight * 0.45 / ( ( 1.0 * height / 100 ) * ( height / 100 ) ) AS BMI FROM Player WHERE player_name = \"Jonathan Leko\"",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Body mass index is weight in pounds divided by height in meters squared and multiplying by a conversion factor 0.45."
  },
  {
    "input": "乔纳森·莱科的体重指数是多少，假如他高190cm？",
    "query": "SELECT weight * 0.45 / ( ( 190.0 / 100 ) * ( 190.0 / 100 ) ) AS BMI FROM Player WHERE player_name = \"Jonathan Leko\"",
    "reasoning_type": "* / C H",
    "commonsense_knowledge": "Body mass index is weight in pounds divided by height in meters squared and multiplying by a conversion factor 0.45."
  },
  {
    "input": "防守评分由40%的盯人、30%的站位拦截和30%的铲球组成。列出防守评分最高的前3名球员的姓名及其体重指数（BMI）。",
    "query": "SELECT B.player_name, B.weight * 0.45 / ((1.0 * B.height / 100) * (1.0 * B.height / 100)) AS BMI FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.marking IS NOT NULL AND A.interceptions IS NOT NULL AND A.standing_tackle IS NOT NULL GROUP BY B.player_name ORDER BY MAX(0.4 * A.marking + 0.3 * A.interceptions + 0.3 * A.standing_tackle) DESC LIMIT 3",
    "reasoning_type": "+ * / C",
    "commonsense_knowledge": "Body mass index is weight in pounds divided by height in meters squared and multiplying by a conversion factor 0.45."
  }
]