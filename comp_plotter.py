import os
import pandas as pd
import matplotlib.pyplot as plt

def process_single_run(experiment_dir, enemy, run_num):
    # Generate the filenames based on the naming convention
    comp_filename = f'comp-data-{enemy}-{run_num}.csv'

    comp_filepath = os.path.join(experiment_dir, comp_filename)

    if os.path.exists(comp_filepath):
        # Read the CSV file for computer data
        comp_data = pd.read_csv(comp_filepath)

        # Group data by generation and calculate cumulative time
        comp_data['cumulative_time'] = comp_data['time'].cumsum()

        # Calculate mean values for CPU and memory
        comp_data_mean = comp_data.groupby('generation').agg({
            'cumulative_time': 'last',  # Get the cumulative time for the last row in each generation
            'cpu_usage_percent': 'mean',
            'memory_usage_MB': 'mean'
        })

        return comp_data_mean

def process_all_runs(experiment_dir, enemy, num_runs):
    avg_comp_data = None

    for run_num in range(num_runs):
        comp_data_mean = process_single_run(experiment_dir, enemy, run_num)

        if comp_data_mean is not None:
            if avg_comp_data is None:
                avg_comp_data = comp_data_mean
            else:
                avg_comp_data += comp_data_mean

    if avg_comp_data is not None:
        avg_comp_data /= num_runs

    return avg_comp_data

def plot_average_data(avg_comp_data1, avg_comp_data2, label1, label2):
    # Create subplots for CPU usage, memory usage, and cumulative time
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

    # Set smaller subplot titles
    fig.suptitle('Comparison of Experiments', fontsize=12)

    # Plot CPU usage
    ax1.plot(avg_comp_data1.index, avg_comp_data1['cpu_usage_percent'], label=f'{label1}')
    ax1.plot(avg_comp_data2.index, avg_comp_data2['cpu_usage_percent'], label=f'{label2}')
    ax1.set_ylabel('CPU Usage (%)')
    ax1.grid(True)
    ax1.legend(fontsize='small')  # Make the legend smaller

    # Plot memory usage
    ax2.plot(avg_comp_data1.index, avg_comp_data1['memory_usage_MB'], label=f'{label1}', color='orange')
    ax2.plot(avg_comp_data2.index, avg_comp_data2['memory_usage_MB'], label=f'{label2}', color='green')
    ax2.set_ylabel('Memory Usage (MB)')
    ax2.grid(True)
    ax2.legend(fontsize='small')  # Make the legend smaller

    # Plot cumulative time
    ax3.plot(avg_comp_data1.index, avg_comp_data1['cumulative_time'], label=f'{label1}', color='red')
    ax3.plot(avg_comp_data2.index, avg_comp_data2['cumulative_time'], label=f'{label2}', color='blue')
    ax3.set_xlabel('Generation')
    ax3.set_ylabel('Cumulative Time (s)')
    ax3.legend(fontsize='small')  # Make the legend smaller

    plt.grid(True)
    plt.show()

def process_and_plot_multiple_experiments(experiment_dirs, num_runs, enemies):
    avg_comp_data1 = process_all_runs(experiment_dirs[0], enemies[0], num_runs)
    avg_comp_data2 = process_all_runs(experiment_dirs[1], enemies[1], num_runs)
    plot_average_data(avg_comp_data1, avg_comp_data2, experiment_dirs[0], experiment_dirs[1])

if __name__ == '__main__':
    experiment_dirs = ['Enemy 7 flexible structure', 'Enemy 7 fixed structure']  # Replace with your experiment directories
    enemies = [7, 7]  # Set to the enemies you want to analyze for each experiment
    num_runs = 10  # Replace with the number of runs you have

    process_and_plot_multiple_experiments(experiment_dirs, num_runs, enemies)