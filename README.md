# Fourier_Optic
Python scripts doing Fourier optics

First we generate an aperture mask in an array to reprsent the aperture of a telescope or lens, then we solve Fraunhofer 
diffraction equation numerically using Fourier transform, at a given wavelength, at focus,  for that aperture.

Last we plot PSF (raw, gamma corrected to see the Iry disk better and in 2D slice) and MTF (3D and 2D slice) to evaluate the results.

Usage: python Fourier_Optics_PSF_MDF_of_Aperture.py

Some useful tips:
 -tip 1: the support array needs to be much bigger than the mask to avoid
 artefacts in the Fourier tansform.
 -tip 2: if new to fft in python, read and understand fftflip doc.
 -tip 3: with cv2, arrays needs to be normalized before saving to image, 
 otherwise you may end up with an all black image while the pyplot looks fine.
 -calculating PSF on pixels is easy. The somewhat tricky part is to correctly 
 assign physical units. This is a good read on the subject:
 https://www.strollswithmydog.com/wavefront-to-psf-to-mtf-physical-units/

Also check:
http://aberrator.astronomy.net/

More at: 
  https://erellaz.com/
  
![Script Output](Fourier_optic.png)
