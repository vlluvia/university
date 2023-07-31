import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras import datasets, layers, optimizers, Sequential, metrics, losses

(train_images, train_labels), (_, _) = datasets.mnist.load_data()
train_images = tf.expand_dims(train_images, -1)

train_images = tf.cast(train_images, tf.float32)
train_images = (train_images - 127.5) / 127.5

BATCH_SIZE = 64
datasets = tf.data.Dataset.from_tensor_slices(train_images)
datasets = datasets.shuffle(60000).batch(BATCH_SIZE)


def genterator_model():
    model = Sequential()
    model.add(layers.Dense(256, input_shape=(100,), use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Dense(512, use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Dense(28 * 28, use_bias=False, activation="tanh"))
    model.add(layers.BatchNormalization())

    model.add(layers.Reshape((28, 28, 1)))

    return model


def discriminator_model():
    model = Sequential()
    model.add(layers.Flatten())

    model.add(layers.Dense(512, use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Dense(256, use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Dense(1))

    return model


cross_entropy = losses.BinaryCrossentropy(from_logits=True)


def discriminator_loss(real_out, fake_out):
    image_real_loss = cross_entropy(0.9 * tf.ones_like(real_out), real_out)
    image_fake_loss = cross_entropy(tf.zeros_like(fake_out), fake_out)
    return image_real_loss + image_fake_loss


def generator_loss(fake_out):
    image_fake_loss = cross_entropy(0.9 * tf.ones_like(fake_out), fake_out)
    return image_fake_loss


generator_optimizer = optimizers.Adam(1e-4)
discriminator_optimizer = optimizers.Adam(1e-4)

epochs = 100
noise_dim = 100
nsample = 20
z = tf.random.normal([nsample, noise_dim])

generator = genterator_model()
discriminator = discriminator_model()


@tf.function
def train_step(images):  # [64, 28, 28, 1]
    noise = tf.random.normal([BATCH_SIZE, noise_dim])  # [64, 100]

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        gen_image = generator(noise, training=True)

        real_out = discriminator(images, training=True)
        fake_out = discriminator(gen_image, training=True)

        gen_loss = generator_loss(fake_out)
        disc_loss = discriminator_loss(real_out, fake_out)

    gradient_gen = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradient_disc = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradient_gen, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradient_disc, discriminator.trainable_variables))


def generator_plot_images(gen_model, test_noise):
    pred_images = gen_model(test_noise, training=False)
    fig = plt.figure(figsize=(20, 1))

    for i in range(nsample):
        plt.subplot(1, 20, i + 1)
        plt.imshow((pred_images[i, :, :, 0] + 1) / 2, cmap='binary')
        plt.axis('off')

    plt.show()


def train(dataset, epochs):
    for epoch in range(epochs):
        for image_batch in dataset:
            train_step(image_batch)

        print("Epoch{}/{}".format(epoch + 1, epochs))
        generator_plot_images(generator, z)


train(datasets, epochs)
