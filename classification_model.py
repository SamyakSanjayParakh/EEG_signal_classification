# -*- coding: utf-8 -*-
"""Classification_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TNUa_-P5WJXf_f_4WqnZoE8Eys9i3YBv
"""

pip install numpy

import numpy as np
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

# Specify the path to your .npy file
file_path = '/content/drive/My Drive/resultant_data.npy'

# Load the .npy file
data = np.load(file_path,allow_pickle=True)

# Display the data (optional)
print(len(data))

# Specify the path to your .npy file
file_path = '/content/drive/My Drive/epoched_data_lables.npy'

# Load the .npy file
label = np.load(file_path,allow_pickle=True)

# Display the data (optional)
print(len(label))

file_path = '/content/drive/My Drive/X2_train.npy'

# Load the .npy file
X2_train =np.zeros((3396,96,6144,3))# np.load(file_path,allow_pickle=True)

# Display the data (optional)
print(X2_train.shape)

n=0
for i in range(10):

  a=data[i].shape
  n=n+a[0]
  print(a[0])
print(n)
# data_reshaped=data.reshape(a[0]*10,a[1],a[2])
# print()
  # data_reshaped=data.reshape()

# for j in range(n):
reshaped_data=np.zeros((n,64,961))
# for i in range(10):
  # a=data[i].shape
reshaped_data= np.vstack((data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))#,data[1],data[1],))
print(reshaped_data.shape)
reshaped_data.reshape((n,64,961,1))
print(reshaped_data.shape)

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv3D, MaxPooling3D, Flatten, Dense, Reshape, Concatenate
# from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense
# Input shapes
# input_shape1 = (64, 961, 1)  # First input: (64, 961)
# input_shape2 = (241, 15424, 3)  # Second input: (96, 6144, 3)
num_classes = 9  # Number of classes
input_shape = (64, 241, 64, 1)
feature_vector_size = (24, 24)
timesteps = 64
features = 961
latent_dim = 100
# # Define the first input branch
# input1 = Input(shape=input_shape1)
# x1 = Conv2D(32, (3, 3), activation='relu')(input1)
# x1 = MaxPooling2D((2, 2))(x1)
# x1 = Conv2D(64, (3, 3), activation='relu')(x1)
# x1 = MaxPooling2D((2, 2))(x1)
# x1 = Flatten()(x1)

# input1 = Input(shape=input_shape1)
# x = LSTM(128, return_sequences=True)(inputs)  # First LSTM layer
# x = LSTM(128)(x)  # Second LSTM layer without return_sequences to reduce dimensionality
# x = Dense(100, activation='relu')(x)
inputs = Input(shape=(timesteps, features))

# Encoder
encoded = LSTM(256, activation='relu')(inputs)
encoded = Dense(latent_dim, activation='relu')(encoded)

# Decoder
decoded = RepeatVector(timesteps)(encoded)
decoded = LSTM(256, activation='relu', return_sequences=True)(decoded)
decoded = TimeDistributed(Dense(features))(decoded)

# Autoencoder model
autoencoder = Model(inputs, decoded)

# Encoder model for feature extraction
encoder = Model(inputs, encoded)
# Define the second input branch
inputs2 = Input(shape=input_shape)

    # Convolutional layers with pooling
x2 = Conv3D(32, kernel_size=(3, 3, 3), activation='relu')(inputs2)
x2 = MaxPooling3D(pool_size=(2, 2, 2))(x2)

x2 = Conv3D(64, kernel_size=(3, 3, 3), activation='relu')(x2)
x2 = MaxPooling3D(pool_size=(2, 2, 2))(x2)

x2 = Conv3D(128, kernel_size=(3, 3, 3), activation='relu')(x2)
x2 = MaxPooling3D(pool_size=(2, 2, 2))(x2)

    # Flatten the output and add fully connected layers
x2 = Flatten()(x2)
x2 = Dense(512, activation='relu')(x2)
# x2 = Dense(feature_vector_size[0] * feature_vector_size[1], activation='relu')(x2)

    # Reshape to the desired feature vector size
# outputs2 = Reshape(feature_vector_size)(x2)

