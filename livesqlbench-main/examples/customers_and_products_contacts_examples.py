customers_and_products_contacts_examples=[
  {
    "input": "斯特林至今花了多少钱了？",
    "query": "SELECT SUM(C.order_quantity * D.product_price) AS cost FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.customer_name = 'Sterling'",
    "reasoning_type": "* C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "假如所有古琦产品的单价都是600，斯特林至今花了多少钱了？",
    "query": "SELECT SUM(cost) FROM (SELECT SUM(C.order_quantity * 600) AS cost FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.customer_name = 'Sterling' AND product_name = 'gucci' UNION SELECT SUM(C.order_quantity * D.product_price) AS cost FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.customer_name = 'Sterling' AND product_name != 'gucci')",
    "reasoning_type": "* C H",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "斯特林是会员，买所有产品都有八折优惠，他至今花了多少钱了？",
    "query": "SELECT SUM(C.order_quantity * D.product_price * (1.0 - 1.0 * 20 / 100)) AS cost_after_discount FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.customer_name = 'Sterling'",
    "reasoning_type": "* C - /",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "斯特林是会员，买所有产品都有八折优惠，他至今节约了多少钱了？",
    "query": "SELECT SUM(C.order_quantity * D.product_price * (1.0 * 20 / 100)) AS saved_money FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.customer_name = 'Sterling'",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "按照用户至今的花费总额的从多到少，列出客户id、姓名、地址、电话、电子邮件。",
    "query": "SELECT A.customer_id, A.customer_name, A.customer_address, A.customer_phone, A.customer_email, SUM(C.order_quantity * D.product_price) AS cost FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id GROUP BY A.customer_name ORDER BY cost DESC",
    "reasoning_type": "* C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "克莱奥最新的订单总价多少？",
    "query": "SELECT cost FROM (SELECT B.order_date, SUM(C.order_quantity * D.product_price) AS cost FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.customer_name = 'Cleo' GROUP BY C.order_id) ORDER BY order_date DESC LIMIT 1",
    "reasoning_type": "* C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "克莱奥最新的订单总价多少，假如他每个产品都买了5个？",
    "query": "SELECT cost FROM (SELECT B.order_date, SUM(5.0 * D.product_price) AS cost FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.customer_name = 'Cleo' GROUP BY C.order_id) ORDER BY order_date DESC LIMIT 1",
    "reasoning_type": "* C H",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "苹果产品的成本是出售价格的40%，古琦产品的成本是出售价格的20%，其他产品的成本是出售价格的50%。请列出各个产品的ID、名字、销售量、销售额、毛利润总额。",
    "query": "SELECT B.product_id, B.product_name, SUM(A.order_quantity) AS quantity, SUM(A.order_quantity * B.product_price) AS revenue, SUM(A.order_quantity * B.product_price) * (1.0 - 40.0 / 100) AS profit FROM Order_Items A JOIN Products B ON A.product_id = B.product_id WHERE B.product_name = 'Apple' GROUP BY B.product_id UNION SELECT B.product_id, B.product_name, SUM(A.order_quantity) AS quantity, SUM(A.order_quantity * B.product_price) AS revenue, SUM(A.order_quantity * B.product_price) * (1.0 - 20.0 / 100) AS profit FROM Order_Items A JOIN Products B ON A.product_id = B.product_id WHERE B.product_name = 'gucci' GROUP BY B.product_id UNION SELECT B.product_id, B.product_name, SUM(A.order_quantity) AS quantity, SUM(A.order_quantity * B.product_price) AS revenue, SUM(A.order_quantity * B.product_price) * (1.0 - 50.0 / 100) AS profit FROM Order_Items A JOIN Products B ON A.product_id = B.product_id WHERE B.product_name != 'Apple' AND B.product_name != 'gucci' GROUP BY B.product_id UNION SELECT B.product_id, B.product_name, 0, 0, 0 FROM (SELECT product_id FROM Products A EXCEPT SELECT B.product_id FROM Order_Items A JOIN Products B ON A.product_id = B.product_id) A JOIN Products B ON A.product_id = B.product_id",
    "reasoning_type": "- * / C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity. Gross profit is calculated by subtracting costs of goods from revenue."
  },
  {
    "input": "苹果产品的成本是出售价格的40%，古琦产品的成本是出售价格的20%，其他产品的成本是出售价格的50%。假如所有苹果产品降价了15%了，请列出各个产品的ID、名字、销售量、销售额、毛利润总额。",
    "query": "SELECT B.product_id, B.product_name, SUM(A.order_quantity) AS quantity, SUM(A.order_quantity * (B.product_price * (1.0 - 15.0 / 100))) AS revenue, SUM(A.order_quantity * (B.product_price * (1.0 - 15.0 / 100))) * (1.0 - 40.0 / 100) AS profit FROM Order_Items A JOIN Products B ON A.product_id = B.product_id WHERE B.product_name = 'Apple' GROUP BY B.product_id UNION SELECT B.product_id, B.product_name, SUM(A.order_quantity) AS quantity, SUM(A.order_quantity * B.product_price) AS revenue, SUM(A.order_quantity * B.product_price) * (1.0 - 20.0 / 100) AS profit FROM Order_Items A JOIN Products B ON A.product_id = B.product_id WHERE B.product_name = 'gucci' GROUP BY B.product_id UNION SELECT B.product_id, B.product_name, SUM(A.order_quantity) AS quantity, SUM(A.order_quantity * B.product_price) AS revenue, SUM(A.order_quantity * B.product_price) * (1.0 - 50.0 / 100) AS profit FROM Order_Items A JOIN Products B ON A.product_id = B.product_id WHERE B.product_name != 'Apple' AND B.product_name != 'gucci' GROUP BY B.product_id UNION SELECT B.product_id, B.product_name, 0, 0, 0 FROM (SELECT product_id FROM Products A EXCEPT SELECT B.product_id FROM Order_Items A JOIN Products B ON A.product_id = B.product_id) A JOIN Products B ON A.product_id = B.product_id",
    "reasoning_type": "- * / C H",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity. Gross profit is calculated by subtracting costs of goods from revenue."
  },
  {
    "input": "有百分之多少的订单已经已完成？",
    "query": "SELECT 1.0 * COUNT(*) / (SELECT COUNT(*) FROM Customer_Orders) * 100 AS percent FROM Customer_Orders WHERE order_status_code = 'Completed'",
    "reasoning_type": "* /",
    "commonsense_knowledge": ""
  },
  {
    "input": "假如2000年以前的订单都完成了，有百分之多少的订单已经已完成？",
    "query": "SELECT 100 - 1.0 * COUNT(*) / (SELECT COUNT(*) FROM Customer_Orders) * 100 AS percent FROM Customer_Orders WHERE strftime('%Y', order_date) >= '2000' AND order_status_code != 'Completed'",
    "reasoning_type": "- * / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "有多个联系方式的用户的姓名和第一个订单的金额是多少？",
    "query": "SELECT customer_name, price FROM (SELECT M.customer_id, N.customer_name, M.price, MIN(M.order_date) FROM (SELECT B.customer_id, B.order_id, B.order_date, SUM(A.order_quantity * C.product_price) AS price FROM Order_Items A JOIN Customer_Orders B ON A.order_id = B.order_id JOIN Products C ON C.product_id = A.product_id GROUP BY B.customer_id, B.order_id) M JOIN Customers N ON M.customer_id = N.customer_id WHERE M.customer_id IN (SELECT customer_id FROM Contacts GROUP BY customer_id HAVING COUNT(*) > 1) GROUP BY M.customer_id)",
    "reasoning_type": "* C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "假如2000年前所有苹果产品的单价都是888，有多个联系方式的用户第一个订单的金额是多少？",
    "query": "SELECT customer_name, price FROM (SELECT M.customer_id, N.customer_name, M.price, MIN(M.order_date) FROM (SELECT customer_id, order_id, order_date, SUM(price) AS price FROM (SELECT B.customer_id, B.order_id, B.order_date, SUM(A.order_quantity * 888.0) AS price FROM Order_Items A JOIN Customer_Orders B ON A.order_id = B.order_id JOIN Products C ON C.product_id = A.product_id WHERE C.product_name = 'Apple' AND strftime('%Y', B.order_date) < '2000' GROUP BY B.customer_id, B.order_id UNION SELECT B.customer_id, B.order_id, B.order_date, SUM(A.order_quantity * C.product_price) AS price FROM Order_Items A JOIN Customer_Orders B ON A.order_id = B.order_id JOIN Products C ON C.product_id = A.product_id WHERE C.product_name != 'Apple' OR strftime('%Y', B.order_date) >= '2000' GROUP BY B.customer_id, B.order_id) GROUP BY customer_id, order_id) M JOIN Customers N ON M.customer_id = N.customer_id WHERE M.customer_id IN (SELECT customer_id FROM Contacts GROUP BY customer_id HAVING COUNT(*) > 1) GROUP BY M.customer_id)",
    "reasoning_type": "* C H",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "哪些用户曾有过多个不同的地址，给出他们的名字，以及它们每个人至今用得最久的地址的邮编。",
    "query": "SELECT customer_name, zip_postcode FROM (SELECT C.customer_name, B.zip_postcode, MAX(julianday(A.date_to) - julianday(A.date_from)) FROM Customer_Address_History A JOIN Addresses B ON A.address_id = B.address_id JOIN Customers C ON C.customer_id = A.customer_id GROUP BY A.customer_id HAVING COUNT(*) > 1)",
    "reasoning_type": "- C",
    "commonsense_knowledge": "The time duration is calculated by subtracting the start time from the end time."
  },
  {
    "input": "哪些用户从未有过多个不同的地址，给出他们的名字，以及它们每个人的邮编地址。",
    "query": "SELECT C.customer_name, B.zip_postcode FROM Customer_Address_History A JOIN Addresses B ON A.address_id = B.address_id JOIN Customers C ON C.customer_id = A.customer_id GROUP BY A.customer_id HAVING COUNT(*) = 1",
    "reasoning_type": "- C",
    "commonsense_knowledge": "The time duration is calculated by subtracting the start time from the end time."
  },
  {
    "input": "哪个用户在2000年以后再也没有下过订单，列出他的id、名字、邮件以及最后一笔订单的金额？",
    "query": "SELECT customer_id, customer_name, customer_email, price AS last_order_price FROM (SELECT M.customer_id, N.customer_name, N.customer_email, M.price, MAX(M.order_date) FROM (SELECT B.customer_id, B.order_id, B.order_date, SUM(A.order_quantity * C.product_price) AS price FROM Order_Items A JOIN Customer_Orders B ON A.order_id = B.order_id JOIN Products C ON C.product_id = A.product_id GROUP BY B.customer_id, B.order_id) M JOIN Customers N ON M.customer_id = N.customer_id WHERE M.customer_id IN (SELECT customer_id FROM Customer_Orders GROUP BY customer_id HAVING strftime('%Y', MAX(order_date)) < '2000') GROUP BY M.customer_id)",
    "reasoning_type": "* C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "用户单笔订单总价超过1000可以获得222积分，超过2000可以再获得666积分。哪个用户目前获得的总积分最多？给出他的ID。",
    "query": "SELECT customer_id FROM (SELECT customer_id, COUNT(*) * (666 + 222) AS points FROM (SELECT B.customer_id, B.order_id, B.order_date, SUM(A.order_quantity * C.product_price) AS price FROM Order_Items A JOIN Customer_Orders B ON A.order_id = B.order_id JOIN Products C ON C.product_id = A.product_id GROUP BY B.customer_id, B.order_id) WHERE price > 2000 GROUP BY customer_id UNION SELECT customer_id, COUNT(*) * 222 AS points FROM (SELECT B.customer_id, B.order_id, B.order_date, SUM(A.order_quantity * C.product_price) AS price FROM Order_Items A JOIN Customer_Orders B ON A.order_id = B.order_id JOIN Products C ON C.product_id = A.product_id GROUP BY B.customer_id, B.order_id) WHERE price > 1000 AND price < 2000 GROUP BY customer_id) GROUP BY customer_id ORDER BY points DESC LIMIT 1",
    "reasoning_type": "+ * C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "衣服的平均单价比硬件高多少？",
    "query": "SELECT clothes_avg - hw_avg AS diff FROM (SELECT AVG(product_price) AS hw_avg FROM Products WHERE product_type_code = 'Hardware') JOIN (SELECT AVG(product_price) AS clothes_avg FROM Products WHERE product_type_code = 'Clothes')",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "如果衣服涨价20%，衣服的平均单价比硬件高多少？",
    "query": "SELECT (1 + 20.0 / 100) * clothes_avg - hw_avg AS diff FROM (SELECT AVG(product_price) AS hw_avg FROM Products WHERE product_type_code = 'Hardware') JOIN (SELECT AVG(product_price) AS clothes_avg FROM Products WHERE product_type_code = 'Clothes')",
    "reasoning_type": "+ * - / H",
    "commonsense_knowledge": ""
  },
  {
    "input": "曾使用过首府为法兰克福的州的地址的用户有多少，他们中女性的比例是多少？",
    "query": "SELECT n_total, 1.0 * n_female / n_total AS female_ratio FROM (SELECT COUNT(DISTINCT(A.customer_id)) AS n_female FROM Customer_Address_History A JOIN Addresses B ON A.address_id = B.address_id JOIN Contacts C ON A.customer_id = C.customer_id WHERE B.state_province_county = 'Kentucky' AND C.gender = 'female') JOIN (SELECT COUNT(DISTINCT(A.customer_id)) AS n_total FROM Customer_Address_History A JOIN Addresses B ON A.address_id = B.address_id WHERE B.state_province_county = 'Kentucky')",
    "reasoning_type": "* / C",
    "commonsense_knowledge": "Frankfort is the capital city of Kentucky state."
  },
  {
    "input": "给出销售量最高的产品的ID，名字，销量，以及给出其比销售量最低的产品的销售量高多少？",
    "query": "SELECT t1.product_id, t1.product_name, MAX(t1.quantity) AS max_quantity, t2.diff FROM (SELECT A.product_id, B.product_name, SUM(order_quantity) AS quantity FROM Order_Items A JOIN Products B ON A.product_id = B.product_id GROUP BY A.product_id UNION SELECT product_id, product_name, 0 AS quantity FROM Products WHERE product_id NOT IN (SELECT A.product_id FROM Order_Items A JOIN Products B ON A.product_id = B.product_id GROUP BY A.product_id)) t1 JOIN (SELECT MAX(quantity) - MIN(quantity) AS diff FROM (SELECT A.product_id, B.product_name, SUM(order_quantity) AS quantity FROM Order_Items A JOIN Products B ON A.product_id = B.product_id GROUP BY A.product_id UNION SELECT product_id, product_name, 0 AS quantity FROM Products WHERE product_id NOT IN (SELECT A.product_id FROM Order_Items A JOIN Products B ON A.product_id = B.product_id GROUP BY A.product_id))) t2",
    "reasoning_type": "-",
    "commonsense_knowledge": ""
  },
  {
    "input": "给出销售量最高的产品的ID，名字。假如它的销售量又增加了500，它的销售量变成了多少，其比销售量最低的产品的销售量高多少？",
    "query": "SELECT t1.product_id, t1.product_name, MAX(t1.quantity) + 500 AS max_quantity, t2.diff + 500 FROM (SELECT A.product_id, B.product_name, SUM(order_quantity) AS quantity FROM Order_Items A JOIN Products B ON A.product_id = B.product_id GROUP BY A.product_id UNION SELECT product_id, product_name, 0 AS quantity FROM Products WHERE product_id NOT IN (SELECT A.product_id FROM Order_Items A JOIN Products B ON A.product_id = B.product_id GROUP BY A.product_id)) t1 JOIN (SELECT MAX(quantity) - MIN(quantity) AS diff FROM (SELECT A.product_id, B.product_name, SUM(order_quantity) AS quantity FROM Order_Items A JOIN Products B ON A.product_id = B.product_id GROUP BY A.product_id UNION SELECT product_id, product_name, 0 AS quantity FROM Products WHERE product_id NOT IN (SELECT A.product_id FROM Order_Items A JOIN Products B ON A.product_id = B.product_id GROUP BY A.product_id))) t2",
    "reasoning_type": "- + H",
    "commonsense_knowledge": ""
  },
  {
    "input": "使用信用卡付款需要交支付金额5%的手续费。列出每个客户的姓名，其每笔订单的id，以及每笔订单共花了多少钱。",
    "query": "SELECT A.customer_name, B.order_id, (C.order_quantity * D.product_price) * (1 + 5.0 / 100) AS cost_plus_fee FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.payment_method_code = 'Credit Card' GROUP BY A.customer_name, B.order_id UNION SELECT A.customer_name, B.order_id, C.order_quantity * D.product_price AS cost_plus_fee FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.payment_method_code != 'Credit Card' GROUP BY A.customer_name, B.order_id",
    "reasoning_type": "+ * / C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "使用信用卡付款需要交支付金额5%的手续费。假如每个产品的单价都是99，列出每个客户的姓名，其每笔订单的id，以及每笔订单共花了多少钱。",
    "query": "SELECT A.customer_name, B.order_id, (C.order_quantity * 99) * (1 + 5.0 / 100) AS cost_plus_fee FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.payment_method_code = 'Credit Card' GROUP BY A.customer_name, B.order_id UNION SELECT A.customer_name, B.order_id, C.order_quantity * 99 AS cost_plus_fee FROM Customers A JOIN Customer_Orders B ON A.customer_id = B.customer_id JOIN Order_Items C ON B.order_id = C.order_id JOIN Products D ON C.product_id = D.product_id WHERE A.payment_method_code != 'Credit Card' GROUP BY A.customer_name, B.order_id",
    "reasoning_type": "+ * / C H",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "列出年份和对应的年销售额。",
    "query": "SELECT strftime('%Y', A.order_date) AS year, SUM(B.order_quantity * C.product_price) AS annual_sales_revenue FROM Customer_Orders A JOIN Order_Items B ON A.order_id = B.order_id JOIN Products C ON B.product_id = C.product_id GROUP BY strftime('%Y', A.order_date)",
    "reasoning_type": "* C",
    "commonsense_knowledge": "Total price is calculated by multiplying unit price to quantity."
  },
  {
    "input": "列出苹果产品的最高价、最低价、方差。",
    "query": "SELECT max_price, min_price, variance FROM (SELECT 1.0 * (product_price - AVG(product_price)) * (product_price - AVG(product_price)) / COUNT(*) AS variance FROM Products WHERE product_name = 'Apple') JOIN (SELECT MAX(product_price) AS max_price, MIN(product_price) AS min_price FROM Products WHERE product_name = 'Apple')",
    "reasoning_type": "- * / C",
    "commonsense_knowledge": "The variance is mean squared difference between each data point and the centre of the distribution measured by the mean."
  }
]