# 🙋 FaceDetector

1. [About](#about)
2. [Results](#results)
3. [Speed](#results)
4. [Demo](#demo)
	* [Japanese Animation](#japanese-animation)
5. [License](#license)


## 📖 About <a name="about"></a>

FaceDetector is a model that detects faces in an image and returns the bounding boxes of the faces.
It is based on a Faster R-CNN ResNet-50 FPN model trained on a custom dataset of 17,811 real-world / drawn faces.

## 📈 Results <a name="results"></a>

Currently this model is able to detect faces with an average precision of ~96% which is quite low.

This is due to the fact that the training dataset is quite small, and contains a lot of different types of faces (real-life humans, drawn humans, animals, realistic drawings, etc), but also because they're not always directly looking at the camera, and might be hidden behind small objects, hair, glasses, sunglasses, or even occluded by other faces.

## 🕰️ Speed <a name="speed"></a>

The model is able to run at ~8 FPS (1920x1080) on a modern CPU (tested on a Ryzen 7 5900X) (single-threaded).

## 🎥 Demo <a name="demo"></a>

Under this section you can find some examples of the model in action.

While this is fairly disturbing to look at, it's also quite fun to see how the model performs on different types of images.

_**note**: Even though it is not demonstrated here, this model CAN find faces of real humans_

_**note2** : I will add examples of movies, YouTube videos_

### 🖌️ Japanese Animation <a name="japanese-animation"></a>

Here's how the model performs on a 15-second clip of a Japanese animation.

#### First example

- Static background
- Animated background
- Wearing glasses
- Moving character
- Far-away shot

https://user-images.githubusercontent.com/20666343/194108288-32c17682-c223-4311-916d-2f870eca731f.mp4

#### Second example

- Small face
- Hand in front of the face
- Wearing glasses
- Moving character
- Side shot
- Sweat droplets
- Multiple characters

_(despite few misses, the model still manages a great job at detecting the face)_

https://user-images.githubusercontent.com/20666343/194108293-d45753dd-a773-44b2-b2c0-02e2771df200.mp4

#### Third example

- Wearing sunglasses
- Speaking character (moving jaw and mouth)
- Multiple characters
- Face partially hidden by a door
- Male character (dataset is mostly composed of female characters)

https://user-images.githubusercontent.com/20666343/194108296-0c957b90-fcc3-4b2e-89f2-b2a128695578.mp4


## 📝 License <a name="license"></a>

This model is licensed under the [Attribution-ShareAlike 2.0 Generic (CC BY-SA 2.0)](https://creativecommons.org/licenses/by-sa/2.0/) license.

Which means you're free to use it for any purpose, even commercially, as long as you give credit this repository and share your modifications under the same license.
