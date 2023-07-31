import tensorflow as tf
from tensorflow.keras import datasets, layers, optimizers, Sequential
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

(x, y), _ = datasets.mnist.load_data()
x = tf.convert_to_tensor(x, dtype=tf.float32) / 255.
y = tf.convert_to_tensor(y, dtype=tf.int32)

print(x.shape, y.shape, x.dtype, y.dtype)
print(tf.reduce_min(x), tf.reduce_max(x))
print(tf.reduce_min(y), tf.reduce_max(y))

train_db = tf.data.Dataset.from_tensor_slices((x, y)).batch(128)
train_iter = iter(train_db)
sample = next(train_iter)

print('batch: ', sample[0].shape, sample[1].shape)

w1 = tf.Variable(tf.random.truncated_normal([784, 256], stddev=0.1))
b1 = tf.Variable(tf.zeros([256]))
w2 = tf.Variable(tf.random.truncated_normal([256, 128], stddev=0.1))
b2 = tf.Variable(tf.zeros([128]))
w3 = tf.Variable(tf.random.truncated_normal([128, 10], stddev=0.1))
b3 = tf.Variable(tf.zeros([10]))

# lr = 1e-4
lr = 1e-3

# for step, (x, y) in enumerate(db):
#     print(step, x.shape, y.shape)

model = Sequential([
    layers.Dense(512, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(10)
])

optimizer = optimizers.SGD(learning_rate=0.000001)

for epoch in range(10):
    for step, (x, y) in enumerate(train_db):
        x = tf.reshape(x, [-1, 28*28])
        with tf.GradientTape() as tape:

            h1 = x@w1 + tf.broadcast_to(b1, [x.shape[0], 256])
            h1 = tf.nn.relu(h1)

            h2 = h1@w2 + b2
            h2 = tf.nn.relu(h2)

            out = h2@w3 +b3
            y_onehot = tf.one_hot(y, depth=10)

            loss = tf.square(y_onehot - out)
            loss = tf.reduce_mean(loss)

        # grads=梯度
        grads = tape.gradient(loss, [w1, b1, w2, b2, w3, b3])
        # for g in grads:
        #     print('----------->', step, tf.norm(g))
        # grads,_ = tf.clip_by_global_norm(grads, 15000)

        w1.assign_sub(lr * grads[0])
        b1.assign_sub(lr * grads[1])
        w2.assign_sub(lr * grads[2])
        b2.assign_sub(lr * grads[3])
        w3.assign_sub(lr * grads[4])
        b3.assign_sub(lr * grads[5])

        # optimizer.apply_gradients(zip(grads, [w1, b1, w2, b2, w3, b3]))

        if step % 100 == 0:
            print(epoch, step, 'loss: ', float(loss))
        #
        #     x = tf.reshape(x, (-1, 28 * 28))
        #     out = model(x)
        #     loss = tf.reduce_sum(tf.square(out - y)) / x.shape[0]
        # grads = tape.gradient(loss, model.trainable_variables)
        # optimizer.apply_gradients(zip(grads, model.trainable_variables))
        #
        # if step % 100 == 0:
        #     print(step, )
