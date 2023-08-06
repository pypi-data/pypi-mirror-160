
__module_name__ = "_potential_net.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# import packages #
# --------------- #
import torch


# import local dependencies #
# ------------------------- #
from ._compose_nn_sequential import _compose_nn_sequential

def _potential_net(
    in_dim=50,
    out_dim=1,
    activation_function=torch.nn.Tanh(),
    hidden_layer_nodes={1: [400, 400]},
    dropout=True,
    dropout_probability=0.1,
):
    """
    MLP (multi-layer perceptron) neural network that outputs a single parameter.
    
    Parameters:
    -----------
    in_dim
        input dimension
        default: 50
        type: int
        
    out_dim
        output dimension
        default: 1
        type: int
        
    activation_function
        default: torch.nn.Tanh()
        type: torch.nn.modules
        
    hidden_layer_nodes
        default: {1: [400, 400]}
        type: dict
        
    dropout
        Boolean indicator of dropout inclusion.
        default: True
        type: bool
        
    dropout_probability
        default: 0.01
        type: float

    Returns:
    --------
    potential_net
        A neural network that outputs a single parameter (i.e., a multi-layer perceptron).
        type: torch.nn.modules.container.Sequential

        
    Notes:
    ------
    
    """
    return _compose_nn_sequential(
        in_dim=in_dim,
        out_dim=out_dim,
        activation_function=activation_function,
        hidden_layer_nodes=hidden_layer_nodes,
        dropout=dropout,
        dropout_probability=dropout_probability,
    )
