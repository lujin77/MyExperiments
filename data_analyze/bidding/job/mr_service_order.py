# -*- coding:utf-8 -*-

from mrjob.job import MRJob
import time


class MROrderTrade(MRJob):
	def mapper_init(self):
		self.DELIMITER = ','
		self.TITLE = ['service_order_id', 'product_type_id', 'fixed_product_id', 'city', 'create_time', 'total_amount',
					  'origin_amount', 'sharing_amount', 'status', 'expect_start_time', 'expect_end_time', 'start_time',
					  'end_time', 'user_id', 'corporate_id', 'car_id', 'driver_id', 'driver_name', 'user_type',
					  'car_type_id',
					  'coupon_name', 'coupon_type', 'source', 'coupon_facevalue', 'dependable_distance',
					  'actual_time_length',
					  'time_length', 'passenger_name', 'is_asap', 'car_type', 'car_brand', 'invoice', 'start_position',
					  'end_position', 'coupon_member_id', 'msg', 'comment', 'reason_id', 'deposit', 'pay_amount',
					  'is_auto_dispatch', 'app_msg', 'regulatepan_amount', 'regulatedri_amount', 'update_time',
					  'origin_sharing_amount', 'pay_status', 'flag', 'confirm_time', 'version', 'app_version',
					  'balance_status',
					  'receipt_title', 'arrival_time', 'driver_night_amount', 'highway_amount', 'parking_amount',
					  'is_night',
					  'deadhead_distance', 'extension', 'driver_service_amount', 'predict_origin_amount',
					  'predict_amount',
					  'start_latitude', 'start_longitude', 'compute_amount', 'addons_amount', 'expect_start_latitude',
					  'expect_start_longitude', 'expect_end_latitude', 'expect_end_longitude', 'system_distance',
					  'mileage',
					  'car_type_ids', 'regulatepan_reason', 'regulatedri_reason', 'abnormal_mark', 'runtime']

		self.COLUMES = ['predict_origin_amount',
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

	def mapper(self, _, line):
		# split log
		segs = line.split('\001')
		try:
			tuple = dict(zip(self.TITLE, segs))
			timeArray = time.localtime(float(tuple['create_time']))
			key = time.strftime("%Y-%m-%d %H:00:00", timeArray)
			value = self.filter_values(tuple)
			yield key, self.DELIMITER.join(value)
		except ValueError, e:
			print e.message, e.args
			self.increment_counter("MROrderTrade", "log_parse_error", amount=1)

	def reducer(self, key, values):
		for value in values:
			yield key, value

	def filter_values(self, line_dict):
		value_list = []
		for tag in self.COLUMES:
			value_list.append(line_dict[tag])
		return value_list

if __name__ == '__main__':
	MROrderTrade.run()
