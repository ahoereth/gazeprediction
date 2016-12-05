% Gaussian Mixture Models
% Alexander Höreth and Sebastian Höffner
% December 03, 2016

---
navigation: empty
theme: CambridgeUS
colortheme: beaver
header-includes:
  - \usepackage[all]{nowidow}
---

# Background Subtraction
## Background Subtraction
* surveillance monitoring
* motion detection
* image segmentation

Primarily used for preprocessing!

e.g.

1. remove background
2. detect moving objects
3. identify individual humans


## Mixture of Gaussians
* consider an image as a distribution over its pixel's values
* estimate it using a mixture of three to five Gaussians
* use expectation maximization (expensive) or k-means to make the Gaussians mixture model better fit the image

* sort by weights by variance ($\omega/\sigma$)
* first few distributions are declared as background
* pixels belonging to these can be declared as background pixels, others are foreground

@stauffer99, specifically page 4


# Improving Background Subtraction
## Improving Background Subtraction
* *Improved Adaptive Background Mixture Model* (MOG) by @ktkp01
* *Improved Adaptive Gaussian Mixture Model* (MOG2) by @zivkovic04


## Improved Adaptive Background Mixture Model (MOG)
* add more Gaussians if pixels are $2.5$ standard deviations away from all current distributions
    - allows the model to adapt to changes quicker
    - predict fore/background affiliation faster
* use *expectation maximization* instead of k-means
    - k-means was basically an approximation of EM
    - EM got computational feasible
* detect shadows
    - combination of background and foreground features
* more precise than original algorithm

@ktkp01


## Improved Adaptive Gaussian Mixture Model (MOG2)
* dynamically add and remove Gaussians:
    - pixels are considered to be not represented by model if more than $3$ standard deviations away from all Gaussians
    - if useful, remove Gaussian with lowers probability and add a new one for the not represented pixels
    - cap Gaussian count at 5
* introduce *balloon estimator* as alternative to k-means
    - again approximates EM
* also detects shadows
* faster than original algorithm

@zivkovic04, @zivkovic06


# Comparison
## OpenCV & cvloop
Using OpenCV's implementations: `MOG`[^linkmog], `MOG2`[^linkmog2]

Custom `cvloop`[^cvlooplink] package for manipulating videos streams, both from file and webcam. Available through PyPI: *`pip install cvloop`*

\vfill

Visualizing the mask for a real time webcam stream:

```python
import cv2
from cvloop import cvloop
def mog2(frame):
    return mog2.fgbg.apply(frame)
mog2.fgbg = cv2.createBackgroundSubtractorMOG2()
cvloop(function=mog2)
```

## Note: Shadows

While both algorithms are capable of extracting shadows, OpenCV only implements this for MOG2.

![MOG2 applied to `768x576.avi`[^linkopencv] [@opencv] with and without shadows. White denotes foreground, gray shadows and black background.](768x576_comp_fg_shadow_f100.png){width=70%}


## Application I

---------------------------------------------------------------------------------------------
Original Frame                 MOG Mask                       MOG2 Mask
------------------------------ ------------------------------ -------------------------------
![](768x576_original_f100.png) ![](768x576_mask_mog_f100.png) ![](768x576_mask_mog2_f100.png)
---------------------------------------------------------------------------------------------

Table: Frame 100 from video `768x576.avi`.


## Application II

---------------------------------------------------------------------------------------------------
Original Frame                   MOG Mask                         MOG2 Mask
-------------------------------- -------------------------------- ---------------------------------
![](1920x1080_original_f100.png) ![](1920x1080_mask_mog_f100.png) ![](1920x1080_mask_mog2_f100.png)
---------------------------------------------------------------------------------------------------

Table: Frame 100 from video `1920x1080.avi`[^linkopencv] [@opencv].


## Application III

---------------------------------------------------------------------------------------------------------------------------
Original Frame                           MOG Mask                                 MOG2 Mask
---------------------------------------- ---------------------------------------- -----------------------------------------
![](AVSS_AB_Easy_Divx_original_f500.png) ![](AVSS_AB_Easy_Divx_mask_mog_f500.png) ![](AVSS_AB_Easy_Divx_mask_mog2_f500.png)
---------------------------------------------------------------------------------------------------------------------------

Table: Frame 500 from video `AVSS_AB_Easy_Divx.avi`[^linkavss] [@avss07].


## Application IV

---------------------------------------------------------------------------------------------------------------------------
Original Frame                           MOG Mask                                 MOG2 Mask
---------------------------------------- ---------------------------------------- -----------------------------------------
![](AVSS_PV_Hard_Divx_original_f500.png) ![](AVSS_PV_Hard_Divx_mask_mog_f500.png) ![](AVSS_PV_Hard_Divx_mask_mog2_f500.png)
---------------------------------------------------------------------------------------------------------------------------

