% Application of the Biologically-Inspired Model
% Alexander Höreth and Sebastian Höffner
% December 03, 2016

# Adaptive Gaussian Mixture Model for Background Subtraction

## Introduction
The following report will introduce the concept of applying Gaussian mixtures for computer vision tasks. Specifically we will discuss two algorithms which prove quite successful in background subtraction and tracking of animated objects in scenes.

The foundation for background subtraction approaches through statistical models like the ones presented in this report is the predictable property of static components in video streams. In order to fulfill the requirement of static components of a scene to actually appear as such we will in the following only discuss the case of statically positioned cameras. By fitting a statistical model to a scene which fulfills this requirement it is possible to track animated objects like people or cars by detecting resulting inconsistencies with the model's prediction.

The big challenge in fulfilling this rather straight forward idea is to update the model appropriately over time in order to smoothly handle changes in the static parts of the scene itself (e.g. parked cars or moved chairs) or for example to general lighting conditions.


## Gaussian Mixtures




"An improved adaptive background mixture model for real-time tracking with shadow detection" by P. KadewTraKuPong and R. Bowden in 2001

Z.Zivkovic, "Improved adaptive Gausian mixture model for background subtraction"
