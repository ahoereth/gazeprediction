% Application of the Biologically-Inspired Model
% Alexander Höreth and Sebastian Höffner
% November 20, 2016

# Saliency-Based Visual Attention for Rapid Scene Analysis

Itti et al.\ propose a model to predict in which order interesting elements of a scene are attended [@itti].
Their model is strongly biologically inspired and depends on several findings from Neuroscience.

To predict the order of attention, Itti et al.\ use a combination of different features to build a saliency map, which highlights interesting regions. These features can be roughly compared to biological features:

- Color features (based on the opponent process of cones)
- Intensity features (inspired by the intensity perception of rods)
- Orientation features (inspired by the orientation filters in the visual cortex)

These features are combined to form a saliency map. This saliency map can then be used in
a winner-take-all (WTA) network to predict the order in which objects will be attended by
a viewer of the input scene.

This report will include our results and findings when implementing the model and testing it with some given example images. After that we will briefly discuss WTA networks and their implementation. We close the report with a small discussion about what needs to be changed for this approach to work with gray images.

# Task 1: Implementation

Our implementation can be found in the attached `gabor_saliency.py`, as well as in the IPython Notebook `task2.ipynb`. Most of the implementation is straight forward from the paper, however some parameters have to be found by careful tuning. Some parameters work better with certain images, while they do not work well with others. We tried to choose a parameter set which works for most example images.

## Parameters

The parameters for the Gabor filters which led to convincing results were selected as follows: The kernel size is fixed to 16x16. This might not work too well for images larger than our biggest example image, but for the given examples, which are just between 380 and 700 pixels in their largest dimension, a size of 16x16 seems to be sufficient for good results.
$\sigma$ is set to 2, $\lambda$ to 10. This seemed to be fine to stretch the Kernels tall enough into the 16x16 filters. For other kernel sizes, these parameters might need further adjustments.
All remaining parameters were given ($\gamma=0.5$, $\psi=0$, and $\theta \in \{0, 45, 90, 135\}$).

The resulting Gabor patches look like this:

![](voc2012_000138_gabor_0.png){width=300}\ ![](voc2012_000138_gabor_1.png){width=300}\ ![](voc2012_000138_gabor_2.png){width=300}\ ![](voc2012_000138_gabor_3.png){width=300}

## Gray image

The gray image for the convolutions is calculated with a costum formula instead of the OpenCV suggestion, as the latter was more difficult to handle because of its returned data types. To circumvent this problem, we used:

    img_gray = np.dot(img[..., :3], [.299, .587, .114])

The results should be the same as we would achieve with `cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)`[^color].

[^color]: Note that we rotated the color channels before, hence the `RGB2GRAY` and not `BGR2GRAY`.

![Gray image](voc2012_000138_gray.png){width=400}

## Gabor filtered results

![Gabor filtered 0 degrees](voc2012_000138_gabored_0.png){width=200}\ ![Gabor filtered 45 degrees](voc2012_000138_gabored_1.png){width=200}

![Gabor filtered 90 degrees](voc2012_000138_gabored_2.png){width=200}\ ![Gabor filtered 135 degrees](voc2012_000138_gabored_3.png){width=200}

## Saliency Map

Combining the features (intensities, colors, and the shown orientation maps) properly results in the saliency map:

![Saliency Map](voc2012_000138_saliency.png){width=200}

Note that we scaled up the saliency map to the original image size for better comparison.

# Results

We applied the algorithm to all four example images. Here are the resulting saliency maps next to the original images.

![](640x480/test0.jpg){width=100}\ ![](test0_saliency.png){width=200}

![](384x384/test1.jpg){width=100}\ ![](test1_saliency.png){width=200}

![](384x384/test2.jpg){width=100}\ ![](test2_saliency.png){width=200}

![](500x357/voc2012_000122.jpg){width=100}\ ![](voc2012_000122_saliency.png){width=200}

![](500x357/voc2012_000138.jpg){width=100}\ ![](voc2012_000138_saliency.png){width=200}

# Winner-take-all network

Winner-take-all networks (WTA) are a special type of neural networks which take an input and compete for firing. In this special application we can implement them to find the saliency richest region in the image.

For each pixel we have one neuron which competes with its neighboring neurons. The neuron with the highest input value (i.e. the saliency pixel map value) wins each of these small competitions and goes on into the next "round" (which can be implemented as another layer). As a reward, its value is now increased by the values of its former competitors, resulting in a higher competition value for the next comparison.

This process is repeated until only one neuron is left, which is the most salient neuron inside a salient region.

An area around this neuron is now "attended" and all pixels are set to zero, which means the corresponding neurons are inhibited. Then the process restarts to find the second most interesting region, until either enough regions were found or the image is completely inhibited (i.e. everything is zero).

# Gray images

To use the presented algorithm with gray images instead of color images, two options seem to be plausible: Conversion to RGB or pruning the path.

## Conversion to RGB

This method relies on increasing the number of dimensions to three by either duplicating the gray channel into R, G, and B channels or by doing some more sophisticated transformations to achieve the same. After that, the algorithm can be applied normally. However, it might be important to also weigh the different features (intensity, orientations, colors) with other weights than $\frac{1}{3}$, since the color is already a big part of the intensity in the RGB case.

## Pruning the path

For this method it is easiest to just completely ignore the color and only rely on intensity
and orientations. This means pruning the left path of the model presented by Itti et al., such that eventually only intensity and orientation are taken into account with weights of $0.5$ each.

# References

