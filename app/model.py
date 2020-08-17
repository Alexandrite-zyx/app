#import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
from PIL import Image
import numpy as np
from tensorflow import keras


def plot_image(predictions_array, img):
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    # plt.figure(figsize=(6,3))
    # plt.subplot(1,2,1)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, cmap=plt.cm.binary)
    predicted_label = np.argmax(predictions_array)

    plt.xlabel("{} ".format(class_names[predicted_label]
                            ))
    '''
    plt.subplot(1,2,2)
    plt.grid(False)
    thisplot = plt.bar(range(10),predictions_array[0])
    plt.xticks(range(10))
    plt.yticks([])                   
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array[0])
    thisplot[predicted_label].set_color('red')
    '''
    plt.savefig('static/result/res.png')


def cloth_predict(img):
    '''fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    test_images = test_images / 255'''

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    model = tf.keras.models.load_model('model.h5', compile=False)

    img = img.convert('L')

    img = img.resize((28, 28))
    color_0 = img.getpixel((0, 0))
    for h in range(28):
        for l in range(28):
            dot = (l, h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = 0
                img.putpixel(dot, color_1)
    '''
    plt.imshow(img)
    plt.show()
    '''
    # img = mpimg.imread('Img.png')

    Img = (np.expand_dims(img, 0))
    # Img = np.expand_dims(Img,-1)

    probability_model = tf.keras.Sequential([model,
                                             tf.keras.layers.Softmax()])

    predictions = probability_model.predict(Img)

    return class_names[np.argmax(predictions)], predictions
    '''
    plt.figure(figsize=(6,3))
    plt.subplot(1,2,1)
    plot_image(predictions, img)
  
    plt.subplot(1,2,2)
    plot_value_array(predictions[0])
    _ = plt.xticks(range(10), class_names, rotation=45)
    plt.show()
    '''


if __name__ == '__main__':
    img = Image.open('xuezi.png')
    res, predictions = cloth_predict(img)
    '''
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    model = tf.keras.models.load_model('saved_modell/my_model')
    train_images=np.expand_dims(train_images,-1)
    test_images=np.expand_dims(test_images,-1)
    predictions = model.predict(test_images)
    '''
    print(predictions)