Table: Frame 500 from video `AVSS_AB_Hard_Divx.avi`.


## Application V

------------------------------------------------------------------------------------------------------------------------------
Original Frame                            MOG Mask                                  MOG2 Mask
----------------------------------------- ----------------------------------------- ------------------------------------------
![](AVSS_PV_Night_Divx_original_f500.png) ![](AVSS_PV_Night_Divx_mask_mog_f500.png) ![](AVSS_PV_Night_Divx_mask_mog2_f500.png)
------------------------------------------------------------------------------------------------------------------------------

Table: Frame 500 from video `AVSS_AB_Night_Divx.avi`.


## Summary

MOG2 generates more complete foreground masks but with overall more background noise than MOG.

![Cropped masks of video `768x576.avi`. MOG (left) has less noise than MOG2 (right). Pay attention to split person's legs.](768x576_comp_mask_f100.png){width=06giarch%}


## Foreground Extraction I

--------------------------------------------------------------------------------------------------------------------------
Original Frame                            MOG Foreground                          MOG2 Foreground
----------------------------------------- --------------------------------------- ----------------------------------------
![](768x576_original_f100.png)            ![](768x576_fg_mog_f100.png)            ![](768x576_fg_mog2_f100.png)
--------------------------------------------------------------------------------------------------------------------------

Table: Frame 100 from video `768x576.avi`.


## Foreground Extraction II

--------------------------------------------------------------------------------------------------------------------------
Original Frame                            MOG Foreground                          MOG2 Foreground
----------------------------------------- --------------------------------------- ----------------------------------------
![](1920x1080_original_f100.png)          ![](1920x1080_fg_mog_f100.png)          ![](1920x1080_fg_mog2_f100.png)
--------------------------------------------------------------------------------------------------------------------------

Table: Frame 100 from video `1920x1080.avi`.


## Foreground Extraction III

--------------------------------------------------------------------------------------------------------------------------
Original Frame                            MOG Foreground                          MOG2 Foreground
----------------------------------------- --------------------------------------- ----------------------------------------
![](AVSS_AB_Easy_Divx_original_f500.png)  ![](AVSS_AB_Easy_Divx_fg_mog_f500.png)  ![](AVSS_AB_Easy_Divx_fg_mog2_f500.png)
--------------------------------------------------------------------------------------------------------------------------

Table: Frame 500 from video `AVSS_AB_Easy_Divx.avi`.


## Foreground Extraction IV

--------------------------------------------------------------------------------------------------------------------------
Original Frame                            MOG Foreground                          MOG2 Foreground
----------------------------------------- --------------------------------------- ----------------------------------------
![](AVSS_PV_Hard_Divx_original_f500.png)  ![](AVSS_PV_Hard_Divx_fg_mog_f500.png)  ![](AVSS_PV_Hard_Divx_fg_mog2_f500.png)
--------------------------------------------------------------------------------------------------------------------------

Table: Frame 500 from video `AVSS_AB_Hard_Divx.avi`.


## Foreground Extraction V

--------------------------------------------------------------------------------------------------------------------------
Original Frame                            MOG Foreground                          MOG2 Foreground
----------------------------------------- --------------------------------------- ----------------------------------------
![](AVSS_PV_Night_Divx_original_f500.png) ![](AVSS_PV_Night_Divx_fg_mog_f500.png) ![](AVSS_PV_Night_Divx_fg_mog2_f500.png)
--------------------------------------------------------------------------------------------------------------------------

Table: Frame 500 from video `AVSS_AB_Night_Divx.avi`.


# Thank you for your attention!
## References {.allowframebreaks}

[^linkmog]: [github.com/opencv/opencv/blob/modules/cudabgsegm/src/mog.cpp](https://github.com/opencv/opencv/blob/modules/cudabgsegm/src/mog.cpp)

[^linkmog2]: [github.com/opencv/opencv/blob/modules/video/src/bgfg_gaussmix2.cpp](https://github.com/opencv/opencv/blob/modules/video/src/bgfg_gaussmix2.cpp)

[^cvlooplink]: [github.com/shoeffner/cvloop](https://github.com/shoeffner/cvloop)

[^linkopencv]: [github.com/opencv/opencv_extra/tree/7054d3f/testdata/cv/video](https://github.com/opencv/opencv_extra/tree/7054d3f5d957c8f4849aea34aa1dcbadf4207a38/testdata/cv/video)

[^linkavss]: [eecs.qmul.ac.uk/~andrea/avss2007_d.html](http://www.eecs.qmul.ac.uk/~andrea/avss2007_d.html)
