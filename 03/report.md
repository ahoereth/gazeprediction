% Background Subtraction using Gaussian Mixture
% Alexander Höreth and Sebastian Höffner
% December 03, 2016


# Introduction

The following report will introduce the concept of applying Gaussian mixtures for computer vision tasks. Specifically we will discuss two algorithms which prove quite successful in background subtraction and tracking of animated objects in scenes.

The foundation for background subtraction approaches through statistical models like the ones presented in this report is the predictable property of static components in video streams. In order to fulfill the requirement of static components of a scene to actually appear as such we will in the following only discuss the case of statically positioned cameras. By fitting a statistical model to a scene which fulfills this requirement it is possible to track animated objects like people or cars by detecting resulting inconsistencies with the model's prediction.

The big challenge in fulfilling this rather straight forward idea is to update the model appropriately over time in order to smoothly handle changes in the static parts of the scene itself (e.g. parked cars or moved chairs) or for example to general lighting conditions.


# Background Subtraction

Background subtraction is a common task in computer vision. It is important for several tasks, for example surveillance monitoring, motion detection, or image segmentation. In surveillance applications it could provide means to skip through parts where the scene is not changing, in motion detection it can provide real time feedback when something is moving through the image.

For many applications however it is only necessary to subtract the background such that the foreground can be used for further processing steps: after detecting humans it might follow to identify them, after segmenting a scene into its different actors the semantic meaning could be inferred. Essentially removing the background allows to focus on a specific task.

## Mixture of Gaussians

One common method for performing background subtraction is to calculate a mask which labels each pixel of an input image as being either foreground ($1$) or background ($0$). @stauffer99 proposed a novel method which uses a mixture of Gaussians as a model to estimate the probability of a pixel being part of the foreground or background. Before, especially in @wren97, only single Gaussians have been used.

In @stauffer99 three to five Gaussians are used (depending on available computational power) to model whether a pixel belongs to the foreground or background. In general this could be done with algorithms like Expectation Maximization (EM), but since that algorithm is costly @stauffer99 resorted to a variant of K-means. They match pixels to the appropriate distributions and re-estimate the distributions parameters. Then the distributions are sorted by their weights divided by their variance ($\omega/\sigma$), such that the background distributions are heuristically first [@stauffer99, p. 4]. Then the first few distributions are declared as the background (depending on how many distributions are involved, this is a fixed parameter) and all pixels belonging to them can be masked as such.


# Improving Background Subtraction

In the early 2000s, two improvements of @stauffer99 have been proposed. The first is the "Improved Adaptive Background Mixture Model" (MOG) by @ktkp01, the second is the "Improved Adaptive Gaussian Mixture Model" (MOG2) described by @zivkovic04 and detailed further by @zivkovic06. In the following we will explain the differences between these two algorithms and @stauffer99 as well as compare MOG and MOG2 in some applications.

## Improved Adaptive Background Mixture Model (MOG)

@ktkp01 make two major changes to @stauffer99's algorithm. First they allow for more than just three to five Gaussian distributions by introducing new distributions if a pixel is further than $2.5$ standard deviations away from all existing distributions. Second they apply the already proposed EM algorithm instead of K-means to determine each pixel's estimated source distribution. Additionally to these changes @ktkp01 also introduce the ability to detect shadows.

These changes solve two important problems @ktkp01 identified in @stauffer99. By allowing an adaptive number of Gaussian distributions and using the EM algorithm they can predict background or foreground affiliation faster and adapt quicker if the scene changes [@ktkp01, p. 3]. The motivation to detect shadows is that shadows have some properties of the foreground (they are moving and usually co-occur with some foreground objects) while they are in general not an important part of the foreground (but just "occlude" some background).

The variant proposed by @ktkp01 is slightly more precise and expressive than former versions, as K-means was an approximation of EM and the new version allows to detect shadows. We will compare MOG with a similarly precise approach by @zivkovic04 below.

## Improved Adaptive Gaussian Mixture Model (MOG2)

@zivkovic06 use another adaptive method of @stauffer99. They introduce similar changes as @ktkp01 do: besides an adapting number of Gaussians they employ the "balloon estimator" [@zivkovic06, p. 4] as a different approximation of EM than K-means. Just like in MOG, MOG2 is able to detect shadows.

