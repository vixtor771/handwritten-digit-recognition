import numpy as np, gzip, sys
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent      # skill demonstration 文件夹
DATA, RESULTS, FIGS = BASE / 'Data' / 'MNIST', BASE / 'Results', BASE / 'Figures'

# ---------- 读数据 ----------
def load_images(path):
    with gzip.open(path) as f:
        data = np.frombuffer(f.read(), np.uint8, offset=16)
    return data.reshape(-1, 784) / 255.0          # 每张图 = 784 个 0~1 之间的数


def load_labels(path):
    with gzip.open(path) as f:
        return np.frombuffer(f.read(), np.uint8, offset=8)


x_train = load_images(f'{DATA}/train-images-idx3-ubyte.gz'); y_train = load_labels(f'{DATA}/train-labels-idx1-ubyte.gz')
x_test  = load_images(f'{DATA}/t10k-images-idx3-ubyte.gz');  y_test  = load_labels(f'{DATA}/t10k-labels-idx1-ubyte.gz')


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


# ---------- 网络：784 -> 1000 -> 10 ----------
def feedforward(W0, W1, s0):
    s1 = sigmoid(W0 @ s0)        # 1000 个中间神经元
    s2 = sigmoid(W1 @ s1)        # 10 个输出神经元
    return s1, s2


def error_rate(W0, W1):
    out = sigmoid(W1 @ sigmoid(W0 @ x_test.T))   # 一次算完 10000 张测试图
    return np.mean(out.argmax(0) != y_test)      # 输出最大的那个神经元 = 网络猜的数字


def mean_angle(W0, W1, B, n=500):
    # 随机反馈 B 传回的信号 和 backprop 用 W1.T 传回的信号 之间的平均夹角（度）
    angs = []
    for k in range(n):
        s1, s2 = feedforward(W0, W1, x_train[k])
        target = np.zeros(10); target[y_train[k]] = 1.0
        delta2 = (s2 - target) * s2 * (1 - s2)
        a, b = B @ delta2, W1.T @ delta2
        angs.append(np.degrees(np.arccos(np.clip(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)), -1, 1))))
    return np.mean(angs)


def train(method, n_epochs, alpha, b_scale, seed=0):
    rng = np.random.default_rng(seed)
    W0 = rng.uniform(-0.05, 0.05, (1000, 784))       # 输入 -> 中间层
    W1 = rng.uniform(-0.05, 0.05, (10, 1000))        # 中间层 -> 输出
    B  = rng.uniform(-b_scale, b_scale, (1000, 10))  # 只给 feedback alignment 用，训练中固定不变
    test_err = [error_rate(W0, W1)]
    angles = [(0, mean_angle(W0, W1, B))]
    step = 0
    for epoch in range(n_epochs):
        for k in rng.permutation(len(x_train)):
            s0 = x_train[k]
            target = np.zeros(10); target[y_train[k]] = 1.0     # 正确答案：对应数字那一格是 1，其余是 0
            s1, s2 = feedforward(W0, W1, s0)

            delta2 = (s2 - target) * s2 * (1 - s2)               # 输出层的 delta（10 个）
            if method == 'bp':
                delta1 = (W1.T @ delta2) * s1 * (1 - s1)        # 用正向权重 W1 把误差传回来
            elif method == 'fa':
                delta1 = (B @ delta2) * s1 * (1 - s1)           # 用固定的随机数 B 把误差传回来
            else:
                delta1 = np.zeros(1000)                          # shallow：中间层不学，只训练最后一层

            W1 -= alpha * np.outer(delta2, s1)
            W0 -= alpha * np.outer(delta1, s0)

            step += 1
            if method == 'fa' and (step <= 20000 and step % 1000 == 0 or step % 10000 == 0):
                angles.append((step, mean_angle(W0, W1, B)))
        test_err.append(error_rate(W0, W1))
        print(f'{method} epoch {epoch+1}: test error {100*test_err[-1]:.2f}%', flush=True)
    return W0, W1, B, np.array(test_err), np.array(angles)


if __name__ == '__main__':
    method, n_epochs, alpha, b_scale = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    W0, W1, B, err, ang = train(method, n_epochs, alpha, b_scale)
    np.savez(RESULTS / f'result_{method}.npz', W0=W0, W1=W1, B=B, err=err, ang=ang)
