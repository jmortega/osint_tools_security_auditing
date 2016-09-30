# -*- encoding: utf-8 -*-

import PIL.ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
from pyexiv2 import ImageMetadata, ExifTag #python 2.7

from collections import namedtuple
import os

Header= namedtuple('Header',
    "profile_size,cmm_type,version,device_class,colour_space,"
    "PCS,date_time,signature,sig_platform,flags,dev_manufacturer,"
    "dev_model,dev_attributes,intent,illuminant,sig_creator,"
    "id"
    )

def icc_profile( icc_bytes ):
    """Decode the icc_bytes to create a Header object."""
    header = Header( *struct.unpack( ">IIIIII12s4s4sIII8sI12s4s16s28x", icc_bytes[:128]) )
    print( " Header:", header )
    tag_count= struct.unpack( ">I", icc_bytes[128:128+4] )[0]
    for tn in range(tag_count):
        offset= 128+4+12*tn
        sig, data_offset, data_size = struct.unpack( ">4sII", icc_bytes[offset:offset+12] )
        data= icc_bytes[data_offset:data_offset+data_size]
        print( "Tag", tn, sig, data[:4], data[4:8], data[8:] )
    return header

def decode_gps_info(exif):
    gpsinfo = {}
    if 'GPSInfo' in exif:
        '''
        Raw Geo-references
        for key in exif['GPSInfo'].keys():
            decode = GPSTAGS.get(key,key)
            gpsinfo[decode] = exif['GPSInfo'][key]
        exif['GPSInfo'] = gpsinfo
        '''
        
        #Parse geo references.
        Nsec = exif['GPSInfo'][2][2][0] / float(exif['GPSInfo'][2][2][1])
        Nmin = exif['GPSInfo'][2][1][0] / float(exif['GPSInfo'][2][1][1])
        Ndeg = exif['GPSInfo'][2][0][0] / float(exif['GPSInfo'][2][0][1])
        Wsec = exif['GPSInfo'][4][2][0] / float(exif['GPSInfo'][4][2][1])
        Wmin = exif['GPSInfo'][4][1][0] / float(exif['GPSInfo'][4][1][1])
        Wdeg = exif['GPSInfo'][4][0][0] / float(exif['GPSInfo'][4][0][1])
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][1] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat" : Lat, "Lng" : Lng}

 
def get_exif_metadata(image_path):
    ret = {}
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    decode_gps_info(ret)
    return ret

def get_exif_metadata2(image_path):
    img = Image.open(image_path)
    for key in img.info:
        if key == 'exif':
            for k,v in img._getexif().items():
                if k == 34853: # GPSInfo
                    print( PIL.ExifTags.TAGS[k], v )
                    for gk, gv in v.items():
                        print(PIL.ExifTags.GPSTAGS[gk], gv )
        elif key == 'icc_profile':
            print( key, )
            icc_profile( img.info[key] )
            
def get_exif_metadata3(image_path):
    metadata = ImageMetadata(image_path)
    metadata.read()
    for item in metadata.exif_keys:
	    tag = metadata[item]
	    print(tag)
	    f = open("Exifinfo.txt","w")
	    f.write(str(tag) + "\n")         
 
 

def printMeta():
    for dirpath, dirnames, files in os.walk("images"):
        for name in files:
            print("[+] Metadata for file: %s " %(dirpath+os.path.sep+name))
            try:
                exifData = {}
                exif = get_exif_metadata(dirpath+os.path.sep+name)
                for metadata in exif:
                    print("Metadata: %s - Value: %s " %(metadata, exif[metadata]))
                print("\n")
                get_exif_metadata3(dirpath+os.path.sep+name)
            except:
                import sys, traceback
                traceback.print_exc(file=sys.stdout)
printMeta()


