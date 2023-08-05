import numpy as np
import pandas as pd
import random

from .resample_by_blocks import random_resample_data_by_blocks
from scipy.optimize import curve_fit
from tqdm import tqdm


def power_law(time_interval, population_growth_rate, initial_population_size):
    """This function represent a simple power law of the type: f(y) = a*x^y

    Args:
        time_interval (array): Time vector
        population_growth_rate (array): Population growth rate parameter
        initial_population_size (int): Initial population size

    Returns:
        [ndarray]: Population growth in time interval
    """
    return initial_population_size * np.power(population_growth_rate, time_interval)


def lambda_calculator(
    temporadas, maximo_nidos, max_iter=10000, lower_bounds=0, lambda_upper_bound=50
):
    """This function represent fit a power law to seasons and burrows quantity data and return lambda coefficient

    Args:
        temporadas (List or ndarray): List or array of seasons.
        maximo_nidos (List or ndarray): List or array of burrows quantity per seasons.
        max_iter (int, optional): Number of bootstrap repetitions. Defaults to 10000.
        lower_bounds (int, optional): Min lambda coefficient. Defaults to 0.
        lambda_upper_bound (int, optional):  Max lambda coefficient. Defaults to 50.

    Returns:
        [ndarray]: The coefficients array for power_law (N0,lamda).
    """
    temporadas = np.array(temporadas)
    numero_agno = temporadas - temporadas[0]
    maximo_nidos = np.array(maximo_nidos)
    popt, _ = curve_fit(
        power_law,
        numero_agno,
        maximo_nidos,
        maxfev=max_iter,
        bounds=((lower_bounds, lower_bounds), (lambda_upper_bound, np.inf)),
    )
    return popt


def remove_distribution_outliers(data, number_of_std=2.698):
    """Remove outliers from distribution using the standard deviation and a range

    Args:
        data (List or ndarray): Distribution samples to be filteredled
        number_of_std (float, optional): Amplitude of filter based on standard deviation units. Defaults to 2.698 std.

    Returns:
        [ndarray]: Numpy array with the filtered data.
    """
    data = np.array(data)
    mean = np.mean(data)
    std = np.std(data)
    mask = abs(data - mean) <= std * number_of_std
    return data[mask]


def tukey_fences(data, fence_width=1.5):
    """Filter an array using Tukey fences method

    Args:
        data (List or ndarray): Distribution samples to be filteredled
        fence_width (float, optional):  Amplitude of filter in IQR units. Defaults to 1.5.

    Returns:
        [ndarray]: Numpy array with the filtered data.
    """
    data = np.array(data)
    first_quantile = np.quantile(data, 0.25)
    third_quantile = np.quantile(data, 0.75)
    interquartile_range = third_quantile - first_quantile
    lower_limit = first_quantile - (interquartile_range * fence_width)
    upper_limit = third_quantile + (interquartile_range * fence_width)
    mask = (lower_limit <= data) & (data <= upper_limit)
    return data[mask]


def seasons_from_date(data):
    """Extract years from string date format: dd/mm/aaaa.

    Args:
        data (DataFrame): Dataframe with the column "Fecha" in format dd/mm/aaaa.

    Returns:
        [ndarray]: Numpy array with the years: aaaa
    """
    seasons = data["Fecha"].str.split("/", n=2, expand=True)
    return np.array(seasons[2])


def boostrapping_feature(data, number_sample=2000):
    """Generate boostrapping distribution from sample data.

    Args:
        data (List or ndarray): Data sample you want to bootstrap
        number_sample (int, optional): Number of bootstrap samples you want. Defaults to 2000.

    Returns:
        [List]: Bootstrap distribution from sample data
    """
    dataframe = pd.DataFrame(data)
    bootstrap_data = []
    for i in range(number_sample):
        resampled_data = dataframe.sample(n=1, random_state=i)
        bootstrap_data.append(resampled_data.iloc[0][0])
    return bootstrap_data


