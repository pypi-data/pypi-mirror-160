import re, json 

from zohavi.zbase.staple import ZStaple
from mclogger import MCLogger

class WebField( ZStaple ):
	def __init__(self, tables, app=None, logger=None):
		super().__init__(app = app, logger = logger )
		self.debug = True

		self._tables = tables
		self._table_lookup = self._calc_web_table_lookup()

		self.log_debug(f"Stored: {json.dumps(tables) }")

	def get_field(self, field_name):
		# for field in self._fields:
		# 	if field['id'] == field_name: return field
		return self._fields[field_name]
 
	def _calc_web_table_lookup(self):
		table_lookup = {}
		for index, table_rec in enumerate( self._tables ):
		#create new dict entry for each of the web fields
			for web_field_name in table_rec['fields'].keys():
				table_lookup[ web_field_name ] =  table_rec 
		return table_lookup

	#############################################################################################################
	#Validate form data in json format
	@MCLogger.logfunc_cls('logger')
	def validate(self, data, validate_fail_reason):
		validation_ok = True 
		self.log_debug( "validating:" + json.dumps(data ) )
		self.log_debug( "Master:" + json.dumps(self._tables ) )

		for data_row in data:	#loop through each web data field
			if not 'id' in data_row: raise Exception( f"Missing field [id] in {data_row}.  Json format shoudl have 'id' and 'value' elements")

			web_field_name = data_row['id']
			# breakpoint()
			if not web_field_name in self._table_lookup: raise Exception( f"[{web_field_name}] from submit data not found in schema { self._tables }")
			# table_ref = self._field_lookup[ web_field_name ]
			
			#Use the reverse lookup to find the table associated with the field
			field_info = self._table_lookup[ web_field_name ]['fields'][ web_field_name ]

			if field_info.get('validation', False):  #has validation
				self.log_debug( f" Checking validation {web_field_name}=>[{data_row['value']}] Rule:{json.dumps( field_info['validation']) } ") 

				validation_ok = validation_ok and self._validate_run_validation_rule( data_row['value'] , field_info['validation'], validate_fail_reason  )

			if field_info.get('transform', False):  #has transformation
				data_row['value'] = self._run_transformation( data_row['value'] , field_info['transform'] )
		return validation_ok


	#############################################################################################################
	#
	def _run_transformation(self, data_value, transform_rules):
		self.log_debug( f" data_value={data_value}; transform={json.dumps(transform_rules) }")

		ret_value = data_value
		for rule in transform_rules: 
			func = getattr(Transform, rule, Transform._func_not_found)  
			ret_value = func( ret_value , transform_rules[rule] )

		return ret_value


	#############################################################################################################
	#Run the actual validation rule
	def _validate_run_validation_rule(self, data_value, validation_rules, validate_fail_reason):
		validation_ok = True 
		# if not data_value: breakpoint()
		self.log_debug( f" data_value={data_value}; validation_rule={'required' in validation_rules.keys()}; required={validation_rules['required']== False}")
		if not data_value and 'required' in validation_rules.keys() and validation_rules['required'] == False: return True
		for rule in validation_rules: 
			func = getattr(Validate, rule, Validate._func_not_found)  
			ret_check = func( data_value , validation_rules[rule], self.log_error )	#Pass reference to error message for failed validatinos

			log_message = f"Validation check [{rule}:{validation_rules[rule]}] on [{data_value}] => {ret_check}"
			if ret_check:
				self.log_debug( log_message ) 
			else:
				validate_fail_reason['01'] = log_message
				self.log_error( log_message )

			validation_ok = validation_ok and ret_check

		self.log_debug("Returning validation check from :" + json.dumps(validation_rules) + " => " + str(validation_ok) )
		return validation_ok
 


class Transform(ZStaple):

	@staticmethod
	def _func_not_found( value, param) :
		Transform.log_error("transformation function not found")

	#############################################################################################################
	#Check if the current 
	@staticmethod
	def to_bool(value, param) :
		return Transform._map_value( value, {'':False, 'false':False, '0':False, 
											'True':True, 'true':True, '1':True, True:True} )
	@staticmethod
	def _map_value(value, map):
		return map.get( value, None)



class Validate(ZStaple):
	#############################################################################################################
	#Check if the current 
	@staticmethod
	def _get_data_field_field(  value, field_name):
		for data_fld in value:	#find the relevant data field in there
			if data_fld['id'] == field_name:
				return data_fld
		return None

	#############################################################################################################
	#validation function not found
	@staticmethod
	def _func_not_found( value, param, log_err_func=print  ):
		Validate.log(   f"Validtion function [{value}] not found", log_err_func)

	#############################################################################################################
	#Check that field is required 
	@staticmethod
	def required(  value, param, log_err_func=print   ):  
		if not param: return True
		return False if not value else True
		# return True

	#############################################################################################################
	#Check that field has min length as required
	@staticmethod
	def text_min_len(  value, param, log_err_func=print  ): 
		if len( str( value  ) ) >= param: return True
		return False

	#############################################################################################################
	#Check that field has max length as required
	@staticmethod
	def text_max_len(  value, param, log_err_func=print  ): 
		if len( str( value ) ) <= param: return True

		Validate.log(   "Text Length of [{value}] is {len( str( value ) )} which is greater than [{param}]", log_err_func)
		
		return False

	#############################################################################################################
	#Check that number is gte
	@staticmethod
	def num_gte(   value, param, log_err_func=print   ): 
		if int( value ) >= int(param): return True
		return False

	#############################################################################################################
	#Check that number is gte
	def num_lte(  value, param , log_err_func=print  ): 
		if int( value ) <= int(param): return True
		return False

	#############################################################################################################
	#Check that field has max length as required
	@staticmethod
	def is_url(  value, param=None, log_err_func=print ):  
		url_re = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))'
		url = re.findall(url_re, value )
		return True if url else False

	#############################################################################################################
	#Check that field has max length as required
	@staticmethod
	def is_ip(  value, param=None, log_err_func=print   ):  
		url_re = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
		url = re.findall(url_re, value )
		return True if url else False


	#############################################################################################################
	#Check that number is gte
	@staticmethod
	def is_unix_path(  value , param=None, log_err_func=print  ): 
		path_re = r'\/?(\/?.+?)+[\/]?'
		path = re.findall(path_re, value )
		return True if path else False

	#############################################################################################################
	#validation function not found
	@staticmethod
	def is_bool( value, param, log_err_func=print  ):
		valid_values = [ True, False, '', None ]
		if value in valid_values: return True

		Validate.log(  f"Value [{value}] is not a boolean", log_err_func)

		return False 

	@staticmethod
	def log( message, log_err_func=print  ):
		log_err_func( "Validation Failture: " + message )
