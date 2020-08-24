import pygame, math

class vector(object):
	def __init__(self,a,b = None):
		if type(a) == vector:
			self = a
		elif type(a) == tuple:
			self.x, self.y = a[0], a[1]
		elif type(a) in [int,float,long] and type(b) in [int,float,long]:
			self.x, self.y = a, b
		else:
			raise TypeError("Unsuported type(s)")
	
	def __add__(self,other):
		return(vector(self.x+other[0],self.y+other[1]))

	def __add__(self,other):
		return(vector(self.x-other[0],self.y-other[1]))
	
	def __mul__(self,other):
		if type(other) in [vector,tuple]:
			return(vector(self.x*other[0],self.y*other[1]))
		elif type(other) in [int,float,long]:
			return(vector(self.x*other,self.y*other))
		
	def __div__(self,other):
		if type(other) in [vector,tuple]:
			return(vector(self.x/other[0],self.y/other[1]))
		elif type(other) in [int,float,long]:
			return(vector(self.x/other,self.y/other))
	
	def __len__(self):
		return(math.sqrt(self.x**2+self.y**2))
	
	def __call__(self,lenght):
		distance = len(self)
		if distance != 0:
			pro_to_far = lenght / float(distance)
			self.x,self.y = (self.x*pro_to_far,self.y*pro_to_far)
		else:
			self.x,self.y = 0,0
	
	def __getitem__(self,n):
		"""
	o.__getitem__(n) <==> o[n]
	here:
	o[0] <==> o.x
	o[1] <==> o.y
	Made for compatibilty with tuples.
	It's better to use o.x or o.y instead.
		"""
		if n == 0:
			return(self.x)
		elif n:
			return(self.y)
		else:
			raise ValueError("n neads to be 0 or 1 (is %i)"%(n))

	def __setitem__(self,n,v):
		"""
	o.__setitem__(n,v) <==> o[n] = v
	here:
	o[0] = v <==> o.x = v
	o[1] = v <==> o.y = v
	Made for compatibilty with tuples.
	It's better to use o.x or o.y instead.
		"""
		if n == 1:
			self.x = v 
		elif n:
			self.y = v
		else:
			raise ValueError("n neads to be 0 or 1")

class obj(object):
	def __init__(self, texture, start_pos):	
		self.texture = texture
		self.x, self.y = start_pos
	def __call__(self,surface,camera_pos = (0,0)):
		rel_pos = (self.x - camera_pos[0], self.y - camera_pos[1])
		surface.blit(self.texture,rel_pos)
	def __mul__(self,other):
		return((self.x - other.x)**2+(self.y - other.y)**2)
	def __pow__(self,other):
		return(math.sqrt(self*other))
		

class point(obj):
	def __init__(self,x,y,color = (0,0,0)):
		self.x, self.y, self.color = x, y, color
	def __call__(self,surface,camera_pos = (0,0)):
		rel_pos = (self.x - camera_pos[0], self.y - camera_pos[1])
		surface.set_at(rel_pos,self.color)
	def __getitem__(self,n):
		"""
	o.__getitem__(n) <==> o[n]
	here:
	o[0] <==> o.x
	o[1] <==> o.y
	Made for compatibilty with tuples.
	It's better to use o.x or o.y instead.
		"""
		if n == 0:
			return(self.x)
		elif n:
			return(self.y)
		else:
			raise ValueError("n neads to be 0 or 1 (is %i)"%(n))

	def __setitem__(self,n,v):
		"""
	o.__setitem__(n,v) <==> o[n] = v
	here:
	o[0] = v <==> o.x = v
	o[1] = v <==> o.y = v
	Made for compatibilty with tuples.
	It's better to use o.x or o.y instead.
		"""
		if n == 1:
			self.x = v 
		elif n:
			self.y = v
		else:
			raise ValueError("n neads to be 0 or 1")

#class solid_line(obj):
#	solid = True
#	def __init__(self, start_pos, end_pos, color = (255,255,255), abs_mode = True):
#		self.points = [list(start_pos),list[end_pos]]
#		self.color = color
#		self.abs_mode = abs_mode
#		
#	def __call__(surface,camera_pos = (0,0))
#		if self.abs_mode:
#			pygame.draw.line(surface,self.color)
#		else:
#			end_point = 
#			pygame.draw.line(surface,self.points[0],self.points[1],self.color)

