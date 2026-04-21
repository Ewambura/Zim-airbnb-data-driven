from baseObject import baseObject
import datetime


class Property_Image(baseObject):
	def __init__(self, config_path='config.yml'):
		self.setup(config_path)

	def getByPropertyId(self, property_id):
		# Note: column is property_Id with capital I
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}` WHERE `property_Id` = %s;'''
		self.cur.execute(sql, [property_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getImageById(self, image_id):
		self.getById(image_id)
		return self.data

	def verifyOwnership(self, property_id, owner_id):
		sql = '''SELECT 1 FROM `PROPERTY` WHERE `property_id` = %s AND `owner_id` = %s;'''
		self.cur.execute(sql, [property_id, owner_id])
		result = self.cur.fetchone()
		return result is not None

	def createImage(self, property_id, owner_id, caption, image_url, date_uploaded=None):
		if not self.verifyOwnership(property_id, owner_id):
			return {'success': False, 'error': 'You do not own this property'}

		if date_uploaded is None:
			date_uploaded = datetime.datetime.now().strftime('%Y-%m-%d')

		image_data = {
			'property_Id': property_id,
			'caption': caption,
			'image_url': image_url,
			'date_uploaded': date_uploaded
		}
		self.set(image_data)
		self.insert()
		return {'success': True, 'image_id': self.data[0].get(self.pk)}

	def updateImage(self, image_id, owner_id, caption=None, image_url=None):
		self.getById(image_id)
		if len(self.data) == 0:
			return {'success': False, 'error': 'Image not found'}

		property_id = self.data[0]['property_Id']

		if not self.verifyOwnership(property_id, owner_id):
			return {'success': False, 'error': 'You do not own this property'}

		updates = []
		tokens = []
		if caption is not None:
			updates.append('`caption` = %s')
			tokens.append(caption)
		if image_url is not None:
			updates.append('`image_url` = %s')
			tokens.append(image_url)

		if not updates:
			return {'success': False, 'error': 'No fields to update'}

		tokens.append(image_id)
		sql = f'''UPDATE `{self.tn}` SET {', '.join(updates)} WHERE `{self.pk}` = %s;'''
		self.cur.execute(sql, tokens)
		return {'success': True}

	def deleteImage(self, image_id, owner_id):
		self.getById(image_id)
		if len(self.data) == 0:
			return {'success': False, 'error': 'Image not found'}

		property_id = self.data[0]['property_Id']

		if not self.verifyOwnership(property_id, owner_id):
			return {'success': False, 'error': 'You do not own this property'}

		self.deleteById(image_id)
		return {'success': True}
