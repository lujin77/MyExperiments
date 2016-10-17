
import sys

sys.path.append('/home/lujin/script')

from job.mr_service_order import MROrderTrade

mr_job = MROrderTrade(args=['-r', 'local', 'data/ods_service_order.mini.txt'])


COLUMES = ['predict_origin_amount',
						'predict_amount',
						'total_amount',
						'compute_amount',
						'pay_amount',
						# status
						'status',
						'is_asap',
						'is_auto_dispatch',
						'is_night',
						'abnormal_mark',
						# coparator
						'user_type',
						'corporate_id',
						# time
						'create_time',
						'confirm_time',
						'expect_start_time',
						'arrival_time',
						'start_time',
						'time_length',
						'actual_time_length',
						# cancle
						'reason_id',
						# extend
						'deadhead_distance',
						'system_distance',
						'product_type_id'
						]
with mr_job.make_runner() as runner:
	runner.run()
	print ','.join(COLUMES)
	for line in runner.stream_output():
		# Use the job's specified protocol to read the output
		key, value = mr_job.parse_output_line(line)
		print key + "," + value