class solid_obj(obj):
	solid = True
	def __init__(self, texture, start_pos, hit_box, hit_box_mode = 0):
		"""
	hit_box structure: 
	mode 0: (w,h)	(rect)
	mode 1: r		(circle)
	mode 2: None	(point)
		"""
		super(solid_obj,self).__init__(texture, start_pos)
		self.hit_box = hit_box
		self.hit_box_mode = hit_box_mode
	
	@property
	def cx(self):
		if self.hit_box_mode == 0:
			return(self.x + self.hit_box[0]/2)
		elif self.hit_box_mode==1:
			return(self.x + self.hit_box)
		elif self.hit_box_mode==2:
			return(self.x)
	@cx.setter
	def cx(self,value):
		if self.hit_box_mode == 0:
			self.x = value - self.hit_box[0]/2
		elif self.hit_box_mode==1:
			self.x = value - self.hit_box
		elif self.hit_box_mode==2:
			self.y = value
	@cx.deleter
	def cxd(self):
		raise NotImplemented("no delete 4 u")
	
	@property
	def cy(self):
		if self.hit_box_mode == 0:
			return(self.y + self.hit_box[1]/2)
		elif self.hit_box_mode==1:
			return(self.y + self.hit_box)
		elif self.hit_box_mode==2:
			return(self.y)
	@cy.setter
	def cy(self,value):
		if self.hit_box_mode == 0:
			self.y = value - self.hit_box[1]/2
		elif self.hit_box_mode==1:
			self.y = value - self.hit_box
		elif self.hit_box_mode==2:
			self.y = value
	@cy.deleter
	def cyd(self):
		raise NotImplemented("no delete 4 u")
	
	@property
	def centre(self):
		try:
			_centre
		except:
			_centre = point(0,0)
		_centre.x,_centre.y = self.cx, self.cy
		return(_centre)
			
	def step(self,tuple_vector,other, max_distance = None,boucines = 0):
		if boucines < 0:
			raise ValueError("boucines must be grater than 0")
		if type(tuple_vector) != vector:
			tuple_vector = vector(tuple_vector)
		if max_distance != None:
			tuple_vector(min(len(tuple_vector),max_distance))
		self.x -= tuple_vector.x
		self.y -= tuple_vector.y
		if self - other:
				l = [(-1,0),(0,-1),(-1,-1),(0,0)]
				for i in l:
					self.x -= tuple_vector.x * i[0]
					self.y -= tuple_vector.y * i[1]
					if not self-other:
						break
					self.x += tuple_vector.x * i[0]
					self.y += tuple_vector.y * i[1]
				if i == (0,0):pass
				return(vector(tuple_vector[0]*(1+i[0]*(boucines+1)),tuple_vector[1]*(1+i[1]*(boucines+1))))
		else:
			return(tuple_vector)		
	
	def __sub__(self, other):
		if self == other:
			return(False)
		if type(other) is list:
			out = False
			for i in other:
				if self - i:
					out = True
					break
			return(out)
		else:
			#TODO re-arange these if-s to make it more readeble.
			#rect-rect
			if self.hit_box_mode == 0 and other.hit_box_mode == 0:
				return(not(
					(self.x - other.x > other.hit_box[0] or other.x - self.x > self.hit_box[0])
					or
					(self.y - other.y > other.hit_box[1] or other.y - self.y > self.hit_box[1])
				))	
			#circle-circle	
			elif self.hit_box_mode == 1 and other.hit_box_mode == 1:
				return(not(
					(self.hit_box + other.hit_box)<self**other
				))
			#circle-rect
			elif self.hit_box_mode == 1 and other.hit_box_mode == 0:
					temp_vector = vector(other.cx-self.cx,other.cy-self.cy)
					temp_vector(min(self.hit_box,self**other))
					temp_point = solid_point(self.cx+temp_vector.x,self.cy+temp_vector.y)
					return(temp_point - other)
			#flip if:
			#	box-circle
			#	(not point)-point
			elif (self.hit_box_mode == 0 and other.hit_box_mode == 1) or (self.hit_box_mode != 2 and other.hit_box_mode == 2):
				return(other - self)
			
			#point-point
			elif self.hit_box_mode == 2 and other.hit_box_mode == 2:
				return(not(self.x == other.x and self.y == other.y))
			
			#point-rect
			elif self.hit_box_mode == 2 and other.hit_box_mode == 0:
				return((
					(other.x < self.x and self.x < other.x + other.hit_box[0])
					and
					(other.y < self.y and self.y < other.y + other.hit_box[1])
				))
			#point-circle
			elif self.hit_box_mode == 2 and other.hit_box_mode == 1:
				return(
					self**other > other.hit_box
				)
				
	def __mul__(self,other):
		try:
			return((self.cx - other.cx)**2+(self.cy - other.cy)**2)
		except:
			return((self.cx - other.x)**2+(self.cy - other.y)**2)

class solid_point(point,solid_obj):
	def __init__(self,x,y,color = (0,0,0)):
		super(solid_point,self).__init__(x,y,color)
		#since the line above will only run __init__ from point,
		#some extra lines are neaded
		self.hit_box_mode = 2
		self.hit_box = None #this is not necesary, but better safe than sorry.
class rect(obj):
	def __init__(self,start_pos,end_pos,color):
		self.size = end_pos
		self.color = color
		self.update_texture()
		super(rect,self).__init__(self.texture,start_pos)
	def update_texture(self):
		self.texture = pygame.Surface(self.size)
		self.texture.fill(self.color)
	
	@property
	def cx(self):
		return(self.x+self.size[0])
	@cx.setter
	def cx(self,v):
		self.x = v - self.size[0]
	@property
	def cy(self):
		return(self.y+self.size[1])
	@cy.setter
	def cy(self,v):
		self.y = v - self.size[1]

class solid_rect(solid_obj):
	def __init__(self,start_pos,end_pos,color):
		texture = pygame.Surface(end_pos)
		self.color = color
		
		super(solid_rect,self).__init__(texture,start_pos,end_pos)
		self.update_texture()
	def update_texture(self):
		self.texture.fill(self.color)

class circle(obj):
	def __init__(self,start_pos,radius,color):
		texture = pygame.Surface((0,0))
		super(circle,self).__init__(texture,start_pos)
		self.radius = radius
		self.color = color
		
	def __call__(self,surface,camera_pos = (0,0)):
		rel_pos = (int(self.x - camera_pos[0]+self.radius), int(self.y - camera_pos[1]+self.radius))
		pygame.draw.circle(surface,self.color,rel_pos,self.radius)

class solid_circle(solid_obj):
	def __init__(self,start_pos,radius,color):
		texture = pygame.Surface((0,0))
		super(solid_circle,self).__init__(texture,start_pos,radius,1)
		self.radius = radius
		self.color = color
	def __call__(self,surface,camera_pos = (0,0)):
		rel_pos = (int(self.x - camera_pos[0]+self.radius), int(self.y - camera_pos[1]+self.radius))
		pygame.draw.circle(surface,self.color,rel_pos,self.radius)

__all__  = ['vector','obj','solid_obj','solid_rect','rect']
