import json
from pprint import pprint

dispatch_snapshot="{\"is_self_employed\":0,\"country\":\"CN\",\"driver_id\":\"2565028\",\"flag\":61454,\"base_score\":20,\"driver_type\":1,\"color\":2,\"distance\":235,\"city\":\"bj\",\"latitude\":39.771577217653,\"total_rate\":10000,\"device_type\":\"2\",\"audit_status\":20,\"has_logistics\":0,\"discount_rate\":100,\"distance_time_length\":70.5,\"contribution_rate\":54,\"last_position_time\":1474300709,\"surpport_face_pay\":1,\"evaluation\":970,\"evaluation_rate\":97,\"destwish_rate\":0,\"has_qualified\":0,\"contribution\":42100,\"cellphone\":\"13956505707\",\"silence_end_at\":1473334500,\"work_status\":0,\"car_id\":2698951,\"brand\":\"\\u5954\\u9a70C\\u7ea7\",\"seat_num\":4,\"route_distance\":0,\"longitude\":116.35407275531,\"car_type_id\":2,\"route_time_length\":0,\"device_id\":2927252,\"base_score_rate\":20,\"good_comment_rate\":97,\"destwish\":0,\"driver_level\":1,\"version\":\"105\",\"car_brand_id\":6,\"car_model_id\":49,\"vehicle_number\":\"\\u7696HUR001\",\"name\":\"\\u5434\\u9e4f\",\"imei\":\"bae573c198b21c1019cb72fc51483e8a\",\"distance_rate\":100,\"is_assigned\":0,\"add_price_set\":{\"add_price_redispatch\":0,\"add_price_rate\":0,\"add_price_max_amount\":10000000,\"add_price_type\":0,\"add_price_vip\":0,\"strategy_id\":0,\"add_total_amount\":0,\"add_amount_str\":\"\",\"add_amount_str_full\":\"\"}}"
resp = json.loads(dispatch_snapshot)
pprint(resp)

for item in resp:
	print '''"dispatch_%s" => "%%{[%s][%s]}"''' % (item, "dispatch_snapshot", item)


add_price_set="{\"add_price_redispatch\":0,\"add_price_rate\":0,\"add_price_max_amount\":10000000,\"add_price_type\":0,\"add_price_vip\":0,\"strategy_id\":0,\"add_total_amount\":0,\"add_amount_str\":\"\",\"add_amount_str_full\":\"\"}"
resp = json.loads(add_price_set)
pprint(resp)

for item in resp:
	print '''"%s" => "%%{[%s][%s]}"''' % (item, "add_price_set", item)