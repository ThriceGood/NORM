

class TypeParent(object):
	attrs = ['value', 'allow_null', 'primary_key', 'unique']
	def __init__(self, Type, **kwargs):
		for k, v in kwargs.items():
			if k in TypeParent.attrs:
				self.__setattr__(k, v)
			elif k in Type.attrs:
				Type.__setattr__(k, v)
			else:
				raise AttributeError(
					'{} is not an attribute of {}'.format(
						k, Type.__class__.__name__))


class TextType(TypeParent):
	def __init__(self, **kwargs):
		self.attrs = []
		parent = super(TextType, self)
		parent.__init__(self, **kwargs)
		self.type = 'TEXT'


class IntegerType(TypeParent):
	def __init__(self, **kwargs):
		self.attrs = ['auto_increment']
		parent = super(IntegerType, self)
		parent.__init__(self, **kwargs)
		self.type = 'INTEGER'
