% Background Subtraction using Gaussian Mixture
% Alexander Höreth and Sebastian Höffner
% December 03, 2016


# Introduction
The following report will introduce the concept of applying Gaussian mixtures for computer vision tasks. Specifically we will discuss two algorithms which prove quite successful in background subtraction and tracking of animated objects in scenes.

The foundation for background subtraction approaches through statistical models like the ones presented in this report is the predictable property of static components in video streams. In order to fulfill the requirement of static components of a scene to actually appear as such we will in the following only discuss the case of statically positioned cameras. By fitting a statistical model to a scene which fulfills this requirement it is possible to track animated objects like people or cars by detecting resulting inconsistencies with the model's prediction.

The big challenge in fulfilling this rather straight forward idea is to update the model appropriately over time in order to smoothly handle changes in the static parts of the scene itself (e.g. parked cars or moved chairs) or for example to general lighting conditions.


# Background Subtraction
- Background/Foreground
- Surveillance
- Motion detection
- Image Segmentation

## Mixture of Gaussians
- wiki example?
- what is MoG


## Improved Adaptive Background Mixture Model (MOG)
- summary [@ktkp01], focus on MoG


# Improving Background Subtraction

## Improved Adaptive Gaussian Mixture Model (MOG2)
- [@zivkovic04], [@zivkovic06]
- Goal statement: what to improve
- point out changes

### Algorithm
- Summary of Algorithm

### OpenCV Implementation Details



# Comparison and Results

To compare the two algorithms we use well known example videos. Two of them, "768x576" and "1920x1080" are provided as examples for using OpenCV [@opencv]. The other videos are taken from the dataset of the Advanced Video and Signal based Surveillance conference 2007 [@avss07], "AVSS AB Easy" (abandoned baggage), "AVSS PV Hard" (parked vehicles), "AVSS PV Night" (parked vehicles at night).


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


In general one of the most striking results is that MOG2 has fewer holes in the masks, leading to a clearer background subtraction. Of course this could be improved even further by closing those holes. Additionally MOG2 extracts the shadows -- it even distinguishes between shadows and foreground, but we just used both as the foreground.

![Cropped binary masks of video 768x576. It can clearly be seen that MOG (left) has fewer noise than MOG2 (right). When paying close attention to the split person in the center, one can also see a slight difference in the quality of the mask (at the legs).](768x576_comp_mask_f100.png)

The better performance comes at a cost: There are couple of more false-positives, i.e. noise, in the resulting mask. Especially for the night scenario (cf. Table 2, AVSS PV Night/MOG2 Mask) there is much more noise in the image. This might also be because the image itself seems to be of a lower quality concerning noise and color depth. A slightly more subtle difference can be found in the MOG2 mask for the OpenCV video 768x576 (Figure 1): Even though the people are well found, there is a lot of noise across the whole image, probably because the scene is filmed from very far away and the foreground itself is really small.


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


In @zivkovic06 it is also reported that they achieved an improved performance. Due to the way we used the algorithm in Jupyter notebooks [@jupyter], we were not really able to measure the performance, or compare them in a meaningful way, as the matplotlib [@matplotlib] backend was really slow and we achieved nothing anywhere close to the reported 19 milliseconds per frame.


# References

[linkopencv]: https://github.com/opencv/opencv_extra/tree/7054d3f5d957c8f4849aea34aa1dcbadf4207a38/testdata/cv/video
[linkavss]: http://www.eecs.qmul.ac.uk/~andrea/avss2007_d.html

