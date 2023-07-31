import tensorflow as tf
from tensorflow.keras import datasets, Sequential, layers, optimizers
import datetime
from matplotlib import pyplot as plt
import io

def preprocess(x, y):
    x = tf.cast(x, dtype=tf.float32) / 255.
    y = tf.cast(y, dtype=tf.int32)
    return x, y


def plot_to_image(figure):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(figure)
    buf.seek(0)
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    image = tf.expand_dims(image, 0)
    return image


def image_grid(images):
    figure = plt.figure(figsize=(10, 10))
    for i in range(25):
        plt.subplot(5, 5, i + 1, title='name')
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i], cmap=plt.cm.binary)
    return figure

(x, y), (test_x, test_y) = datasets.mnist.load_data()

train_db = tf.data.Dataset.from_tensor_slices((x, y))
train_db = train_db.map(preprocess).shuffle(10000).batch(128).repeat(10)

test_db = tf.data.Dataset.from_tensor_slices((test_x, test_y))
test_db = test_db.map(preprocess).shuffle(10000).batch(128, drop_remainder=True)

network = Sequential([
    layers.Dense(256, activation=tf.nn.relu),
    layers.Dense(128, activation=tf.nn.relu),
    layers.Dense(64, activation=tf.nn.relu),
    layers.Dense(32, activation=tf.nn.relu),
    layers.Dense(10),
])

current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_dir = 'log_tmp/' + current_time
summary_writer = tf.summary.create_file_writer(log_dir)

sample_img = next(iter(train_db))[0]
sample_img = sample_img[0]
sample_img = tf.reshape(sample_img, [1, 28, 28, 1])

with summary_writer.as_default():
    tf.summary.image("Training sample:", sample_img, step=0)

optimizer = optimizers.Adam(0.00001)

for epoch in range(10):
    for step, (x, y) in enumerate(train_db):
        x = tf.reshape(x, [-1, 28*28])

        with tf.GradientTape() as tape:
            digits = network(x)

            y_onehot = tf.one_hot(y, depth=10)
            loss = tf.reduce_mean(tf.keras.losses.categorical_crossentropy(y_onehot, digits, from_logits=True))

        grads = tape.gradient(loss, network.trainable_variables)
        optimizer.apply_gradients(zip(grads, network.trainable_variables))

        if step % 100 == 0:
            print(epoch, step, 'loss: ', float(loss))

            with summary_writer.as_default():
                tf.summary.scalar('train-loss', float(loss), step=step)

    total, total_correct = 0., 0
    for step, (x, y) in enumerate(test_db):
        x = tf.reshape(x, [-1, 28*28])
        out = network(x)
        pred = tf.argmax(out, axis=1)
        pred = tf.cast(pred, dtype=tf.int32)
        correct = tf.equal(pred, y)
        total += x.shape[0]
        total_correct += tf.reduce_sum(tf.cast(correct, dtype=tf.int32)).numpy()
        print(step, 'Evaluate Acc: ', total_correct / total)

        val_images = x[:25]
        val_images = tf.reshape(val_images, [-1, 28, 28, 1])
        with summary_writer.as_default():
            tf.summary.scalar('test-acc', float(total_correct / total), step=step)
            val_images = tf.reshape(val_images, [-1, 28, 28])
            figure = image_grid(val_images)
            tf.summary.image('val_images:', plot_to_image(figure), step=step)