def lambdas_from_bootstrap_table(dataframe, remove_outliers=True, outlier_method="tukey", **kwargs):
    """Calculate bootstrap distributions without outliers for lambda coefficient in population growth model from bootstrapped samples per season.

    Args:
        dataframe (DataFrame): DataFrame with "Years" in columns and the bootstrap samples in the rows. (GECI-Bootstrap con R).
        remove_outliers (bool, optional): True if you want filter your final distribution. Defaults to True.
        outlier_method (str, optional): Method to use to filter, available methods are "tukey" and "std" . Defaults to "tukey".

    Returns:
        [ndarray]: Filtered bootstrap distribution for lambdas coefficient.
    """
    lambdas_bootstraps = []
    seasons = np.array(dataframe.columns.values, dtype=int)
    N = len(dataframe)
    print("Calculating bootstrap growth rates distribution:")
    for i in tqdm(range(N)):
        fitting_result = lambda_calculator(seasons, dataframe.T[i].values)
        lambdas_bootstraps.append(fitting_result[0])
    if remove_outliers:
        lambdas_bootstraps = remove_outlier(outlier_method, lambdas_bootstraps, **kwargs)
    return lambdas_bootstraps


def lambdas_bootstrap_from_dataframe(
    dataframe,
    column_name,
    N=2000,
    return_distribution=False,
    remove_outliers=True,
    outlier_method="tukey",
    **kwargs,
):
    """Calculate bootstrap 95% intervals for lambda coefficient in population growth model from DataFrame with seasons and burrows quantity
    data.

    Args:
        dataframe (DataFrame): DataFrame with column "Temporada" and "column_name" is the burrows quantity.
        column_name (string): Name of the column in the DataFrame to fit the model.
        N (int, optional): Number of bootstrap samples you want. Defaults to 2000.
        return_distribution (bool, optional): True if you want the bootstrap distribution. Defaults to False.
        remove_outliers (bool, optional): True if you want filter your final distribution. Defaults to True.
        outlier_method (str, optional): Method to use to filter, available methods are "tukey" and "std" . Defaults to "tukey".

    Returns:
        [ndarray]: 95% bootstrap interval for lambda coefficient. The interval is conformed by 2.5, 50 and 97.5 percentiles in an Numpy array.
        If `return_distribution` is True, returns the distribution too.
    """
    bootstraped_data = pd.DataFrame()
    lambdas_bootstraps = []
    seasons = dataframe.sort_values(by="Temporada").Temporada.unique()
    print("Calculating samples per season:")
    for season in tqdm(seasons):
        data_per_season = dataframe[dataframe.Temporada == season]
        bootstraped_data[season] = boostrapping_feature(data_per_season[column_name], N)
    lambdas_bootstraps = lambdas_from_bootstrap_table(bootstraped_data)
    if remove_outliers:
        lambdas_bootstraps = remove_outlier(outlier_method, lambdas_bootstraps, **kwargs)
    if return_distribution:
        return lambdas_bootstraps, np.percentile(lambdas_bootstraps, [2.5, 50, 97.5])
    return np.percentile(lambdas_bootstraps, [2.5, 50, 97.5])


def get_bootstrap_interval(bootstrap_distribution, **kwargs):
    """Generate bootstrap interval differences for reports from 95% bootstrap interval array (2.5, 50 and 97.5 percentiles).

    Args:
        bootstrap_distribution (ndarray): 95% bootstrap interval array.

    Returns:
        [List]: bootstrap interval differences
    """
    inferior_limit = np.around(bootstrap_distribution[1] - bootstrap_distribution[0], **kwargs)
    superior_limit = np.around(bootstrap_distribution[2] - bootstrap_distribution[1], **kwargs)
    bootstrap_distribution = np.around(bootstrap_distribution, **kwargs)
    return [inferior_limit, bootstrap_distribution[1], superior_limit]


