import tensorflow as tf
import time, os
import numpy as np 

def get_unique_filename(filename):
    time_stamp = time.asctime().replace(" ", "_").replace(":", "_")
    unique_filename  = f"{time_stamp}_{filename}"
    return unique_filename
    

def get_callbacks (X_train, es_patience, callbacked_model_name ,model_ckpt_path, TENSORBOARD_ROOT_LOG_DIR):
    #Tensorboard Callback 
    tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir = TENSORBOARD_ROOT_LOG_DIR)
    file_writer = tf.summary.create_file_writer(logdir=TENSORBOARD_ROOT_LOG_DIR)

    with file_writer.as_default():
        images = np.reshape(X_train[10:30], (-1, 28, 28, 1))
        tf.summary.image("20 handwritten digit samples", images, max_outputs=25, step=0)
    #Early stopping callback
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(patience=es_patience, restore_best_weights=True)
    #Model Checkpointing callback (Helpful in backup, would save the last checkpoint in crashing)
    CKPT_name = get_unique_filename(callbacked_model_name)
    CKPT_path = os.path.join( model_ckpt_path ,CKPT_name)
    checkpointing_cb = tf.keras.callbacks.ModelCheckpoint(CKPT_path , save_best_only=True)
    return early_stopping_cb, checkpointing_cb, tensorboard_cb