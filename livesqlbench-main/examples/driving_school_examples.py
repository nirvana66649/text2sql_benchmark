driving_school_examples = [
  {
    "input": "列出每个客户的ID和报名驾校时的年龄。",
    "query": "SELECT customer_id, strftime('%Y', date_became_customer) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_became_customer) < strftime('%m-%d', date_of_birth)) AS age FROM Customers",
    "reasoning_type": "- C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如达蒙·桑福德出生于21世纪的第一天，列出每个客户的ID和报名驾校时的年龄。",
    "query": "SELECT customer_id, strftime('%Y', date_became_customer) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_became_customer) < strftime('%m-%d', date_of_birth)) AS age FROM Customers WHERE NOT (first_name = 'Dameon' AND last_name = 'Sanford') UNION ALL SELECT customer_id, strftime('%Y', date_became_customer) - strftime('%Y', '2001-01-01') - (strftime('%m-%d', date_became_customer) < strftime('%m-%d', '2001-01-01')) AS age FROM Customers WHERE first_name = 'Dameon' AND last_name = 'Sanford'",
    "reasoning_type": "- C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date. The 21st century began on 1st January 2001."
  },
  {
    "input": "未偿金额大于2000的客户中有百分之多少客户是优质客户？",
    "query": "SELECT 100.0 * good / n AS percent FROM (SELECT COUNT(*) AS good FROM Customers WHERE amount_outstanding > 2000 AND customer_status_code = 'Good Customer') JOIN (SELECT COUNT(*) AS n FROM Customers WHERE amount_outstanding > 2000)",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如2015年报名的客户未偿金额为200，未偿金额大于2000的客户中有百分之多少客户是优质客户？",
    "query": "SELECT 100.0 * good / n AS percent FROM (SELECT COUNT(*) AS good FROM (SELECT 200 AS amount_outstanding, customer_status_code FROM Customers WHERE strftime('%Y', date_became_customer) = '2015' UNION ALL SELECT amount_outstanding, customer_status_code FROM Customers WHERE strftime('%Y', date_became_customer) != '2015') WHERE amount_outstanding > 2000 AND customer_status_code = 'Good Customer') JOIN (SELECT COUNT(*) AS n FROM (SELECT 200 AS amount_outstanding, customer_status_code FROM Customers WHERE strftime('%Y', date_became_customer) = '2015' UNION ALL SELECT amount_outstanding, customer_status_code FROM Customers WHERE strftime('%Y', date_became_customer) != '2015') WHERE amount_outstanding > 2000)",
    "reasoning_type": "* / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "列出入职时大于20岁的教练的ID和安排的课程数量。",
    "query": "SELECT A.staff_id, COUNT(*) AS n_lesson FROM Staff A JOIN Lessons B ON A.staff_id = B.staff_id WHERE strftime('%Y', A.date_joined_staff) - strftime('%Y', A.date_of_birth) - (strftime('%m-%d', A.date_joined_staff) < strftime('%m-%d', A.date_of_birth)) > 20 UNION ALL SELECT staff_id, 0 AS n_lesson FROM Staff WHERE strftime('%Y', date_joined_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_joined_staff) < strftime('%m-%d', date_of_birth)) > 20 AND staff_id NOT IN (SELECT A.staff_id FROM Staff A JOIN Lessons B ON A.staff_id = B.staff_id)",
    "reasoning_type": "- C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如2018年3月8日离职的教练都是2016年3月8日入职的，列出入职时大于20岁的教练的ID、安排的课程数量。",
    "query": "SELECT A.staff_id, COUNT(*) AS n_lesson FROM (SELECT staff_id, date_of_birth, '2016-03-08' AS date_joined_staff FROM Staff WHERE strftime('%Y-%m-%d', date_left_staff) = '2018-03-08' UNION ALL SELECT staff_id, date_of_birth, date_joined_staff FROM Staff WHERE strftime('%Y-%m-%d', date_left_staff) != '2018-03-08') A JOIN Lessons B ON A.staff_id = B.staff_id WHERE strftime('%Y', A.date_joined_staff) - strftime('%Y', A.date_of_birth) - (strftime('%m-%d', A.date_joined_staff) < strftime('%m-%d', A.date_of_birth)) > 20 UNION ALL SELECT staff_id, 0 AS n_lesson FROM (SELECT staff_id, date_of_birth, '2016-03-08' AS date_joined_staff FROM Staff WHERE strftime('%Y-%m-%d', date_left_staff) = '2018-03-08' UNION ALL SELECT staff_id, date_of_birth, date_joined_staff FROM Staff WHERE strftime('%Y-%m-%d', date_left_staff) != '2018-03-08') WHERE strftime('%Y', date_joined_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_joined_staff) < strftime('%m-%d', date_of_birth)) > 20 AND staff_id NOT IN (SELECT A.staff_id FROM Staff A JOIN Lessons B ON A.staff_id = B.staff_id)",
    "reasoning_type": "- C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "哪个教练在驾校工作得最久？给出他们的ID。",
    "query": "SELECT staff_id FROM Staff ORDER BY julianday(date_left_staff) - julianday(date_joined_staff) DESC LIMIT 1",
    "reasoning_type": "- C",
    "commonsense_knowledge": "The time duration is calculated by subtracting the start time from the end time."
  },
  {
    "input": "假如林肯·本尼·卡罗尔21岁生日那天入职的，给出在驾校工作得最久的教练的ID。",
    "query": "SELECT staff_id FROM (SELECT staff_id, strftime('%Y-%m-%d', julianday(date_of_birth) + 21 * 365.25) AS date_joined_staff, date_left_staff FROM Staff WHERE first_name = 'Lincoln' AND middle_name = 'Benny' AND last_name = 'Carroll' UNION ALL SELECT staff_id, date_joined_staff, date_left_staff FROM Staff WHERE NOT (first_name = 'Lincoln' AND middle_name = 'Benny' AND last_name = 'Carroll')) ORDER BY julianday(date_left_staff) - julianday(date_joined_staff) DESC LIMIT 1",
    "reasoning_type": "- + * C H",
    "commonsense_knowledge": "The time duration is calculated by subtracting the start time from the end time. Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "一次课都没上过的客户中不良客户比优质客户多多少？",
    "query": "SELECT n_bad - n_good AS diff FROM (SELECT COUNT(*) AS n_good FROM Customers WHERE customer_id NOT IN (SELECT DISTINCT(customer_id) FROM Lessons WHERE lesson_status_code != 'Cancelled') AND customer_status_code = 'Good Customer') JOIN (SELECT COUNT(*) AS n_bad FROM Customers WHERE customer_id NOT IN (SELECT DISTINCT(customer_id) FROM Lessons WHERE lesson_status_code != 'Cancelled') AND customer_status_code = 'Bad Customer')",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如2018年3月7日所有课都没有被取消，一次课都没上过的客户中不良客户比优质客户多多少？",
    "query": "SELECT n_bad - n_good AS diff FROM (SELECT COUNT(*) AS n_good FROM Customers WHERE customer_id NOT IN (SELECT DISTINCT(customer_id) FROM (SELECT customer_id, 'Completed' AS lesson_status_code FROM Lessons WHERE strftime('%Y-%m-%d', lesson_date) = '2018-03-07' UNION ALL SELECT customer_id, lesson_status_code FROM Lessons WHERE strftime('%Y-%m-%d', lesson_date) != '2018-03-07') WHERE lesson_status_code != 'Cancelled') AND customer_status_code = 'Good Customer') JOIN (SELECT COUNT(*) AS n_bad FROM Customers WHERE customer_id NOT IN (SELECT DISTINCT(customer_id) FROM (SELECT customer_id, 'Completed' AS lesson_status_code FROM Lessons WHERE strftime('%Y-%m-%d', lesson_date) = '2018-03-07' UNION ALL SELECT customer_id, lesson_status_code FROM Lessons WHERE strftime('%Y-%m-%d', lesson_date) != '2018-03-07') WHERE lesson_status_code != 'Cancelled') AND customer_status_code = 'Bad Customer')",
    "reasoning_type": "- H",
    "commonsense_knowledge": ""
  },
  {
    "input": "2018年3月5日后没有课程安排的教练的ID是多少，其一次课平均多少钱，他今年多少岁了？",
    "query": "SELECT A.staff_id, AVG(A.price) AS avg_price, strftime('%Y', 'now') - strftime('%Y', B.date_of_birth) - (strftime('%m-%d', 'now') < strftime('%m-%d', B.date_of_birth)) AS age FROM Lessons A JOIN Staff B ON A.staff_id = B.staff_id WHERE A.staff_id NOT IN (SELECT staff_id FROM Lessons WHERE strftime('%Y-%m-%d', lesson_date) > '2018-03-05') GROUP BY A.staff_id",
    "reasoning_type": "- C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如2018年2月所有课涨价8%，2018年3月5日后没有课程安排的教练的ID是多少，其一次课平均多少钱，这些教练今年多少岁？",
    "query": "SELECT A.staff_id, AVG(A.price) AS avg_price, strftime('%Y', 'now') - strftime('%Y', B.date_of_birth) - (strftime('%m-%d', 'now') < strftime('%m-%d', B.date_of_birth)) AS age FROM (SELECT staff_id, (1 + 0.08) * price AS price FROM Lessons WHERE strftime('%Y-%m', lesson_date) = '2018-02' UNION ALL SELECT staff_id, price FROM Lessons WHERE strftime('%Y-%m', lesson_date) != '2018-02') A JOIN Staff B ON A.staff_id = B.staff_id WHERE A.staff_id NOT IN (SELECT staff_id FROM Lessons WHERE strftime('%Y-%m-%d', lesson_date) > '2018-03-05') GROUP BY A.staff_id",
    "reasoning_type": "* + - C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "哪个教练课程均价最高，给出他的ID。其均价比课程均价最低的教练高多少？",
    "query": "SELECT A.staff_id, AVG(A.price) - (SELECT AVG(price) FROM Lessons GROUP BY staff_id ORDER BY AVG(price) ASC LIMIT 1) AS diff FROM Lessons A JOIN Staff B ON A.staff_id = B.staff_id GROUP BY A.staff_id ORDER BY AVG(A.price) DESC LIMIT 1",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如温尼弗雷德·利亚姆·贾斯特的所有课程降价12%，哪个教练课程均价最高，给出他的ID，其均价比课程均价最低的教练高多少？",
    "query": "SELECT staff_id, AVG(price) - (SELECT AVG(price) FROM (SELECT A.staff_id, B.first_name, B.middle_name, B.last_name, A.price * (1 - 0.12) AS price FROM Lessons A JOIN Staff B ON A.staff_id = B.staff_id WHERE B.first_name = 'Winnifred' AND B.middle_name = 'Liam' AND B.last_name = 'Jast' UNION ALL SELECT A.staff_id, B.first_name, B.middle_name, B.last_name, A.price FROM Lessons A JOIN Staff B ON A.staff_id = B.staff_id WHERE NOT (B.first_name = 'Winnifred' AND B.middle_name = 'Liam' AND B.last_name = 'Jast')) GROUP BY staff_id ORDER BY AVG(price) ASC LIMIT 1) AS diff FROM (SELECT A.staff_id, B.first_name, B.middle_name, B.last_name, A.price * (1 - 0.12) AS price FROM Lessons A JOIN Staff B ON A.staff_id = B.staff_id WHERE B.first_name = 'Winnifred' AND B.middle_name = 'Liam' AND B.last_name = 'Jast' UNION ALL SELECT A.staff_id, B.first_name, B.middle_name, B.last_name, A.price FROM Lessons A JOIN Staff B ON A.staff_id = B.staff_id WHERE NOT (B.first_name = 'Winnifred' AND B.middle_name = 'Liam' AND B.last_name = 'Jast')) GROUP BY staff_id ORDER BY AVG(price) DESC LIMIT 1",
    "reasoning_type": "- * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "有百分之多少的学员有多个教练？",
    "query": "SELECT 100.0 * COUNT(*) / (SELECT COUNT(*) FROM Customers) AS percent FROM (SELECT customer_id FROM Lessons GROUP BY customer_id HAVING COUNT(DISTINCT(staff_id)) >= 2)",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如ID为12的课程的教练是尼弗雷德·利亚姆·贾斯特，有百分之多少的学员有多个教练？",
    "query": "SELECT 100.0 * COUNT(*) / (SELECT COUNT(*) FROM Customers) AS percent FROM (SELECT customer_id FROM (SELECT customer_id, (SELECT staff_id FROM Staff WHERE first_name = 'Winnifred' AND middle_name = 'Liam' AND last_name = 'Jast') AS staff_id FROM Lessons WHERE lesson_id = '12' UNION ALL SELECT customer_id, staff_id FROM Lessons WHERE lesson_id != '12') GROUP BY customer_id HAVING COUNT(DISTINCT(staff_id)) >= 2)",
    "reasoning_type": "* / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "最老的教练比最年轻的教练大多少岁？",
    "query": "SELECT strftime('%Y', MAX(date_of_birth)) - strftime('%Y', MIN(date_of_birth)) - (strftime('%m-%d', MAX(date_of_birth)) < strftime('%m-%d', MIN(date_of_birth))) AS diff FROM Staff",
    "reasoning_type": "- C",
    "commonsense_knowledge": "The time duration is calculated by subtracting the start time from the end time."
  },
  {
    "input": "假如2020年的时候卡梅尔·伊西·魏斯纳特的年龄是2009年出生的人的两倍，最老的教练比最年轻的教练大多少岁？",
    "query": "SELECT MAX(date_of_birth) - MIN(date_of_birth) AS diff FROM (SELECT 2020 - (2020 - 2009) * 2 AS date_of_birth FROM Staff WHERE first_name = 'Camylle' AND middle_name = 'Icie' AND last_name = 'Weissnat' UNION ALL SELECT date_of_birth FROM Staff WHERE NOT (first_name = 'Camylle' AND middle_name = 'Icie' AND last_name = 'Weissnat')) ORDER BY date_of_birth DESC",
    "reasoning_type": "* - C H",
    "commonsense_knowledge": "The time duration is calculated by subtracting the start time from the end time."
  },
  {
    "input": "离开驾校时的年龄最大的教练总共有多少课程安排，其中被取消了的课占比多少？",
    "query": "SELECT total, 1.0 * n_cancel / total AS ratio FROM (SELECT COUNT(*) AS total FROM Lessons WHERE staff_id = (SELECT staff_id FROM Staff ORDER BY strftime('%Y', date_left_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_left_staff) < strftime('%m-%d', date_of_birth)) DESC LIMIT 1)) JOIN (SELECT COUNT(*) AS n_cancel FROM Lessons WHERE staff_id = (SELECT staff_id FROM Staff ORDER BY strftime('%Y', date_left_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_left_staff) < strftime('%m-%d', date_of_birth)) DESC LIMIT 1) AND lesson_status_code = 'Cancelled')",
    "reasoning_type": "- * /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如所有教练入职后的60天内都没有课程安排，离开驾校的时年龄最大的教练总共有多少课程安排，其中被取消了的课占比多少？",
    "query": "SELECT total, 1.0 * n_cancel / total AS ratio FROM (SELECT COUNT(*) AS total FROM Lessons A JOIN Staff B ON A.staff_id = B.staff_id WHERE A.staff_id = (SELECT staff_id FROM Staff ORDER BY strftime('%Y', date_left_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_left_staff) < strftime('%m-%d', date_of_birth)) DESC LIMIT 1) AND A.lesson_date > strftime('%Y-%m-%d', julianday(B.date_joined_staff) + 60)) JOIN (SELECT COUNT(*) AS n_cancel FROM Lessons A JOIN Staff B ON A.staff_id = B.staff_id WHERE A.staff_id = (SELECT staff_id FROM Staff ORDER BY strftime('%Y', date_left_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_left_staff) < strftime('%m-%d', date_of_birth)) DESC LIMIT 1) AND A.lesson_status_code = 'Cancelled' AND A.lesson_date > strftime('%Y-%m-%d', julianday(B.date_joined_staff) + 60))",
    "reasoning_type": "+ - * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "哪个客户支付的钱最多，给出他的ID，并求出其比支付的钱最少的客户多支付多少钱。",
    "query": "SELECT A.customer_id, MAX(A.amount_payment) - (SELECT MIN(amount_payment) FROM Customer_Payments) AS payment_diff FROM Customer_Payments A JOIN Customers B ON A.customer_id = B.customer_id",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如阿米娅·斯宾卡2018年3月12日多支付5000，哪个客户支付的钱最多，给出他的ID，并求出其比支付的钱最少的客户多支付多少钱。",
    "query": "SELECT customer_id, MAX(amount_payment) - (SELECT MIN(amount_payment) FROM (SELECT A.customer_id, amount_payment + 5000 AS amount_payment FROM Customer_Payments A JOIN Customers B ON A.customer_id = B.customer_id WHERE B.first_name = 'Amya' AND B.last_name = 'Spinka' AND strftime('%Y-%m-%d', A.datetime_payment) = '2018-03-12' UNION ALL SELECT A.customer_id, amount_payment AS amount_payment FROM Customer_Payments A JOIN Customers B ON A.customer_id = B.customer_id WHERE NOT (B.first_name = 'Amya' AND B.last_name = 'Spinka' AND strftime('%Y-%m-%d', A.datetime_payment) = '2018-03-12'))) AS payment_diff FROM (SELECT A.customer_id, amount_payment + 5000 AS amount_payment FROM Customer_Payments A JOIN Customers B ON A.customer_id = B.customer_id WHERE B.first_name = 'Amya' AND B.last_name = 'Spinka' AND strftime('%Y-%m-%d', A.datetime_payment) = '2018-03-12' UNION ALL SELECT A.customer_id, amount_payment AS amount_payment FROM Customer_Payments A JOIN Customers B ON A.customer_id = B.customer_id WHERE NOT (B.first_name = 'Amya' AND B.last_name = 'Spinka' AND strftime('%Y-%m-%d', A.datetime_payment) = '2018-03-12'))",
    "reasoning_type": "- + H",
    "commonsense_knowledge": ""
  },
  {
    "input": "住在乔治亚州伊莱恩湖市的教练平均年龄是多少？",
    "query": "SELECT AVG(strftime('%Y', 'now') - strftime('%Y', A.date_of_birth) - (strftime('%m-%d', 'now') < strftime('%m-%d', A.date_of_birth))) AS avg_age FROM Staff A JOIN Addresses B ON A.staff_address_id = B.address_id WHERE B.state_province_county = 'Georgia' AND B.city = 'Lake Elaina'",
    "reasoning_type": "- C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如住在乔治亚州伊莱恩湖市的教练平均年龄是住在乔治亚州梅丽莎港市的教练的平均年龄的两倍，住在乔治亚州伊莱恩湖市的教练平均年龄是多少？",
    "query": "SELECT 2 * AVG(strftime('%Y', 'now') - strftime('%Y', A.date_of_birth) - (strftime('%m-%d', 'now') < strftime('%m-%d', A.date_of_birth))) AS avg_age FROM Staff A JOIN Addresses B ON A.staff_address_id = B.address_id WHERE B.state_province_county = 'Georgia' AND B.city = 'Port Melyssa'",
    "reasoning_type": "- * C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "贾妮莎·阿马拉·萨文离职5年后多少岁，比卡梅尔·伊西·魏斯纳特小多少岁？",
    "query": "SELECT * FROM (SELECT 5 + strftime('%Y', date_left_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_left_staff) < strftime('%m-%d', date_of_birth)) AS age FROM Staff WHERE first_name = 'Janessa' AND middle_name = 'Amara' AND last_name = 'Sawayn') JOIN (SELECT date_of_birth - (SELECT date_of_birth FROM Staff WHERE first_name = 'Janessa' AND middle_name = 'Amara' AND last_name = 'Sawayn') AS diff FROM Staff WHERE first_name = 'Camylle' AND middle_name = 'Icie' AND last_name = 'Weissnat')",
    "reasoning_type": "- + C",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  },
  {
    "input": "假如贾妮莎·阿马拉·萨文离职的时候卡梅尔·伊西·魏斯纳特30岁，贾妮莎·阿马拉·萨文离职5年后多少岁，比卡梅尔·伊西·魏斯纳特小多少岁？",
    "query": "SELECT 5 + strftime('%Y', date_left_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_left_staff) < strftime('%m-%d', date_of_birth)) AS age, 30 - (strftime('%Y', date_left_staff) - strftime('%Y', date_of_birth) - (strftime('%m-%d', date_left_staff) < strftime('%m-%d', date_of_birth))) AS diff FROM Staff WHERE first_name = 'Janessa' AND middle_name = 'Amara' AND last_name = 'Sawayn'",
    "reasoning_type": "- + C H",
    "commonsense_knowledge": "Age is calculated by subtracting date of birth from a given date."
  }
]