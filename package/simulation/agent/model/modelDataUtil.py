"""Data util for the models.
"""
import tensorflow as tf
import pandas as pd


def generateInputFunction(input_df: pd.DataFrame, expected_output_df=None, num_epochs=1, shuffle=True, batch_size=32):
    """Generates input function for the tensorflow models.

    Args:
        input_df (pd.DataFrame):
        expected_output_df (pd.DataFrame):
        num_epochs (int):
        shuffle (bool):
        batch_size (int):
    :return:
    """
    def input_function():
        if expected_output_df is not None:
            slices = (dict(input_df), expected_output_df)
        else:
            slices = dict(input_df)
        dataset = tf.data.Dataset.from_tensor_slices(slices)
        if shuffle:
            dataset = dataset.shuffle(100)
        ds = dataset.batch(batch_size).repeat(num_epochs)
        return ds
    return input_function