# Concatenate the outputs of the two branches
concatenated = Concatenate()([encoder.output, x2])

# Dense network
dense1 = Dense(612, activation='relu')(concatenated)
dense2 = Dense(256, activation='relu')(dense1)
output = Dense(num_classes+1, activation='softmax')(dense2)

# Create the model
model = Model(inputs=[inputs, inputs2], outputs=output)
autoencoder.compile(optimizer='adam', loss='mse')
# autoencoder.fit(data, data, epochs=50, batch_size=32, validation_split=0.2)
# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

import numpy as np

# Specify the path to your .npy file in Google Drive
file_path = '/content/drive/MyDrive/Copyofgaf_images_e_1-5.npy'

# Load the .npy file
imag = np.load(file_path)

# Print the loaded data (optional)
print(imag.shape)

# Assuming X1_train and X2_train are your two forms of input data, and y_train are your labels
# X1_train.shape = (3396, 64, 961, 1)
# X2_train.shape = (3396, 961, 961, 1)
# y_train.shape = (3396,)
# X2_train=np.random.rand(3396, 961, 6144,3)

history = model.fit([reshaped_data[:5], imag], label[:5], epochs=1, batch_size=32, validation_split=0.2)

m=model.predict([reshaped_data[:5], imag])
print(m)

print(sum(m[2]))

# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense

# # Data dimensions
# n_samples = 348
# timesteps = 64
# features = 961
# latent_dim = 100

# # Define the LSTM autoencoder
# inputs = Input(shape=(timesteps, features))

# # Encoder
# encoded = LSTM(256, activation='relu')(inputs)
# encoded = Dense(latent_dim, activation='relu')(encoded)

# # Decoder
# decoded = RepeatVector(timesteps)(encoded)
# decoded = LSTM(256, activation='relu', return_sequences=True)(decoded)
# decoded = TimeDistributed(Dense(features))(decoded)

# # Autoencoder model
# autoencoder = Model(inputs, decoded)

# # Encoder model for feature extraction
# encoder = Model(inputs, encoded)

# # Compile the autoencoder
# autoencoder.compile(optimizer='adam', loss='mse')

# # Print the model summary
# autoencoder.summary()

# # Generate some dummy data
# data = np.random.rand(n_samples, timesteps, features)

# # Train the autoencoder
# autoencoder.fit(data, data, epochs=50, batch_size=32, validation_split=0.2)

# # Extract features using the encoder
# features = encoder.predict(data)
# print("Extracted features shape:", features.shape)

# import tensorflow as tf
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Input, Conv3D, MaxPooling3D, Flatten, Dense, Reshape

# def create_3d_cnn(input_shape=(64, 241, 64, 1), feature_vector_size=(24, 24)):
#     inputs = Input(shape=input_shape)

#     # Convolutional layers with pooling
#     x = Conv3D(32, kernel_size=(3, 3, 3), activation='relu')(inputs)
#     x = MaxPooling3D(pool_size=(2, 2, 2))(x)

#     x = Conv3D(64, kernel_size=(3, 3, 3), activation='relu')(x)
#     x = MaxPooling3D(pool_size=(2, 2, 2))(x)

#     x = Conv3D(128, kernel_size=(3, 3, 3), activation='relu')(x)
#     x = MaxPooling3D(pool_size=(2, 2, 2))(x)

#     # Flatten the output and add fully connected layers
#     x = Flatten()(x)
#     x = Dense(512, activation='relu')(x)
#     x = Dense(feature_vector_size[0] * feature_vector_size[1], activation='relu')(x)

#     # Reshape to the desired feature vector size
#     outputs = Reshape(feature_vector_size)(x)

#     # Create the model
#     model = Model(inputs, outputs)

#     # Compile the model
#     model.compile(optimizer='adam', loss='mse')

#     return model

# # Define the input shape and feature vector size
# input_shape = (64, 241, 64, 1)
# feature_vector_size = (24, 24)

# # Create the model
# model = create_3d_cnn(input_shape=input_shape, feature_vector_size=feature_vector_size)

# # Print the model summary
# model.summary()