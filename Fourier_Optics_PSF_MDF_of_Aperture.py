"""
This is a Python 3 program doing basic Fourier Optics.

First we generate an aperture mask in an array, then we solve Fraunhofer 
diffraction equation numerically using Fourier transform. 
Last we plot PSF and MTF to evaluate results.

Usage: python Fourier_Optics_PSF_MDF_of_Aperture.py

Date: 2020-12-18

For tutorial & doc visit:
    https://www.erellaz.com 

Documentation:
 -tip 1: the support array needs to be much bigger than the mask to avoid
 artefacts in the Fourier tansform.
 -tip 2: read and understand fftflip doc, or the display won't make sense.
 -tip 3: with cv2, arrays needs to be normalized before saving to image, 
 otherwise you may end up with an all black image while the pyplot looks fine.
 -calculating PSF on pixels is easy. The somewhat tricky part is to correctly 
 assign physical units. This is a good read on the subject:
 https://www.strollswithmydog.com/wavefront-to-psf-to-mtf-physical-units/

Also check:
http://aberrator.astronomy.net/
"""
#______________________________________________________________________________
# User defined input parameters. You need to adjust only this.
imagesizepixels=(10000,10000) # must be much bigger than aperture to avoid artefects
diam_app_mm=250 # Your aperture in mm
diam_obs_mm=80 # Your central obstruction in mm
thickness_mm=2 # your vane thickness in mm
fn=20 # Your f/ number, a-dimentional.
la=656.28 # The monochormatic wavelength for which we do the calculation in nanometers

# The spatial scale is Q pixels per mm
Q=4 

#gamma corection for displays
gamma=.5

outputdir=r"D:\diffraction"
filetype=".jpg"

#______________________________________________________________________________
#import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

#______________________________________________________________________________
def normalize_to_min(ina):
    maxin=np.max(ina)
    minin=np.min(ina)
    nin=(ina-minin)*255/(maxin-minin)
    return nin

def normalize_to_zero(ina):
    maxin=np.amax(ina)
    nin=np.abs(ina)*255/maxin
    return nin

def normalize_to_0_1(ina):
    maxin=np.max(ina)
    minin=np.min(ina)
    nin=(ina-minin)*1/(maxin-minin)
    return nin

def make_telescope_4_vanes(imagesizepixels,diam_app,diam_obs,thickness):
    im =np.zeros(imagesizepixels,np.float64)
    center_x=int(imagesizepixels[0]/2)
    center_y=int(imagesizepixels[1]/2)
    # Make aperture, very small in an ocean of black
    im=cv2.circle(im,(center_x,center_y), int(diam_app/2),255,-1)
    im=cv2.circle(im,(center_x,center_y), int(diam_obs/2),0,-1)
    im = cv2.line(im, (center_x,0), (center_x,imagesizepixels[1]),0, int(thickness))
    im = cv2.line(im, (0,center_y), (imagesizepixels[1],center_y), 0, int(thickness))    
    return im

#______________________________________________________________________________
diam_app=diam_app_mm*Q # Your aperture in pixels
diam_obs=diam_obs_mm*Q # Your central obstruction pixels
thickness=thickness_mm*Q # your vane thickness in pixels

center_x=int(imagesizepixels[0]/2)
center_y=int(imagesizepixels[1]/2)
#filenamein=os.path.join(outputdir,"Aperture_"+str(diam_app)+"_obstruction"+str(diam_obs)+filetype)
#filenamem=os.path.join(outputdir,"Diffaction_magnitude_for_aperture_"+str(diam_app)+"_obstruction"+str(diam_obs)+filetype)
#filenamea=os.path.join(outputdir,"Diffaction_amplitude_for_aperture_"+str(diam_app)+"_obstruction"+str(diam_obs)+filetype)
#filenamep=os.path.join(outputdir,"Diffaction_phase_for_aperture_"+str(diam_app)+"_obstruction"+str(diam_obs)+filetype)
#filenamei=os.path.join(outputdir,"Diffaction_intensity_for_aperture_"+str(diam_app)+"_obstruction"+str(diam_obs)+filetype)


im=make_telescope_4_vanes(imagesizepixels,diam_app,diam_obs,thickness)

f = np.fft.fft2(im)
fshift = np.fft.fftshift(f)

# The amplitude
amp=(np.abs(fshift))
#namp=normalize_to_zero(amp)

# The Intensity
intens=np.square(amp)
#nintens=normalize_to_zero(intens)