While the shadow detection again solves the problem @stauffer99 have with them, MOG and MOG2 have small differences in their performance.
In this algorithm the number of Gaussian distributions is adaptive but capped at five, and whenever one needs to be introduced because the others do not explain the new pixel, the Gaussian with the lowest probability (i.e. the Gaussian explaining the fewest number of pixels) is replaced by a new Gaussian. A pixel can not be explained by any of the Gaussians if it is farther away than $3$ standard deviations (compared to $2.5$ in MOG) from all existing Gaussians.

Concerning background detection performance (as can be measured by ROCs, cf. @zivkovic06, p. 6) the changes introduced in MOG2 do not significantly increase compared to the original method by @stauffer99. However, in terms of computation time @zivkovic06 score some improvements over their predecessor. This might be because K-means performs slower than the "balloon estimator" to estimate the Gaussian distributions.

The variant proposed by @zivkovic06 is slightly more precise and also more expressive than previous algorithms. Its biggest improvement is in terms of processing speed. However, comparing MOG2 to MOG below, we will see that the improved speed results in more noise for MOG2, while MOG fails to detect as much of the foreground as MOG2 does.


# Comparison

To compare the two algorithms MOG and MOG2 we use well known example videos. Two of them, "768x576" and "1920x1080" are provided as examples for using OpenCV [@opencv]. The other videos are taken from the dataset of the Advanced Video and Signal based Surveillance conference 2007 [@avss07], "AVSS AB Easy" (abandoned baggage), "AVSS PV Hard" (parked vehicles), "AVSS PV Night" (parked vehicles at night). Both algorithms are implemented in OpenCV (MOG[^linkmog], MOG2[^linkmog2]) [@opencv] and can be applied by our own [cvloop][linkcvloop] package as follows:

```python
%matplotlib notebook
from cvloop import cvloop
import cv2

def mog2(frame):
    return mog2.fgbg.apply(frame)
mog2.fgbg = cv2.createBackgroundSubtractorMOG2()
# for MOG use cv2.createBackgroundSubtractorMOG() equivalently

cvloop('768x576.avi', function=mog2)
```

This calculates the mask calculated by each algorithm. To subtract the background from the foreground we introduce the following small addition to mask the original image:

```python
import numpy as np

def mog2_fg_extractor(image):
    return image * (mog2(image) > 0)[:, :, np.newaxis]

cvloop('768x576.avi', function=mog2_fg_extractor)
```

We compared only specific frames per video: For the shorter OpenCV example videos we used frames 100, for the longer example videos from AVSS we used frame 500. The attached `.ipynb` also contains functions used to create Figures 1 and 2.


# Results

In general one of the most striking results is that MOG2 has fewer holes in the masks, leading to a clearer background subtraction. Of course this could be improved even further by closing those holes. Additionally MOG2 extracts the shadows -- it even distinguishes between shadows and foreground, but we just used both as the foreground. MOG should also be able to extract shadows [@ktkp01 Fig.1], however its OpenCV implementation does not provide an option for it. It is still okay to compare the results, as turning the shadow detection off in MOG2 results in the shadows simply being part of the foreground (Figure 1) -- the exact assumption we used for comparisons.

![Cropped masks of video 768x576: MOG2 applied with and without shadows. White areas are foreground, gray areas shadows and black denotes the background.](768x576_comp_fg_shadow_f100.png)


--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Video                      Frame No. Original Frame                            MOG Mask                                  MOG2 Mask
-------------------------- --------- ----------------------------------------- ----------------------------------------- ------------------------------------------
768x576                    100       ![](768x576_original_f100.png)            ![](768x576_mask_mog_f100.png)            ![](768x576_mask_mog2_f100.png)

1920x1080                  100       ![](1920x1080_original_f100.png)          ![](1920x1080_mask_mog_f100.png)          ![](1920x1080_mask_mog2_f100.png)

AVSS AB Easy               500       ![](AVSS_AB_Easy_Divx_original_f500.png)  ![](AVSS_AB_Easy_Divx_mask_mog_f500.png)  ![](AVSS_AB_Easy_Divx_mask_mog2_f500.png)

AVSS PV Hard               500       ![](AVSS_PV_Hard_Divx_original_f500.png)  ![](AVSS_PV_Hard_Divx_mask_mog_f500.png)  ![](AVSS_PV_Hard_Divx_mask_mog2_f500.png)

