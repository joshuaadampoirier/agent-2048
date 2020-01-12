import numpy as np 

from representations.base import BaseRepresentation


class NeuralNetworkRepresentation(BaseRepresentation):
    """
    Class for the simple neural network representation. 
    
    Notes
    -----
    Here, we define the simple neural network as a single fully-connected hidden 
    layer implemented with NumPy.

    Parameters
    ----------
    n_i:        integer, default 16
                number of inputs to the network

    n_h:        integer, default 24
                number of hidden nodes in the network

    n_o:        integer, default 4
                number of outputs produced by the network

    activation: string, default sigmoid
                type of activation function to use

    seed:       integer, default 1234
                Seed for the random number generator.

    initialize: bool, default True
                Whether or not to initialize the weights and biases upon
                construction.

    normalize:  bool, default True
                Whether or not to normalize the inputs. This is useful for 
                testing the neural network structure as we can force inputs 
                through.
    """
    def __init__(self, 
                 n_i=16, 
                 n_h=24, 
                 n_o=4, 
                 activation='sigmoid',
                 seed=1234, 
                 initialize=True,
                 normalize_input=True):
        self.n_i = n_i 
        self.n_h = n_h 
        self.n_o = n_o 
        self.seed = seed 

        # initialize weights and biases
        self.W_i_h = np.empty((n_i, n_h))
        self.b_i_h = np.empty(n_h)
        self.W_h_o = np.empty((n_h, n_o))
        self.b_h_o = np.empty(n_o)

        # softmax activation function 
        if activation == 'softmax':
            self.activation_function = lambda x: np.exp(x) / np.sum(np.exp(x))
        elif activation == 'sigmoid':
            self.activation_function = lambda x: 1 / (1 + np.exp(-x))
        elif activation == 'relu':
            self.activation_function = lambda x: np.max(0, x)

        # initialize if indicated
        if initialize == True:
            self.initialize()

        # whether or not input data needs to be normalized
        self.normalize_input = normalize_input 

    def initialize(self):
        """
        Initialize the weights and biases with random numbers.

        Parameters
        ----------
        None 

        Returns
        -------
        None 
        """
        # seed the random number generator ensuring reproducibilty
        np.random.seed(self.seed)

        # weights from input layer to hidden layer
        self.W_i_h = np.random.normal(
            0.0, 
            self.n_i ** -0.5, 
            self.W_i_h.shape
        )

        # biases from input layer to hidden layer
        self.b_i_h = np.random.normal(
            0.0,
            self.n_i ** -0.5,
            self.b_i_h.shape
        )

        # weights from hidden layer to output layer
        self.w_h_o = np.random.normal(
            0.0,
            self.n_h ** -0.5,
            self.W_h_o.shape
        )

        # biases from hidden layer to output layer 
        self.b_h_o = np.random.normal(
            0.0,
            self.n_h ** -0.5,
            self.b_h_o.shape 
        )

    def update_parameters(self, W_i_h, b_i_h, W_h_o, b_h_o):
        """
        Manually update parameters from the network.

        Parameters
        ----------
        W_i_h:  NumPy array or None, size of the networks current W_i_h array
                Weights between input and hidden layers.

        b_i_h:  NumPy array or None, size of networks current b_i_h array
                Biases between input and hidden layers.

        W_h_o:  NumPy array or None, size of networks current W_h_o array
                Weights between hidden and output layers.

        b_h_o:  NumPy array or None, size of networks current b_h_o array
                Biases between hidden and output layers.
        """
        # if given and appropriate shape, update input-to-hidden weights
        if W_i_h is not None and W_i_h.shape == self.W_i_h.shape:
            self.W_i_h = W_i_h 

        # if given and appropriate shape, update input-to-hidden biases
        if b_i_h is not None and b_i_h.shape == self.b_i_h.shape:
            self.b_i_h = b_i_h 

        # if given and appropriate shape, update hidden-to-output weights 
        if W_h_o is not None and W_h_o.shape == self.W_h_o.shape:
            self.W_h_o = W_h_o 

        # if given and appropriate shape, update hidden-to-output biases
        if b_h_o is not None and b_h_o.shape == self.b_h_o.shape:
            print(b_h_o)
            self.b_h_o = b_h_o 

    def feed_forward(self, x):
        """
        Feed a given set of inputs through the network.

        Parameters
        ----------
        x:      NumPy array, size of input layer
                These are the raw inputs to the network.

        o_o:    Numpy array, size of output layer
                These are the calculated outputs from the feed-forward 
                calculation. A softmax has been applied to convert them to
                probabilities.
        """
        # normalize the input layer
        if self.normalize_input == True:
            i = self.normalize(x)
        else: 
            i = x

        # calculate the hidden layer inputs and outputs
        h_i = np.dot(i, self.W_i_h + self.b_i_h)
        h_o = self.activation_function(h_i)

        # calculate the inputs to the output layer
        o_i = np.dot(h_o, self.W_h_o + self.b_h_o)
        o_o = self.activation_function(o_i)

        return o_o