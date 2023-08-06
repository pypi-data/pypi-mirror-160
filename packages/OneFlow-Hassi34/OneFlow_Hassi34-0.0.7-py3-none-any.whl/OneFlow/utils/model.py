"""
Author : Hasnain Mehmood
Contact : hasnainmehmood3435@gmail.com 
"""

import tensorflow as tf 
import time
import os
import matplotlib.pyplot as plt
import pandas as pd
from OneFlow.utils.callbacks import get_callbacks


def get_unique_filename(filename):
    time_stamp = time.asctime().replace(" ", "_").replace(":", "_")
    unique_filename  = f"{time_stamp}_{filename}"
    return unique_filename
class StepFlow:
    """ This class shall be used to train an end to end ANN model with callback
        Written by : Hasnain
    """
    def __init__(self,config, X_train, y_train, X_valid, y_valid):
        self.config = config
        self.LOSS_FUNCTION = config["params"]["loss_function"]
        self.OPTIMIZER = config['params']['optimizer']
        self.METRICS = config["params"]["metrics"]
        self.NUM_CLASSES = config["params"]["num_classes"]
        self.EPOCHS = config['params']["epochs"]
        self.ES_PATIENCE = config['params']['es_patience']
        self.VALIDATION_SET = (X_valid, y_valid)
        self.X_train = X_train
        self.y_train = y_train
        self.model_ckpt_dir = config['artifacts']['model_ckpt_dir']
        self.artifacts_dir = config["artifacts"]["artifacts_dir"]
        self.model_dir = config["artifacts"]["model_dir"]
        self.model_name = config['artifacts']['model_name']
        self.callbacked_model_name = config['artifacts']['callbacked_model_name']
        self.plots_dir = config["artifacts"]["plots_dir"]
        self.plot_name = config["artifacts"]["plot_name"]
        self.logs = config["logs"]
        self.tensorboard_root_log_dir = config["logs"]["tensorboard_root_log_dir"]

    def create_model(self):
        """This method will get the variables initialized with class 
            And will provide the model architecture for next methods
            Written by : Hasnain
        """

        LAYERS = [
            tf.keras.layers.Flatten(input_shape = [28, 28], name = "inputLayer"),
            tf.keras.layers.Dense(300, activation = "relu", name = "hiddenLayer1"),
            tf.keras.layers.Dense(100, activation = "relu", name = "hiddenLayer2"),
            tf.keras.layers.Dense(self.NUM_CLASSES, activation = "softmax", name = "OutputLayer")
        ]
        
        self.model = tf.keras.models.Sequential(LAYERS)
        self.model.summary()
        self.model.compile(
            loss = self.LOSS_FUNCTION,
            optimizer = self.OPTIMIZER,
            metrics = self.METRICS
        )
        #<< untrained model

    def fit_model(self):
        """This method will perform the operation on data and model architecture
            and will provide the trained model with call backs
           Written by : Hasnain
        """
        TENSORBOARD_ROOT_LOG_DIR = os.path.join(self.logs["logs_dir"], self.tensorboard_root_log_dir)
        os.makedirs(TENSORBOARD_ROOT_LOG_DIR, exist_ok=True) 
        model_ckpt_path = os.path.join(self.artifacts_dir,self.model_dir, self.model_ckpt_dir)
        os.makedirs(model_ckpt_path, exist_ok=True)
        early_stopping_cb, checkpointing_cb, tensorboard_cb = get_callbacks(self.X_train, self.ES_PATIENCE, self.callbacked_model_name, model_ckpt_path, TENSORBOARD_ROOT_LOG_DIR)
        self.history = self.model.fit(self.X_train, self.y_train, epochs=self.EPOCHS, validation_data = self.VALIDATION_SET, callbacks = [tensorboard_cb , early_stopping_cb, checkpointing_cb])

    def save_final_model(self):
        """This method with create the "models" directory
            and will save trained model in that
            Written by : Hasnain
        """
        model_dir_path = os.path.join(self.artifacts_dir,self.model_dir, get_unique_filename("tb_logs"))
        os.makedirs(model_dir_path, exist_ok = True)
        unique_filename = get_unique_filename(self.model_name)
        path_to_model = os.path.join(model_dir_path, unique_filename)
        self.model.save(path_to_model)

    def save_plot(self):
        """This method will create the plots of defined evaluation metrics 
           and will save the plots in "plots" directory
            Written by : Hasnain
        """

        plots_dir_path = os.path.join(self.artifacts_dir, self.plots_dir )
        os.makedirs(plots_dir_path, exist_ok=True)
        
        unique_filename = get_unique_filename(self.plot_name)
        path_to_plot = os.path.join(plots_dir_path, unique_filename)
        pd.DataFrame(self.history.history).plot(figsize= (8,5))
        plt.grid(True)
        plt.gca().set_ylim(0,1)
        plt.savefig(path_to_plot)

