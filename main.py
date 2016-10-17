#! -*- coding:utf-8 -*-

# file = "/user/lujin/tmp/bj_dispatch_detail_info/dispatch_detail_info"
# table = "dispatch_detail_info"
# t = 20160901
# for i in xrange(0, 25):
#     date = t + i
#     sql = "load data inpath '%s/dt=%d' into table %s PARTITION (dt=%s);" % (file, date, table, date)
#     print sql
#
#
lable = []
with open('test.txt', 'r') as fp:
    for line in fp:
        lable.append(line.split(" ")[0])

print len(lable)
print ','.join(lable)

t = 20160901
for i in xrange(0, 25):
    date = t + i
    sql = "insert into bj_dispatch_detail_info partition (dt=%d) select datetime,null1,service_order_id,round,batch,flag,driver_id,distance,dispatch_time,dispatch_lat,dispatch_lng,dispatch_total_rate,dispatch_snapshot,response_time,accept_status,response_lat,response_lng,response_distance,response_time_length,decision_time,decision_total_rate,decision_result,decision_failure_reason,decision_msg_snapshot,subtract_amount,add_price_set,response_snapshot,is_assigned,route_distance,route_time_length,distance_time_length from dispatch_detail_info where dt=%d and service_order_id in (select service_order_id from ods_service_order where city='bj' and dt=%d);" % (date, date, date)
    print sql