AVSS PV Night              500       ![](AVSS_PV_Night_Divx_original_f500.png) ![](AVSS_PV_Night_Divx_mask_mog_f500.png) ![](AVSS_PV_Night_Divx_mask_mog2_f500.png)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Table: Comparing masks for different example videos. Videos taken from [OpenCV][linkopencv] [@opencv] and [AVSS 2007][linkavss] [@avss07].


The better performance comes at a cost: There are couple of more false-positives, i.e. noise, in the resulting mask. Especially for the night scenario (cf. Table 1, AVSS PV Night/MOG2 Mask) there is much more noise in the image. This might also be because the image itself seems to be of a lower quality concerning noise and color depth. A slightly more subtle difference can be found in the MOG2 mask for the OpenCV video 768x576 (Figure 2): Even though the people are well found, there is a lot of noise across the whole image, probably because the scene is filmed from very far away and the foreground itself is really small.

![Cropped binary masks of video 768x576. It can clearly be seen that MOG (left) has fewer noise than MOG2 (right). When paying close attention to the split person in the center, one can also see a slight difference in the quality of the mask (at the legs).](768x576_comp_mask_f100.png)


---------------------------------------------------------------------------------------------------------------------------------------------------------------
Video                      Frame No. Original Frame                            MOG Foreground                          MOG2 Foreground
-------------------------- --------- ----------------------------------------- --------------------------------------- ----------------------------------------
768x576                    100       ![](768x576_original_f100.png)            ![](768x576_fg_mog_f100.png)            ![](768x576_fg_mog2_f100.png)

1920x1080                  100       ![](1920x1080_original_f100.png)          ![](1920x1080_fg_mog_f100.png)          ![](1920x1080_fg_mog2_f100.png)

AVSS AB Easy               500       ![](AVSS_AB_Easy_Divx_original_f500.png)  ![](AVSS_AB_Easy_Divx_fg_mog_f500.png)  ![](AVSS_AB_Easy_Divx_fg_mog2_f500.png)

AVSS PV Hard               500       ![](AVSS_PV_Hard_Divx_original_f500.png)  ![](AVSS_PV_Hard_Divx_fg_mog_f500.png)  ![](AVSS_PV_Hard_Divx_fg_mog2_f500.png)

AVSS PV Night              500       ![](AVSS_PV_Night_Divx_original_f500.png) ![](AVSS_PV_Night_Divx_fg_mog_f500.png) ![](AVSS_PV_Night_Divx_fg_mog2_f500.png)
---------------------------------------------------------------------------------------------------------------------------------------------------------------
Table: Comparing foreground extracted images for different example videos. Videos taken from [OpenCV][linkopencv] [@opencv] and [AVSS 2007][linkavss] [@avss07].


In @zivkovic06 it is also reported that they achieved an improved performance over a previous algorithm by @stauffer99. Due to the way we used the algorithm in Jupyter notebooks [@jupyter], we were not really able to measure the performance, or compare them in a meaningful way, as the matplotlib [@matplotlib] backend was really slow and we achieved nothing anywhere close to the reported 19 milliseconds per frame. Additionally the algorithm by @stauffer99 is not pre-implemented in OpenCV.


# Conclusion

The algorithms discussed in this report all perform pretty good in background detection. By making use of adaptive strategies they overcome problems previous approaches face and are even able to distinguish not only between fore- and background but also to detect shadows. The choice of choosing MOG over MOG2 or vice versa depends on someone's application -- MOG slightly more exact but slower while MOG2 introduces more noise at higher computation speed.


# References

[linkopencv]: https://github.com/opencv/opencv_extra/tree/7054d3f5d957c8f4849aea34aa1dcbadf4207a38/testdata/cv/video
[linkavss]: http://www.eecs.qmul.ac.uk/~andrea/avss2007_d.html
[linkcvloop]: https://pypi.python.org/pypi/cvloop/0.1.1
[^linkmog]: MOG: [https://github.com/opencv/opencv/blob/modules/cudabgsegm/src/mog.cpp](https://github.com/opencv/opencv/blob/modules/cudabgsegm/src/mog.cpp)
[^linkmog2]: MOG: [https://github.com/opencv/opencv/blob/modules/video/src/bgfg_gaussmix2.cpp](https://github.com/opencv/opencv/blob/modules/video/src/bgfg_gaussmix2.cpp)

