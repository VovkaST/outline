class Contact(object):

	TEMPLATE_FOLDER = 'contact/'
	
	def __init__(self, base):
		self.__base__ = base

	def add(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.add
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'add.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def update(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.update
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'update.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response 

	def update_custom_data(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.updateCustomData
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'updateCustomData.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def get(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.get
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'get.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def get_list(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.getList
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'getList.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def manage_planfix_access(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.managePlanfixAccess
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'managePlanfixAccess.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def update_user_info(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.updateUserInfo
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'updateUserInfo.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def update_contractors(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.updateContractors
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'updateContractors.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def get_phone_types(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.getPhoneTypes
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'getPhoneTypes.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def get_group_list(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.getGroupList
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'getGroupList.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response

	def delete(self, kwargs):
		"""
		https://planfix.ru/docs/%D0%9F%D0%BB%D0%B0%D0%BD%D0%A4%D0%B8%D0%BA%D1%81_API_contact.delete
		"""
		TEMPLATE_NAME = self.TEMPLATE_FOLDER + 'delete.xml'

		response = self.__base__._get_response(TEMPLATE_NAME, kwargs)

		return response
		