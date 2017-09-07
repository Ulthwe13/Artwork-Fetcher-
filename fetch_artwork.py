#!/usr/bin/python
# Fetch album art for the given artist from metal-archives.com and saves to current album folder
import os
from mutagen.id3 import ID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.aac import AAC
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.mp4 import MP4MetadataError
import musicbrainzngs


musicbrainzngs.set_useragent("Artwork Fetcher App", "0.1", "")
root_dir = "<full path to music dir>"

def check_for_cover(album_dir):
	has_cover = False

	for file in os.listdir(album_dir + '/'):
		if ".jpg" in file or ".png" in  file:
			has_cover = True
			break

	return has_cover

def get_cover(artist, album):
	result = musicbrainzngs.search_releases(artist=artist, release=album, limit=10)

	if not result['release-list']:
		return False

	for idx, release in enumerate(result['release-list']):
		try:
			data = musicbrainzngs.get_image_front(release['id'], size=None)
			print "[+] Artwork Saved!"
			fh = open(root+"/cover.jpg", "w")
			fh.write(data)
			fh.flush()
			fh.close()
			break
		except Exception, HTTPError:
			continue
	return True 

def getMP3Tags(filename):

	try:
		audio = ID3(filename)

		if 'TPE1' in  audio and 'TALB' in audio:
			artist = audio['TPE1'].text[0]
			album = audio['TALB'].text[0]
			print "[*] Searching for artwork for " + artist + " - " + album
			return get_cover(artist, album)
		else:
			return False
	except ID3NoHeaderError:
		print "[!] No Tags found for " + filename
	
	manualSearch()

def getMP4Tags(filename):
	try:
		audio = MP4(filename)
		
		if '\xa9ART' in audio and '\xa9alb' in audio:
			artist  = audio['\xa9ART'][0]
			album = audio['\xa9alb'][0]
			print "\n[*] Searching for artwork for " + artist +	" - " + album 
			return get_cover(artist, album)
		else:
			return False
	except KeyError:
		print "[!] No Tags found for " + filename
	
	manualSearch()


def getFLACTags(filename):
	try:
		audio = FLAC(filename)
		print audio['artist']
		if 'artist' in audio and 'album' in audio:
			artist = audio['artist']
			album = audio['album']
			print "\n[*] Search for artwork for " + str(artist) + " - " + str(album)
			return get_cover(artist, album)
		else:
			return False
	except KeyError:
		print "[!] No Tags found for " + filename
	
	manualSearch()


def manualSearch():
	print "[-] Would you like to manually enter artist & album to search? [y/n]"
	
	choice = str(raw_input().strip())
	if choice != 'y':
		print "[!] Skipping: " + root
		return False
	else:
		print "Enter Album Name:"
		album = str(raw_input().strip())
		print "Enter Artist Name:"
		artist = str(raw_input().strip())
		print "Searching for: " + artist + " - " + album
		return get_cover(artist, album)


for root, folders, files in os.walk(root_dir):
	for filename in files:
		if check_for_cover(root) is True:
			break
		else:
			if filename.endswith('.mp3'):
				getMP3Tags(root+'/'+filename)
				break
			elif filename.endswith('.m4a'):
				getMP4Tags(root+'/'+filename)
				break
			elif filename.endswith('.flac'):
				getFLACTags(root+'/'+filename)
			else:
				print "[!] Unrecognized File Type for " + root + '/' + filename
				break
