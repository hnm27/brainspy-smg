import os
import numpy as np
import matplotlib.pyplot as plt

import torch
from brainspy.utils.waveform import WaveformManager


def plot_error_hist(targets: np.array,
                    prediction: np.array,
                    error: np.array,
                    mse: np.array,
                    save_dir: str,
                    name: str = "error") -> None:
    """
    Plots and saves error histogram graph for between given target and predicted.

    Parameters
    ----------
    targets : np.array
        Reference data used for training/validation.
    prediction : np.array
        Predictions made by model.
    error : np.array
        Errors correspoding to each target data point.
    mse : np.array
        Mean squared error correspoding to each target data point.
    save_dir : str
        Name of the path where the graph is to be saved.
    name : str [Optional]
        Name of the file for the graph.
    """
    plt.figure()
    plt.title('Predicted vs True values')
    plt.subplot(1, 2, 1)
    plt.plot(targets, prediction, ".")
    plt.xlabel("True Output (nA)")
    plt.ylabel("Predicted Output (nA)")
    targets_and_prediction_array = np.concatenate((targets, prediction))
    min_out = np.min(targets_and_prediction_array)
    max_out = np.max(targets_and_prediction_array)
    plt.plot(np.linspace(min_out, max_out), np.linspace(min_out, max_out), "k")
    plt.title(f"RMSE {np.sqrt(mse)} (nA)")
    plt.subplot(1, 2, 2)
    plt.hist(np.reshape(error, error.size), 500)
    x_lim = 0.25 * np.max([np.abs(error.min()), error.max()])
    plt.xlim([-x_lim, x_lim])
    plt.title("Error histogram (nA) ")
    fig_loc = os.path.join(save_dir, name)
    plt.tight_layout()
    plt.savefig(fig_loc, dpi=300)
    plt.close()


def plot_error_vs_output(targets: np.array,
                         error: np.array,
                         save_dir: str,
                         name: str = "error_vs_output") -> None:
    """
    Plots and saves error vs output graph for given error and their
    correspoding output.

    Parameters
    ----------
    targets : np.array
        Reference data used for training/validation.
    error : np.array
        Errors correspoding to each target data point.
    save_dir : str
        Name of the path where the graph is to be saved.
    name : str [Optional]
        Name of the file for the graph.
    """
    plt.figure()
    plt.plot(targets, error, ".")
    plt.plot(
        np.linspace(
            targets.min(),
            targets.max(),
            len(error),
        ),
        np.zeros_like(error),
    )
    plt.title("Error vs Output")
    plt.xlabel("Output (nA)")
    plt.ylabel("Error (nA)")
    fig_loc = os.path.join(save_dir, name)
    plt.savefig(fig_loc, dpi=300)
    plt.close()


def plot_waves(inputs: np.array, outputs: np.array, input_no: int,
               output_no: int, batch: int, legend: np.array,
               save_directory: str) -> None:
    """
    Plots and saves input and output waves for the model. Image is overwritten 
    for each batch and it is used to control what is happening to the device
    input output relationship for each batch.

    Parameters
    ----------
    inputs : np.array
        Input data used for training/validation of model.
    outputs : np.array
        Output generated by model corresponding the inputs.
    input_no : int
        Input activation electrode number.
    output_no : int
        Output electrode number.
    batch : int
        The current batch number of the data.
    legend : np.array
        List of headers of text file which contains data used
        for training, validation, and testing.
    save_directory : str
        Name of the file for the graph.
    """
    plt.figure()
    plt.suptitle(f'I/O data for batch {batch}')
    plt.subplot(211)
    plt.plot(inputs)
    plt.ylabel('Inputs (V)')
    plt.xlabel('Time points (a.u.)')
    plt.legend(legend[:input_no])
    plt.subplot(212)
    plt.plot(outputs)
    plt.ylabel('Outputs (nA)')
    plt.legend(legend[-output_no:])
    plt.xlabel('Time points (a.u.)')
    plt.tight_layout()
    plt.savefig(os.path.join(save_directory, 'example_batch'))
    plt.close()


def output_hist(outputs: np.array,
                data_dir: str,
                bins: int = 100,
                show: bool = False) -> None:
    """
    Saves and optionally plots the histogram of output/predictions
    of the model.

    Parameters
    ----------
    outputs : np.array
        Output generated by model.
    data_dir : str
        Name of the path where the graph is to be saved.
    bins : int [Optional]
        Number of bins for the histogram.
    show : bool [Optional]
        If set to true, it displays the generated histogram.
    """
    plt.figure()
    plt.title("Output Histogram")
    plt.hist(outputs, bins=bins)
    plt.ylabel("Counts")
    plt.xlabel("Raw output (nA)")
    if show:
        plt.show()
    plt.savefig(data_dir + "/output_distribution")
    plt.close()


# def plot(self, x, y):
#     for i in range(np.shape(y)[1]):
#         plt.figure()
#         plt.plot(x)
#         plt.plot(y)
#         plt.show()


