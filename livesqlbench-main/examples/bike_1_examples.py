bike_1_examples = [
    {
        "input": "2015年6月2日12:47:02，圣何塞文娱中心站不可用的自行车停靠点有多少？",
        "query": "SELECT A.dock_count - B.docks_available AS n_unavailable FROM station A JOIN status B ON A.id = B.station_id WHERE B.time = '2015-06-02 12:47:02' AND A.name = 'San Jose Civic Center'",
        "reasoning_type": "- C",
        "commonsense_knowledge": "unavailable dock count= total dock count - available dock count"
    },
    {
        "input": "如果圣何塞文娱中心站站总共有20个自行车停靠点，那么2015年6月2日12:47:02，它不可用的自行车停靠点有多少？",
        "query": "SELECT 20 - B.docks_available AS n_unavailable FROM station A JOIN status B ON A.id = B.station_id WHERE B.time = '2015-06-02 12:47:02' AND A.name = 'San Jose Civic Center'",
        "reasoning_type": "- C H",
        "commonsense_knowledge": "unavailable dock count= total dock count - available dock count"
    },
    {
        "input": "金门之城总共有多少个自行车站，比帕洛阿托少多少？",
        "query": "SELECT ( SELECT COUNT ( * ) FROM station WHERE city = 'Palo Alto' ) - COUNT ( * ) AS diff FROM station WHERE city = 'San Francisco'",
        "reasoning_type": "- C",
        "commonsense_knowledge": "San Francisco is known as city of the Golden Gate."
    },
    {
        "input": "金门之城总共有多少个自行车站？如果帕洛阿托的自行车站数量是它自己的两倍还多10个，那金门之城的自行车站数量比帕洛阿托少多少？",
        "query": "SELECT ( SELECT COUNT ( * ) * 2 + 10 FROM station WHERE city = 'Palo Alto' ) - COUNT ( * ) AS diff FROM station WHERE city = 'San Francisco'",
        "reasoning_type": "- + * C H",
        "commonsense_knowledge": "San Francisco is known as city of the Golden Gate."
    },
    {
        "input": "在2015年6月2日12:46:02这个时刻，那些建于2013年8月20日的车站的可用自行车停靠点一共有多少，不可用的自行车停靠点呢？",
        "query": "SELECT SUM ( B.docks_available ) AS total_available , SUM ( A.dock_count ) - SUM ( B.docks_available ) AS total_unavailable FROM station A JOIN status B ON A.id = B.station_id WHERE A.installation_date = '8/20/2013' AND B.time = '2015-06-02 12:46:02'",
        "reasoning_type": "- C",
        "commonsense_knowledge": "unavailable dock count= total dock count - available dock count"
    },
    {
        "input": "如果建于2013年8月20日的每个车站的自行车停靠点数量都是\"Grant Avenue at Columbus Avenue\"车站自行车停靠点数量的两倍多5个，在2015年6月2日12:46:02这个时刻，那些建于2013年8月20日的车站的可用的自行车停靠点一共有多少可用，不可用的自行车停靠点呢？",
        "query": "SELECT SUM ( B.docks_available ) AS total_available , SUM ( 2 * ( SELECT dock_count FROM station WHERE name = 'Grant Avenue at Columbus Avenue' ) + 5 - B.docks_available ) AS total_unavailable FROM station A JOIN status B ON A.id = B.station_id WHERE A.installation_date = '8/20/2013' AND B.time = '2015-06-02 12:46:02'",
        "reasoning_type": '+ * - C H',
        "commonsense_knowledge": 'unavailable dock count= total dock count - available dock count'
    },
    {
        "input": "查找持续时间是出发于“2nd at Folsom”站的行程的平均持续时间至少两倍的行程ID。",
        "query": "SELECT id FROM trip WHERE duration >= ( SELECT 2 * AVG ( duration ) FROM trip WHERE start_station_name = '2nd at Folsom' )",
        "reasoning_type": "*",
        "commonsense_knowledge": ""
    },
    {
        "input": "查找持续时间至少是出发于“2nd at Folsom”站的行程的平均持续时间两倍的行程ID，假如出发于“2nd at Folsom”站的行程的平均持续时间是666。",
        "query": "SELECT id FROM trip WHERE duration >= 2 * 666",
        "reasoning_type": "* H",
        "commonsense_knowledge": ""
    },
    {
        "input": "2015年6月2日13:59:02，哪个车站的可用自行车数量是“2nd at Townsend”的两倍多？给出这些车站的名字。",
        "query": "SELECT B.name FROM status A JOIN station B ON A.station_id = B.id WHERE A.bikes_available > 2 * ( SELECT A.bikes_available FROM status A JOIN station B ON A.station_id = B.id WHERE B.name = '2nd at Townsend' AND A.time = '2015-06-02 13:59:02' ) AND A.time = '2015-06-02 13:59:02'",
        "reasoning_type": "*",
        "commonsense_knowledge": ""
    },
    {
        "input": "2015年6月2日13:59:02，如果“2nd at Townsend”有5个可用的自行车，哪个车站的可用自行车是“2nd at Townsend”的两倍多？给出这些车站的名字。",
        "query": "SELECT B.name FROM status A JOIN station B ON A.station_id = B.id WHERE A.bikes_available > 2 * 5 AND A.time = '2015-06-02 13:59:02'",
        "reasoning_type": "* H",
        "commonsense_knowledge": ""
    },
    {
        "input": "对于每个车站，找出以它为终点站的行程的最小持续时间、最长持续时间以及它们的差值。",
        "query": "SELECT end_station_name , MAX ( duration ) AS max_duration , MIN ( duration ) AS min_duration , MAX ( duration ) - MIN ( duration ) AS diff FROM trip GROUP BY end_station_name",
        "reasoning_type": "-",
        "commonsense_knowledge": ""
    },
    {
        "input": "邮编为94107的地方哪天温差最大？",
        "query": "SELECT date FROM weather WHERE zip_code = '94107' AND max_temperature_f - min_temperature_f = ( SELECT MAX ( max_temperature_f - min_temperature_f ) FROM weather WHERE zip_code = '94107' )",
        "reasoning_type": "-",
        "commonsense_knowledge": ""
    },
    {
        "input": "2013年一战停战纪念日，哪个地方的平均能见度英里数最高，给出那里的邮编，以及那里那天的温差。",
        "query": "SELECT zip_code , tem_diff FROM ( SELECT zip_code , MAX ( mean_visibility_miles ) , max_temperature_f - min_temperature_f AS tem_diff FROM weather WHERE date = '11/11/2013' )",
        "reasoning_type": "- C",
        "commonsense_knowledge": "Armistice Day is commemorated on 11th November every year."
    },
    {
        "input": "2013年一战停战纪念日，哪个地方的平均能见度英里数最高？给出那里的邮编。如果那里最低温度是52华氏度，那天的温差是多少？",
        "query": "SELECT zip_code , tem_diff FROM ( SELECT zip_code , MAX ( mean_visibility_miles ) , max_temperature_f - 52 AS tem_diff FROM weather WHERE date = '11/11/2013' )",
        "reasoning_type": "- C",
        "commonsense_knowledge": "Armistice Day is commemorated on 11th November every year."
    },
    {
        "input": "邮编为94107的地方哪天平均温度最高？列出日期和平均摄氏温度。",
        "query": "SELECT date , 1.0 * ( MAX ( mean_temperature_f ) - 32 ) * 5 / 9 AS celsius FROM weather WHERE zip_code = '94107'",
        "reasoning_type": "/ * - C",
        "commonsense_knowledge": "To convert Fahrenheit to celsius, the formula used is °C = 5/9(°F – 32)."
    },
    {
        "input": "各个地方的邮编是多少？它们2014年1月1日平均风速分别是多少千米每小时？",
        "query": "SELECT zip_code , mean_wind_speed_mph * 1.609344 AS km_per_h FROM weather WHERE date = '1/1/2014'",
        "reasoning_type": "* C",
        "commonsense_knowledge": "1 miles per hour (mph) is equal to 1.609344 kilometres per hour (km/h)."
    },
    {
        "input": "2014年1月1日这天各个地方的平均风速是多少千米每小时，如果当天的平均风速增加了20%？同时给出对应的邮编。",
        "query": "SELECT zip_code , mean_wind_speed_mph * ( 1 + 0.2 ) * 1.609344 AS km_per_h FROM weather WHERE date = '1/1/2014'",
        "reasoning_type": "+ * C",
        "commonsense_knowledge": "1 miles per hour (mph) is equal to 1.609344 kilometres per hour (km/h)."
    },
    {
        "input": "邮编地址为94041的地方2014年11月12日和2014年3月12日这两天的降水量分别是多少毫米，相差多少？",
        "query": "SELECT mm_1 , mm_2 , ABS ( mm_1 - mm_2 ) AS diff FROM ( SELECT precipitation_inches * 25 AS mm_1 FROM weather WHERE zip_code = '94041' AND date = '12/11/2014' ) JOIN ( SELECT precipitation_inches * 25 AS mm_2 FROM weather WHERE zip_code = '94041' AND date = '12/3/2014' )",
        "reasoning_type": "* - C",
        "commonsense_knowledge": "25 mm equals one inch."
    },
    {
        "input": "如果邮编地址为94041的地方2014年11月12日和2014年3月12日那两天的降水量减少了15%，那两天的降水量分别是多少毫米，相差多少？",
        "query": "SELECT mm_1 , mm_2 , ABS ( mm_1 - mm_2 ) AS diff FROM ( SELECT precipitation_inches * ( 1 - 0.15 ) * 25 AS mm_1 FROM weather WHERE zip_code = '94041' AND date = '12/11/2014' ) JOIN ( SELECT precipitation_inches * ( 1 - 0.15 ) * 25 AS mm_2 FROM weather WHERE zip_code = '94041' AND date = '12/3/2014' )",
        "reasoning_type": "- * C H",
        "commonsense_knowledge": "25 mm equals one inch."
    },
    {
        "input": "2013年国民悲痛意识日这天，各个地方的最高能见度、平均能见度、最低能见度是多少米？同时给出对应的邮编。",
        "query": "SELECT zip_code , max_visibility_miles * 1609.344 AS max_m , mean_visibility_miles * 1609.344 AS mean_m , min_visibility_miles * 1609.344 AS min_m FROM weather WHERE date = '8/30/2013'",
        "reasoning_type": "* C",
        "commonsense_knowledge": "1 mile is equal to 1,609.344 meters. National Grief Awareness Day takes place on August 30th every year"
    },
    {
        "input": "如果给自行车停靠点最少的车站再添10个自行车停靠点，它会有多少自行车停靠点？",
        "query": "SELECT MIN ( dock_count ) + 10 AS n_dock FROM station",
        "reasoning_type": "+",
        "commonsense_knowledge": ""
    },
    {
        "input": "政府计划在加利福尼亚州的人口排名第三的城市中再建立四个车站，那里将总共有几个车站？",
        "query": "SELECT COUNT ( * ) + 4 AS n_stations FROM station WHERE city = 'San Jose'",
        "reasoning_type": "+ C",
        "commonsense_knowledge": "San Jose is the third largest city by population in California."
    },
    {
        "input": "给出各地区的邮政编码，并计算2014年10月24日，各地区的最高温度是多少？与地球上有记录以来的最高气温相差多少？",
        "query": "SELECT zip_code , max_temperature_f , ABS ( max_temperature_f - 136 ) AS diff FROM weather WHERE date = '10/24/2014'",
        "reasoning_type": "- C",
        "commonsense_knowledge": "57.8 °C (136 °F) is the hottest temperature ever recorded on Earth."
    },
    {
        "input": "旧金山有百分之多少的车站有超过25个自行车停靠点？",
        "query": "SELECT 100.0 * COUNT ( * ) / ( SELECT COUNT ( * ) FROM station WHERE city = 'San Francisco' ) AS propotion FROM station WHERE city = 'San Francisco' AND dock_count > 25",
        "reasoning_type": "/ *",
        "commonsense_knowledge": ""
    },
    {
        "input": "拥有最多车站的城市的车站数量是拥有最少车站的车站数量的多少倍？",
        "query": "SELECT 1.0 * MAX ( n_station ) / MIN ( n_station ) AS times FROM ( SELECT city , COUNT ( * ) AS n_station FROM station GROUP BY city )",
        "reasoning_type": "/ *",
        "commonsense_knowledge": ""
    },
    {
        "input": "温差最大的时候最高温度是最低温度的多少倍？",
        "query": "SELECT 1.0 * max_temperature_f / min_temperature_f AS times FROM weather WHERE max_temperature_f - min_temperature_f = ( SELECT MAX ( max_temperature_f - min_temperature_f ) FROM weather )",
        "reasoning_type": "- * /",
        "commonsense_knowledge": ""
    },
    {
        "input": "邮编为94063的地方平均最高气温是多少摄氏度，比平均最低气温高多少？",
        "query": "SELECT ( AVG ( max_temperature_f ) - 32 ) * 5 / 9 AS avg_max_celsius , ( ( AVG ( max_temperature_f ) - AVG ( min_temperature_f ) ) ) * 5 / 9 AS diff_celsius FROM weather WHERE zip_code = '94063'",
        "reasoning_type": "/ * - C",
        "commonsense_knowledge": "To convert Fahrenheit to celsius, the formula used is °C = 5/9(°F – 32)."
    }
]
