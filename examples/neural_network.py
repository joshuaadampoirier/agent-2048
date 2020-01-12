import numpy as np 

from representations.neural_network import NeuralNetworkRepresentation

def main():
    """
    Build a neural network representation.

    Parameters
    ----------
        None

    Returns
    -------
        0
    """

    # follow stevenmiller888.github.io/mind-how-to-build-a-neural-network to 
    # force inputs, weights to ensure we're calculating outputs correctly
    nn = NeuralNetworkRepresentation(
        n_i=2, 
        n_h=3, 
        n_o=1, 
        initialize=False, 
        normalize_input=False
    )

    # manually update with some weights and biases
    W_i_h = np.array([[0.8, 0.4, 0.3], [0.2, 0.9, 0.5]])
    b_i_h = np.array([0, 0, 0])
    W_h_o = np.array([[0.3], [0.5], [0.9]])
    b_h_o = np.array([0])
    nn.update_parameters(W_i_h, b_i_h, W_h_o, b_h_o)

    # feed-forward to get network response
    result = nn.feed_forward(np.array([1, 1]))
    print('Result: {}'.format(result))

    return 0


if __name__ == '__main__':
    main()