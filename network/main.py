# データのロード
import numpy as np
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# データの整形
x_train = x_train.astype('float32') / 255
y_train = np.eye(10)[y_train.astype('int32').flatten()]

x_test = x_test.astype('float32') / 255
y_test = np.eye(10)[y_test.astype('int32').flatten()]

x_train, x_valid, y_train, y_valid = train_test_split(
    x_train, y_train, test_size=10000)

# 4次元にしておかないと、
# model.fitのときに下記エラーが出てきてしまう
# ValueError: ('Input data in `NumpyArrayIterator`
# should have rank 4. You passed an array with shape', (50000, 28, 28))
x_test = x_test.reshape(-1, 28, 28, 1)
x_train = x_train.reshape(-1, 28, 28, 1)
x_valid = x_valid.reshape(-1, 28, 28, 1)

# モデル構築
model = Sequential()

# 28x28x3 -> 28x28x6
model.add(Conv2D(6, kernel_size=(5, 5), activation='relu',
                 kernel_initializer='he_normal', input_shape=(28, 28, 1)))
# 28x28x6 -> 14x14x6
model.add(MaxPooling2D(pool_size=(2, 2)))
# 14x14x6 -> 10x10x16
model.add(Conv2D(16, kernel_size=(5, 5), activation='relu',
                 kernel_initializer='he_normal'))
# 10x10x16 -> 5x5x16
model.add(MaxPooling2D(pool_size=(2, 2)))
# 5x5x16 -> 400
model.add(Flatten())
# 400 -> 120
model.add(Dense(120, activation='relu',
                kernel_initializer='he_normal'))
# 120 ->84
model.add(Dense(84, activation='relu', kernel_initializer='he_normal'))
# 84 ->10
model.add(Dense(10, activation='softmax'))

model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer='adam',
    metrics=['accuracy']
)

# データのかさまし
datagen = ImageDataGenerator(
    width_shift_range=0.2,  # 3.1.1 左右にずらす
    height_shift_range=0.2,  # 3.1.2 上下にずらす
    horizontal_flip=True,  # 3.1.3 左右反転
    # 3.2.1 Global Contrast Normalization (GCN) (Falseに設定しているのでここでは使用していない)
    samplewise_center=False,
    samplewise_std_normalization=False,
    zca_whitening=False)  # 3.2.2 Zero-phase Component Analysis (ZCA) Whitening (Falseに設定しているのでここでは使用していない)

# 学習
model.fit(datagen.flow(x_train, y_train, batch_size=100),
          steps_per_epoch=x_train.shape[0] // 100, epochs=30, validation_data=(x_valid, y_valid))

# 性能評価
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# 予測
input_data = []
input_data.append(x_test[100])
input_data = np.asarray(input_data)
print(model.predict(input_data))

# モデルの保存
model.save('cnn_model.h5', include_optimizer=True)
