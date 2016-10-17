input = """
service_order_id        bigint
expect_start_latitude   double
expect_start_longitude  double
expect_end_latitude     double
expect_end_longitude    double
expect_start_time       timestamp
expect_start_day_of_week        int
expect_start_hour_of_day        int
expect_end_time         int
expect_end_day_of_week  int
expect_end_hour_of_day  int
predict_distance        int
car_type_ids            int
dispatch_type           string
deadhead_distance       int
predict_origin_amount   int
predict_amount          int
sum_valid_driver        bigint
mean_driver_distance    double
order_status            tinyint
cancel_reason_id        int
total_round             int
final_add_rate          float
final_bidding_rate      float
first_response_round    int
first_response_add_rate float
max_no_accept_round     int
max_no_accept_add_rate  float
"""

title = []
for line in input.split('\n'):
	tmp = []
	for tag in line.split(' '):
		if tag != '':
			tmp.append(tag)
	if len(tmp) == 2:
		title.append(tmp[0])
	continue
	#print tmp

	if len(tmp) == 2:
		if tmp[1] in ['bigint', 'double', 'int', 'float']:
			print "var %s = df.filter(\"%s is null or %s=0\").count" % (tmp[0], tmp[0], tmp[0])
		else:
			print "var %s = df.filter(\"%s is null\").count" % (tmp[0], tmp[0])

print ','.join(title)