def iv_plot(result: np.array,
            input_electrode: int,
            save_plot: bool = None,
            show_plot: bool = False) -> None:
    """
    Plots IV characteristics and optinally saves the graph
    for a given electrode number.

    Parameters
    ----------
    result : np.array
        Output current values of an electrode.
    input_electrode : int
        Electrode number.
    save_plot : bool [Optional]
        If set to true, it saves the generated plot to
        current directory.
    show_plot : bool [Optional]
        If set to true, it displays the generated plot.
    """
    plt.plot(result, label='IV Curve for electrode ' + str(input_electrode))
    plt.xlabel('Point no.')
    plt.ylabel('Current (nA)')
    if save_plot is not None:
        plt.savefig(save_plot)
    if show_plot:
        plt.show()


def multi_iv_plot(configs, inputs, output):
    """
    Plots the IV curve of several devices in one plot. Devices can be the DNPU
    device or a surrogate model.

    Parameters
    ----------
    configs : dict
        Dictionary containing the configurations for IV measurements with
        the following keys:
        - devices: list
            List of devices for which IV response is to be computed. This list
            contains the names of all the devices (A,B,C,D etc) involved in the
            experiment.
        - driver: dict
            It contains the configurations for each device in the experiment which
            are defined in the devices list.
    inputs : dict
        Dictionary containing the list of input signal waves for each device.
    outputs : dict
        Dictionary containing the list of output currents for each device.
    """
    ylabeldist = -10
    electrode_id = 0
    cmap = plt.get_cmap("tab10")
    for k, dev in enumerate(configs['devices']):
        fig, axs = plt.subplots(2, 4)
        # plt.grid(True)
        fig.suptitle('Device ' + dev + ' - Input voltage vs Output current')
        for i in range(2):
            for j in range(4):
                exp_index = j + i * 4
                exp = "IV" + str(exp_index + 1)
                if exp_index < 7:
                    if configs["driver"]['instruments_setup'][dev][
                            "activation_channel_mask"][exp_index] == 1:
                        masked_idx = sum(
                            configs["driver"]['instruments_setup'][dev]
                            ["activation_channel_mask"][:exp_index + 1]) - 1
                        # Modifying x-axis
                        temp = inputs[exp][dev][masked_idx]
                        if not configs['driver']['instruments_setup']['average_io_point_difference']:
                            wm = WaveformManager(
                                {'slope_length':0, 'plateau_length': int(configs['driver']['instruments_setup']['readout_sampling_frequency']/configs['driver']['instruments_setup']['activation_sampling_frequency'])})
                            temp = wm.points_to_plateaus(torch.tensor(inputs[exp][dev][masked_idx])).detach().cpu().numpy()
                        axs[i, j].plot(temp,
                                       output[exp][dev],
                                       color=cmap(exp_index))
                        axs[i, j].set_ylabel('output (nA)',
                                             labelpad=ylabeldist)
                        axs[i, j].set_xlabel('input (V)', labelpad=1)
                        axs[i, j].xaxis.grid(True)
                        axs[i, j].yaxis.grid(True)
                    else:
                        # if self.configs["driver"]['instruments_setup'][
                        #         dev]["activation_channel_mask"][
                        #             exp_index] == 1:
                        #     axs[i,
                        #         j].plot(input_waveform[exp_index]
                        #                 [:, electrode_id])

                        #     axs[i, j].set_title(
                        #         devlist[dev]["activation_channels"]
                        #         [exp_index])
                        axs[i, j].plot([])
                        axs[i, j].set_xlabel('Channel Masked')
                    electrode_id += 1
                else:
                    for z, key in enumerate(inputs.keys()):
                        m = 0
                        if configs["driver"]['instruments_setup'][dev][
                                "activation_channel_mask"][z] == 1:
                            masked_idx = sum(
                                configs["driver"]['instruments_setup'][dev]
                                ["activation_channel_mask"][:z + 1]) - 1
                            temp = inputs[key][dev][masked_idx]
                            if not configs['driver']['instruments_setup']['average_io_point_difference']:
                                wm = WaveformManager({'slope_length':0, 'plateau_length': int(configs['driver']['instruments_setup']['readout_sampling_frequency']/configs['driver']['instruments_setup']['activation_sampling_frequency'])})
                                temp =  wm.points_to_plateaus(torch.tensor(inputs[key][dev][masked_idx])).detach().cpu().numpy()[int(configs['driver']['instruments_setup']['readout_sampling_frequency']/configs['driver']['instruments_setup']['activation_sampling_frequency']):]
                            axs[i, j].plot(temp,
                                           label="IV" + str(z),
                                           color=cmap(z))
                            m += 1
                    #axs[i, j].yaxis.tick_right()
                    #axs[i, j].yaxis.set_label_position("right")
                    axs[i, j].set_ylabel('input (V)')
                    axs[i, j].set_xlabel('points', labelpad=1)
                    axs[i, j].set_title("Input input_signal")
                    axs[i, j].xaxis.grid(True)
                    axs[i, j].yaxis.grid(True)
                    axs[i, j].legend()
    plt.subplots_adjust(hspace=0.3, wspace=0.35)
    plt.show()
