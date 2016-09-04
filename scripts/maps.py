import urllib
import time
import os
import math

class maps():
	zoom = 0
	size = 0
	delta = 0.0
	INT = 10
	CDEL = 0.013333
	DIR = ''
	surl = 'http://maps.googleapis.com/maps/api/staticmap?center='
	t = '&zoom='
	s = '&size='
	u = '&sensor=false'
	tsurl1 = 'http://mt0.google.com/vt/lyrs='
	tsurl2 = '@110&hl=en&x='
	teurl = '&z=17&s='
	tmurl = '&s=&y='

	def __init__(self):
		#self.zoom = z
		#self.size = s
		#diff = - self.zoom + 16
		#self.delta = self.CDEL*(2**diff)
		#self.t = self.t + str(self.zoom)
		#self.s = self.s + str(self.size) + 'x' +str(self.size)
		#self.DIR = d + '/'
		#self.teurl = '&z=' + str( self.zoom ) + '&s='
		#os.system('mkdir ' + self.DIR)
		self.base = ''
		

	def getblock(self,latmin,latmax,lonmin,lonmax):
		eurl = self.t + self.s + self.u
		lat = lon = 0
		lat = latmin
		f = open('trash.png','r')
		trimg = f.read()
		f.close()
		while lat <= latmax:
			lon = lonmin
			while lon <= lonmax:
				url = self.surl + str(lat) + ',' + str(lon) + eurl
				print url
				block = self.download(url)
				while block == trimg:
					time.sleep(24*self.INT)
					block = self.download(url)
				f = open(self.DIR + str(lat)+'_'+str(lon)+'.png','w')
				f.write(block)
				f.close()
				time.sleep(self.INT)
				lon = lon + self.delta
			lat = lat + self.delta
		
	def download(self,url):
		blk = 'crap'
		while blk == 'crap':
			try:
				gmap = urllib.urlopen(url)
				blk = gmap.read()
				return blk
			except:
				blk = 'crap'

	def getmap(self,lat,lon):
		eurl = self.t + self.s + self.u
		url = self.surl + str(lat)+','+str(lon)+eurl
		block = self.download(url)
		f = open('trash.png','r')
		trimg = f.read()
		f.close()
		while block == trimg:
			time.sleep(24*self.INT)
			block = self.download(url)
		f = open(self.DIR + str(lat)+'_'+str(lon)+'.png','w')
		f.write(block)
		f.close()
		time.sleep(10)

	def _gettile( self, x, y, t, d ):
		if t == 'm':
			turl = self.tsurl1 + t + self.tsurl2
			url = turl + str(x) + self.tmurl + str(y) + self.teurl
			ofile = str(y)+'.png'
		if t == 's':
			turl = self.tsurl1 + t + self.tsurl2
			url = turl + str(x) + self.tmurl + str(y) + self.teurl
			ofile = str(y)+'.jpeg'
		page = urllib.urlopen(url)
		data = page.read()
		while data.find('HTML') != -1:
			page = urllib.urlopen(url)
			data = page.read()
		print url
		f = open(d+ofile,'w')
		f.write(data)
		f.close()

	def xyfromlatlon_( self, lat_deg, lon_deg, zoom):
		lat_rad = math.radians(lat_deg)
		n = 2.0 ** zoom
		xtile = ((lon_deg + 180.0) / 360.0 * n)
		ytile = ( ( 1.0-math.log( math.tan( lat_rad )+( 1/math.cos(lat_rad)))/math.pi)/2.0*n)
		return ( xtile, ytile )
	
	def latlonfromxy( self, x, y, zoom ):
		n = 2**zoom
		lon_deg = x/(n+0.0)*360.0 - 180.0
		lat_rad = math.atan( math.sinh( math.pi*( 1.0-(2.0*y)/n ) ) )
		lat_deg = math.degrees( lat_rad )
		return ( lat_deg, lon_deg )

	def xyfromlatlon( self, lat, lon, zoom ):
		tile = self.xyfromlatlon_( lat, lon, zoom )
		return ( int( tile[ 0 ] ), int( tile[ 1 ] ) )

	def setzoom( self, z ):
		self.zoom = z
		self.teurl = '&z=' + str( self.zoom ) + '&s='

	def setbase( self, base ):
		self.base = base
		self.satdir = base + '/' + 'sats'
		self.mapdir = base + '/' + 'maps'
		if not os.path.exists( self.base ):
			os.mkdir( self.base )
		if not os.path.exists( self.satdir ):
			os.mkdir( self.satdir )
		if not os.path.exists( self.mapdir ):
			os.mkdir( self.mapdir )
	
	def gettile( self, x, y, t ):
		if t == 's':
			if not os.path.exists( self.satdir + '/' +str( self.zoom ) ):
				os.mkdir( self.satdir + '/' + str( self.zoom ) )
			path = self.satdir + '/' +  str(self.zoom) + '/' + str(x) + '/'
		else:
			if t == 'm':
				if not os.path.exists( self.mapdir + '/' +str( self.zoom ) ):
					os.mkdir( self.mapdir + '/' + str( self.zoom ) )
				path = self.mapdir + '/' + str(self.zoom) + '/'  + str(x) + '/'
		if os.path.exists(path):
			self._gettile( x, y, t, path )
		else:
			try:
				os.mkdir( path )
			except:
				pass
			self._gettile( x, y, t, path )
		

	def gettile_( self, x, y, t):
		if t == 's':
			path = self.satdir + '/'+ str(self.zoom)+'/'+str(x)+'/'+str(y)+'.jpeg'
		if t == 'm':
			path = self.mapdir + '/'+ str(self.zoom)+'/'+str(x)+'/'+str(y)+'.png'
		if os.path.exists( path ):
			return False
		else:
			self.gettile(x, y, t)
			return True

	def readGPS( self, log ):
		flog = open( log, 'r' )
		lines = flog.readlines()
		gpsData = []

		for line in lines:
			if line.find( '<gx:coord>' ) != -1:
				tmp = line[ 10:len(line) - 12 ].split( ' ' )
				coords = [ float( tmp[0] ), float( tmp[1] ),\
						  float( tmp[2] ) ]
				gpsData.append( coords )
				
		return gpsData

	def getTilesFromGPS( self, log, zoom, t ):
		coords = self.readGPS( log )
		for xyz in coords:
			( x, y ) = self.xyfromlatlon( xyz[1], xyz[0], zoom )
			self.gettile_( x, y, t )