#The MTF
mtf=np.abs(np.fft.fftshift(np.fft.fft2(intens)))


#mag = 20*np.log(amp)
#nmag=normalize_to_min(mag)

#phase=(180+np.angle(fshift,1))*(255/180) #phase in degrees

# Prepare the aperture display
margin=int(diam_app/2+100) #space margin in pixels
#Zoom in the intersting part
im_zoom=im[center_x-margin:center_x+margin,center_y-margin:center_y+margin]


plt.rcParams["figure.figsize"] = (28,6)
plt.subplot(161)
plt.imshow(im_zoom, cmap = 'gray',extent=[0,(im_zoom.shape[0]/Q),0,(im_zoom.shape[1]/Q)])
plt.title('Input Aperture'), plt.xlabel('in mm')
#plt.show()

#plt.subplot(152),plt.imshow(amp, cmap = 'gray')
#plt.title('Amplitude Spectrum'), plt.xticks([]), plt.yticks([])
#
#plt.subplot(153),plt.imshow(nmag, cmap = 'gray')
#plt.title('Magnitude Spectrum, (ie- log scale)'), plt.xticks([]), plt.yticks([])
#
#plt.subplot(154),plt.imshow(phase, cmap = 'gray')
#plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])
#
#plt.subplot(155),plt.imshow(intens, cmap = 'gray')
#plt.title('PSF'), plt.xticks([]), plt.yticks([])




#______________________________________________________________________________
#PSF
zf=35
PSFscale=(la/1000)*fn*(Q/1000) # convert l from nano meters to microns and Q from pixel/mm to pixel/micron
intenszoom=intens[center_x-zf:center_x+zf,center_y-zf:center_y+zf]
#nintenszoom=normalize_to_zero(intenszoom)

#
plt.subplot(162)
#plt.rcParams["figure.figsize"] = (6,6)
extPSF=(im_zoom.shape[0]*PSFscale)/2
plt.imshow(intenszoom, cmap = 'gray',extent=[-extPSF,extPSF,-extPSF,extPSF])
plt.title('PSF'), plt.xlabel('in microns')
#plt.show()

plt.subplot(163)
#plt.rcParams["figure.figsize"] = (6,6)
extPSF=(im_zoom.shape[0]*PSFscale)/2
plt.imshow(normalize_to_min(np.power(normalize_to_0_1(intenszoom),gamma)), cmap = 'gray',extent=[-extPSF,extPSF,-extPSF,extPSF])
plt.title('Gamma corrected PSF'), plt.xlabel('in microns')
#plt.show()

#
plt.subplot(164)
#plt.rcParams["figure.figsize"] = (6,6)
xx=np.linspace(-extPSF,extPSF, num=intenszoom.shape[1])
plt.plot(xx,intenszoom[zf,:])
plt.title('PSF sliced along x'), plt.xlabel('in microns')
#plt.show()

#______________________________________________________________________________
#MTF
zf=600

mtfscale=1000*(la/1000)*(Q/1000)/fn # convert l from nano meters to microns and Q from pixel/mm to pixel/micron
mtfzoom=mtf[center_x-zf:center_x+zf,center_y-zf:center_y+zf]
extMTF=int((im_zoom.shape[0]*mtfscale)/2)

plt.subplot(165)
#plt.rcParams["figure.figsize"] = (6,6)
plt.imshow(mtfzoom, cmap = 'gray',extent=[-extMTF,extMTF,-extMTF,extMTF])
plt.rcParams["figure.figsize"] = (6,6)
plt.title('MTF'), plt.xlabel('in lp/mm')
#plt.show()

plt.subplot(166)
#plt.rcParams["figure.figsize"] = (6,6)
#xx=np.linspace(-extMTF,extMTF, num=mtfzoom.shape[1])
mtfpos=mtfzoom[zf,zf:]
xx=np.linspace(0,extMTF, num=mtfpos.shape[0])
plt.plot(xx,mtfpos)
plt.title('MTF sliced along x'), plt.xlabel('in lp/mm')
plt.show()
#______________________________________________________________________________

print("Airy disk radius calculated through 1.22 lambda f/ =",1.22*(la/1000)*fn, " microns")
#
#
#
#cv2.imwrite(filenamein, im)
#cv2.imwrite(filenamea, namp)
#cv2.imwrite(filenamem, nmag)
#cv2.imwrite(filenamep, phase)
#cv2.imwrite(filenamei, nintenszoom)
#
