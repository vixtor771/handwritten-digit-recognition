# Handwritten Digit Recognition

Team 3 skill demonstration for EN.553.696 Methods in Computational Neuroscience (Fall 2026).

We train a 784 → 1000 → 10 network on MNIST with plain numpy, using backpropagation and feedback alignment (Lillicrap et al., 2016, Nature Communications 7, 13276).

## Results (20 epochs, 10,000 test images)

| Method | Test accuracy |
|---|---|
| Backpropagation | 98.33% |
| Feedback alignment | 98.01% |
| Last layer only (hidden layer never trained) | 89.59% |

Each method was run once with one random seed.

## Files

- `Code/mnist_fa.py`: trains the network; one script for all three methods
- `Code/fig_input.py`: figure of what the network sees (image, pixels, input, target)
- `Code/fig_results.py`: figures of test error, error signal angle, and example guesses
- `Code/make_slides.py`: builds the presentation slides
- `Data/MNIST/`: the MNIST dataset (gzip files)
- `Results/`: trained weights (`.npz`) and training logs (`.log`)
- `Figures/`: all figures

## How to run

```bash
python Code/mnist_fa.py bp 20 0.1 2
python Code/mnist_fa.py fa 20 0.1 2
python Code/mnist_fa.py shallow 20 0.1 2
python Code/fig_results.py
```

Arguments: method (`bp`, `fa` or `shallow`), number of epochs, learning rate, range of the random feedback matrix B.

Needs `numpy` and `matplotlib`. `make_slides.py` also needs `python-pptx` and the course slide template.

## Team

Wenrui Chen, Chengweiran Liu, Xianchen Fang
