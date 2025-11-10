hospital_1_examples=[
  {
    "input": "约翰·史密斯住了几天院？",
    "query": "SELECT CAST ( julianday ( A.StayEnd ) - julianday ( A.StayStart ) AS INTEGER ) AS days_diff FROM Stay A JOIN Patient B ON A.Patient = B.SSN WHERE B.name = \"John Smith\"",
    "reasoning_type": "- C",
    "commonsense_knowledge": "Days in hospital is caculated by subtracting day of admission from day of discharge."
  },
  {
    "input": "如果约翰·史密斯是国际护士节那天出院的，他住了几天院？",
    "query": "SELECT julianday ( strftime ( \"%Y-\" , A.StayEnd ) || \"05-12\" ) - julianday ( strftime ( \"%Y-\" , A.StayStart ) || strftime ( \"%m-%d\" , A.StayStart ) ) AS date_diff FROM Stay A JOIN Patient B ON A.Patient = B.SSN WHERE B.name = \"John Smith\"",
    "reasoning_type": "- C H",
    "commonsense_knowledge": "Days in hospital is caculated by subtracting day of admission from day of dischargel. International Nurses Day is an international day observed around the world on 12 May each year."
  },
  {
    "input": "使用了Foo Labs品牌的药的病人比使用了Baz Industries品牌的药的病人多多少？",
    "query": "SELECT COUNT ( DISTINCT ( Patient ) ) - ( SELECT COUNT ( DISTINCT ( Patient ) ) FROM Medication A JOIN Prescribes B ON A.code = B.Medication WHERE A.Brand = \"Baz Industries\" ) AS diff FROM Medication A JOIN Prescribes B ON A.code = B.Medication WHERE A.Brand = \"Foo Labs\"",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "如果使用过Foo Labs品牌的病人共有10个，使用了Foo Labs品牌的药的病人比使用了Baz Industries品牌的药的病人多多少？",
    "query": "SELECT 10 - ( SELECT COUNT ( DISTINCT ( Patient ) ) FROM Medication A JOIN Prescribes B ON A.code = B.Medication WHERE A.Brand = \"Baz Industries\" ) AS diff",
    "reasoning_type": "- H",
    "commonsense_knowledge": ""
  },
  {
    "input": "预约次数最多的医生的预约次数是预约次数最少的医生的多少倍？",
    "query": "SELECT 1.0 * MAX ( c ) / MIN ( c ) AS times FROM ( SELECT Physician , COUNT ( * ) AS c FROM Appointment GROUP BY Physician )",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "如果预约最少的医师新添了2个预约，预约次数最多的医生的预约次数是他的多少倍？",
    "query": "SELECT 1.0 * MAX ( c ) / ( MIN ( c ) + 2 ) AS times FROM ( SELECT Physician , COUNT ( * ) AS c FROM Appointment GROUP BY Physician )",
    "reasoning_type": "+ * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "所有药物每剂2美元。Dennis Doe在药物和治疗上总共花了多少钱？",
    "query": "SELECT med_cost + pro_cost AS total_cost FROM ( SELECT 2 * SUM ( A.dose ) AS med_cost FROM Prescribes A JOIN Patient B ON A.Patient = B.SSN WHERE B.name = \"Dennis Doe\" ) JOIN ( SELECT SUM ( COST ) AS pro_cost FROM Procedures A JOIN Undergoes B ON A.Code = B.Procedures JOIN Patient C ON B.Patient = C.SSN WHERE C.name = \"Dennis Doe\" )",
    "reasoning_type": "+ * C",
    "commonsense_knowledge": "Total price is calculated by multiplying quantity with unit price."
  },
  {
    "input": "所有药物每剂2美元。假如丹尼斯·多伊2008年4月30日16:53多买了10剂Thesisin，他在药物和治疗上总共花了多少钱？",
    "query": "SELECT med_cost + pro_cost + 10 * 2 AS total_cost FROM ( SELECT 2 * SUM ( A.dose ) AS med_cost FROM Prescribes A JOIN Patient B ON A.Patient = B.SSN WHERE B.name = \"Dennis Doe\" AND A.Date != \"2008-04-30 16:53\" ) JOIN ( SELECT SUM ( COST ) AS pro_cost FROM Procedures A JOIN Undergoes B ON A.Code = B.Procedures JOIN Patient C ON B.Patient = C.SSN WHERE C.name = \"Dennis Doe\" )",
    "reasoning_type": "+ * C H",
    "commonsense_knowledge": "Total price is calculated by multiplying quantity with unit price."
  },
  {
    "input": "John Wen 接受培训过的手术资格认证的有效期是多长？",
    "query": "SELECT C.name , CAST ( julianday ( A.CertificationExpires ) - julianday ( A.CertificationDate ) AS INTEGER ) AS lifetime FROM Trained_In A JOIN Physician B ON A.Physician = B.EmployeeID JOIN Procedures C ON C.code = A.Treatment WHERE B.name = \"John Wen\"",
    "reasoning_type": "- C",
    "commonsense_knowledge": "Lifetime of the certification is computed substacting certification start date from certification expire date."
  },
  {
    "input": "John Wen 接受培训过的手术资格认证的有效期是多长，假如有效期延长180天？",
    "query": "SELECT C.name , CAST ( julianday ( A.CertificationExpires ) - julianday ( A.CertificationDate ) AS INTEGER ) + 180 AS lifetime FROM Trained_In A JOIN Physician B ON A.Physician = B.EmployeeID JOIN Procedures C ON C.code = A.Treatment WHERE B.name = \"John Wen\"",
    "reasoning_type": "- + C H",
    "commonsense_knowledge": "Lifetime of the certification is computed substacting certification start date from certification expire date."
  },
  {
    "input": "同时属于外科部门和普通内科部门的医生在属于外科的医生中所占的比例是多少？",
    "query": "SELECT 1.0 * COUNT ( * ) / ( SELECT COUNT ( * ) FROM Affiliated_With WHERE Department = ( SELECT DepartmentID FROM Department WHERE Name = \"Surgery\" ) ) AS prop FROM ( select * from Affiliated_With as A join department as B on A.Department = B.DepartmentID WHERE B.Name = \"Surgery\" or B.Name = \"General Medicine\" GROUP BY Physician HAVING COUNT ( DISTINCT ( B.Name ) ) = 2 )",
    "reasoning_type": "/ *",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如基思·杜德米斯特既属于外科部门又属于普通内科部门，同时属于外科部门和普通内科部门的医生在属于外科的医生中所占的比例是多少？",
    "query": "SELECT 1.0 * ( 1 + COUNT ( * ) ) / ( 1 + ( SELECT COUNT ( * ) FROM Affiliated_With as A join Physician as B on A.Physician = B.EmployeeID WHERE B.Name != \"Keith Dudermeister\" and Department = ( SELECT DepartmentID FROM Department WHERE Name = \"Surgery\" ) ) ) AS prop FROM ( select * from Affiliated_With as A join department as B on A.Department = B.DepartmentID join Physician as C on A.Physician = C.EmployeeID WHERE C.Name != \"Keith Dudermeister\" and ( B.Name = \"Surgery\" or B.Name = \"General Medicine\" ) GROUP BY Physician HAVING COUNT ( DISTINCT ( B.Name ) ) = 2 )",
    "reasoning_type": "+ / * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "治疗的最高价格与最低价格相比是多少倍？",
    "query": "SELECT 1.0 * MAX ( Cost ) / MIN ( Cost ) AS times FROM Procedures",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "治疗的最高价格与最低价格相比是多少倍，如果最低价提高了75%？",
    "query": "SELECT 1.0 * MAX ( Cost ) / ( ( 1 + 0.75 ) * MIN ( Cost ) ) AS times FROM Procedures",
    "reasoning_type": "+ * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "治疗费用高于1000的案例占治疗案例总数的多少？",
    "query": "SELECT 1.0 * COUNT ( * ) / ( SELECT COUNT ( * ) FROM Procedures ) FROM Procedures WHERE Cost > 1000",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "不使用Procrastin-X的患者占患者总数的多少？",
    "query": "SELECT 1.0 - 1.0 * COUNT ( DISTINCT ( Patient ) ) / ( SELECT COUNT ( DISTINCT ( SSN ) ) FROM Patient ) AS prop FROM Medication A JOIN Prescribes B ON A.code = B.Medication WHERE A.Name = \"Procrastin-X\"",
    "reasoning_type": "- * /",
    "commonsense_knowledge": ""
  },
  {
    "input": "丹尼斯·多伊最昂贵的治疗和最便宜的治疗之间有多少区别？",
    "query": "SELECT MAX ( A.Cost ) - MIN ( A.Cost ) AS diff FROM Procedures A JOIN Undergoes B ON A.Code = B.Procedures JOIN Patient C ON C.SSN = B.Patient WHERE C.Name = \"Dennis Doe\"",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "如果每个治疗都涨价50%，丹尼斯·多伊做的最昂贵的治疗和最便宜的治疗相差多少钱？",
    "query": "SELECT ( ( 1 + 0.5 ) * MAX ( A.Cost ) ) - ( ( 1 + 0.5 ) * MIN ( A.Cost ) ) AS diff FROM Procedures A JOIN Undergoes B ON A.Code = B.Procedures JOIN Patient C ON C.SSN = B.Patient WHERE C.Name = \"Dennis Doe\"",
    "reasoning_type": "- + * H",
    "commonsense_knowledge": ""
  },
  {
    "input": "可用房间占房间总数的多少？",
    "query": "SELECT 1.0 * COUNT ( * ) / ( SELECT COUNT ( * ) FROM Room ) AS prop FROM Room WHERE Unavailable = \"0\"",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "如果每个房间有两张床，那么可用的房间总共可以容纳多少人？",
    "query": "SELECT 2 * COUNT ( * ) AS n_people FROM Room WHERE Unavailable = \"0\"",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "预约ID为13216584的预约持续时间是多少分钟？",
    "query": "SELECT ( strftime ( \"%s\" , End ) - strftime ( \"%s\" , Start ) ) / 60.0 AS time FROM Appointment WHERE AppointmentID = \"13216584\"",
    "reasoning_type": "- / C",
    "commonsense_knowledge": "One hour is 60 minutes."
  },
  {
    "input": "如果预约ID为13216584的预约持续时间延长了半个小时，它的持续了多少分钟？",
    "query": "SELECT ( strftime ( \"%s\" , End ) - strftime ( \"%s\" , Start ) ) / 60.0 + 30 AS time FROM Appointment WHERE AppointmentID = \"13216584\"",
    "reasoning_type": "- + / C H",
    "commonsense_knowledge": "Half an hour is 30 minutes."
  },
  {
    "input": "如果每次培训的培训费是50英镑，那么谁是在培训上花费最多的医生？列出他的姓名、职位和培训费用。",
    "query": "SELECT A.Name , A.Position , 50 * COUNT ( * ) AS cost FROM Physician A JOIN Trained_In B ON A.EmployeeID = B.Physician GROUP BY A.EmployeeID HAVING COUNT ( * ) = ( SELECT MAX ( training_count ) FROM ( SELECT COUNT ( * ) AS training_count FROM Trained_In GROUP BY Physician ) )",
    "reasoning_type": "*",
    "commonsense_knowledge": ""
  },
  {
    "input": "顶层的可用房间比最底层的多多少？",
    "query": "SELECT COUNT ( * ) - ( SELECT COUNT ( * ) FROM Room WHERE Unavailable = \"0\" AND BlockFloor = ( SELECT MIN ( BlockFloor ) FROM Room ) ) AS diff FROM Room WHERE Unavailable = \"0\" AND BlockFloor = ( SELECT MAX ( BlockFloor ) FROM Room )",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "假设在顶层有20个可用房间，顶层的可用房间比最底层的多多少？",
    "query": "SELECT 20 - ( SELECT COUNT ( * ) FROM Room WHERE Unavailable = \"0\" AND BlockFloor = ( SELECT MIN ( BlockFloor ) FROM Room ) ) AS diff",
    "reasoning_type": "- H",
    "commonsense_knowledge": ""
  }
]