def bootstrap_from_time_series(
    dataframe,
    column_name,
    N=2000,
    return_distribution=False,
    remove_outliers=True,
    outlier_method="tukey",
    blocks_length=2,
    **kwargs,
):
    """Calculate 95% bootstrap intervals for lambda coefficient in population growth model from timeseries data.

    Args:
        dataframe (DataFrame): DataFrame with the columns "Temporada" with the seasons, and "column_name" with the values of the time serie.
        column_name (string): Name of the column in the DataFrame to fit the model.
        N (int, optional): Number of bootstrap samples you want. Defaults to 2000.
        return_distribution (bool, optional): True if you want the bootstrap distribution. Defaults to False.
        remove_outliers (bool, optional): True if you want filter your final distribution. Defaults to True.
        outlier_method (str, optional): Method to use to filter, available methods are "tukey" and "std" . Defaults to "tukey".
    Returns:
        [ndarray]: 95% bootstrap interval for lambda coefficient. The interval is conformed by 2.5, 50 and 97.5 percentiles in an Numpy array.
        If `return_distribution` is True, returns the distribution too.
    """
    lambdas_bootstraps = []
    cont = 0
    rand = 0
    print("Calculating bootstrap growth rates distribution:")
    while cont < N:
        resampled_data = resample_data(dataframe, rand, blocks_length)
        try:
            fitting_result = lambda_calculator(
                resampled_data["Temporada"], resampled_data[column_name]
            )
        except RuntimeError:
            rand += 1
            continue
        lambdas_bootstraps.append(fitting_result[0])
        cont += 1
        rand += 1
    if remove_outliers:
        lambdas_bootstraps = remove_outlier(outlier_method, lambdas_bootstraps, **kwargs)
    if return_distribution:
        return lambdas_bootstraps, np.percentile(lambdas_bootstraps, [2.5, 50, 97.5])
    return np.percentile(lambdas_bootstraps, [2.5, 50, 97.5])


def resample_data(dataframe, seed, blocks_length):
    random.seed(seed)
    return random_resample_data_by_blocks(dataframe, blocks_length)


def calculate_p_values(distribution):
    """Calculate p-values based on proportion of samples greater than 1, and below 1.0

    Args:
        distribution (List or ndarray): List or Numpy array with the distribution

    Returns:
        (float,float): proportion below 1, proportion grater than 1
    """
    distribution = np.array(distribution)
    mask = distribution < 1
    mask2 = distribution > 1
    return mask.sum() / len(distribution), mask2.sum() / len(distribution)


def generate_latex_interval_string(intervals, **kwargs):
    """Genetare string for 95% interval in equation latex notation from 95% bootstrap interval array.

    Args:
        intervals (List or ndarray): 95% bootstrap interval array (2.5, 50 and 97.5 percentiles).

    Returns:
        [string]: Interval equation string format for latex.
    """
    lower_limit, central, upper_limit = get_bootstrap_interval(intervals, **kwargs)
    return f"${{{central}}}_{{-{lower_limit}}}^{{+{upper_limit}}}$"


def mean_bootstrapped(data, N=2000):
    """Calculate means bootstrapped distribution from some data.

    Args:
        data (List or ndarrray): Data samples from you want to calculate the bootstrap distribution for the mean.
        N (int, optional): Number of bootstrap samples. Defaults to 2000.

    Returns:
        [ndarray]: Bootstrap distribution for the mean.
    """
    dataframe = pd.DataFrame(data)
    bootstrap_mean = []
    for i in range(N):
        resampled_data = dataframe.sample(n=len(dataframe), random_state=i, replace=True)
        bootstrap_mean.append(np.mean(resampled_data))
    return np.squeeze(bootstrap_mean)


def remove_outlier(method, data, **kwargs):
    """Select method to filter the outliers in data.

    Args:
        method (string): Method to use to filter, available methods are "tukey" and "std" . Defaults to "tukey".
        data (List or ndarray): Distribution to be filtered by the method selected.
        **kwargs: Arguments for the filter method.
    Returns:
        [ndarray]: data filtered.
    """
    outlier_method = {"tukey": tukey_fences, "std": remove_distribution_outliers}
    assert method in outlier_method, "No se reconoce el método de filtrado"
    data = outlier_method[method](data, **kwargs)
    return data
