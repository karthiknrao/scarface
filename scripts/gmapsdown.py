#! /usr/bin/python

from maps import *
import os
import glob
import sys

def downmaps():
	if len( sys.argv ) < 3:
		sys.exit(0)
	zoom = int( sys.argv[ 3 ] )
	c_lat = float( sys.argv[ 1 ] )
	c_lon = float ( sys.argv[ 2 ] )
	typ = sys.argv[ 4 ]
	delt = int(sys.argv[ 5 ])
	gmaps = maps( )
	lat1 = c_lat - delt
	lon1 = c_lon 
	lat2 = c_lat 
	lon2 = c_lon + delt
	print zoom
	#( xmin, ymax ) = gmaps.xyfromlatlon( c_lat-.5, c_lon-.5, zoom )
	#( xmax, ymin ) = gmaps.xyfromlatlon( c_lat+.5, c_lon+.5, zoom )
	gmaps.setzoom( zoom )
	gmaps.setbase( '/Users/karthikrao/Downloads/maps' )
	( xmin, ymax ) = gmaps.xyfromlatlon( lat1, lon1, zoom )
	( xmax, ymin ) = gmaps.xyfromlatlon( lat2, lon2, zoom )
	#print xmin,ymin
	#print xmax,ymax
	#i = 23417
	tot = ( xmax - xmin )*( ymax - ymin )
	print tot
	i = xmin
	while i <= xmax:
		j = ymin
		while j <= ymax:
			#gmaps.gettile( i, j ,'m', 'maps/map4/' )
			if gmaps.gettile_( i, j, typ ):
				print str((i-xmin)*(ymax - ymin) + j-ymin) + '/' + str(tot)
			j = j + 1
		i = i + 1

downmaps()
