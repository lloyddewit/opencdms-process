from cmath import atan
import filecmp
import os
from pandas import DataFrame, read_csv
from opencdms_process.process.rinstat import cdms_products

TEST_DIR = os.path.dirname(__file__)


def test_climatic_summary():
    """test approx 29000 row dataframe with missing values"""
    data_file: str = os.path.join(TEST_DIR, "data", "dodoma.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=data,
        date_time="date",
        elements=["rain", "tmax"],
        summaries={"mean": "mean", "sd": "sd"},
        na_rm=True,
        to="overall",
    )
    assert (
        str(actual.head()) == "   mean_rain   sd_rain  mean_tmax   sd_tmax\n"
        "1   1.574531  6.960521  28.942301  2.188736"
    )

    actual = cdms_products.climatic_summary(
        data=data,
        date_time="date",
        elements=["rain", "tmax"],
        summaries={"mean": "mean", "sd": "sd", "n_na": "naflex::na_n"},
        na_rm=True,
        to="monthly",
    )
    assert __is_expected_csv(data=actual, file_name="climatic_summary_actual010.csv")

    """ test approx 55000 row dataframe with missing values
    """
    data_file: str = os.path.join(TEST_DIR, "data", "rwanda.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=data,
        date_time="date",
        elements=["precip", "tmp_min"],
        station="station_id",
        summaries={"mean": "mean", "sd": "sd"},
        na_prop=0,
        to="monthly",
    )
    assert __is_expected_csv(data=actual, file_name="climatic_summary_actual020.csv")

    """ run selection of package `testhat` tests
    """
    data_file: str = os.path.join(TEST_DIR, "data", "niger50.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=data,
        date_time="date",
        year="year",
        month="month",
        by="station_name",
        elements=["rain"],
        station="station_name",
        to="monthly",
        summaries={"mean": "mean", "st_dv": "sd", "n_na": "naflex::na_n"},
    )
    assert __is_expected_csv(data=actual, file_name="climatic_summary_actual030.csv")

    """ test with data used in demo
    """
    data_file: str = os.path.join(TEST_DIR, "data", "observationFinalMinimal.csv")
    data = read_csv(
        data_file,
        parse_dates=["obsDatetime"],
        dayfirst=True,
        na_values="NA",
    )
    # climatic_summary(data = obs, date_time = "obsDatetime", station = "ï..recordedFrom", elements = "obsValue", 
    #       to = "annual", summaries = c(mean = "mean", max = "max", min = "min"))
    actual = cdms_products.climatic_summary(
        data=data,
        date_time="obsDatetime",
        elements=["obsValue"],
        station="recordedFrom",
        to="annual",
        summaries={"mean": "mean", "max": "max", "min": "min"},
    )
    assert __is_expected_csv(data=actual, file_name="climatic_summary_actual040.csv")


def test_inventory_plot():
    data_file: str = os.path.join(TEST_DIR, "data", "daily_niger.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    output_path_actual: str = os.path.join(TEST_DIR, "results_actual")

    # Create an inventory plot with two elements and by station
    file_name_actual: str = "inventory_plot_actual010.jpg"
    actual = cdms_products.inventory_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=data,
        station="station_name",
        elements=["tmax", "tmin"],
        date_time="date",
    )
    assert __is_expected_jpg(file_name_actual)

    # Create an inventory plot by year and day of year
    # TODO Python plot has slightly more data than R plot
    file_name_actual: str = "inventory_plot_actual020.jpg"
    actual = cdms_products.inventory_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=data,
        station="station_name",
        elements=["tmax", "tmin"],
        date_time="date",
        year_doy_plot=True,
    )
    assert __is_expected_jpg(file_name_actual)

    # Can add in rainy/dry days into the plot
    file_name_actual: str = "inventory_plot_actual030.jpg"
    actual = cdms_products.inventory_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=data,
        station="station_name",
        elements=["tmax", "tmin"],
        date_time="date",
        rain="rain",
        display_rain_days=True,
    )
    assert __is_expected_jpg(file_name_actual)

    # test with data used in demo
    data_file: str = os.path.join(TEST_DIR, "data", "observationFinalMinimal.csv")
    data = read_csv(
        data_file,
        parse_dates=["obsDatetime"],
        dayfirst=True,
        na_values="NA",
    )

    file_name_actual: str = "inventory_plot_actual040.jpg"
    actual = cdms_products.inventory_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=data,
        station="recordedFrom",
        elements=["obsValue"],
        date_time="obsDatetime",
    )
    assert __is_expected_jpg(file_name_actual)


def test_inventory_table():
    data_file: str = os.path.join(TEST_DIR, "data", "daily_niger.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    # Functions output for one element (rain) for day
    actual = cdms_products.inventory_table(
        data=data,
        date_time="date",
        elements=["rain"],
        station="station_name",
        year="year",
        month="month",
        day="day",
    )
    assert __is_expected_csv(data=actual, file_name="inventory_table_actual010.csv")

    # Functions output for all elements for day
    actual = cdms_products.inventory_table(
        data=data,
        date_time="date",
        elements=["tmax", "tmin", "rain", "hmax", "hmin", "sunh", "ws", "wd"],
        station="station_name",
        year="year",
        month="month",
        day="day",
    )
    assert __is_expected_csv(data=actual, file_name="inventory_table_actual020.csv")

    # Functions output for one element (rain) for doy
    actual = cdms_products.inventory_table(
        data=data,
        date_time="date",
        elements=["rain"],
        station="station_name",
        year="year",
        month="month",
        day="doy",
    )
    assert __is_expected_csv(data=actual, file_name="inventory_table_actual030.csv")

    # Functions output for all elements for doy
    actual = cdms_products.inventory_table(
        data=data,
        date_time="date",
        elements=["tmax", "tmin", "rain", "hmax", "hmin", "sunh", "ws", "wd"],
        station="station_name",
        year="year",
        month="month",
        day="doy",
    )
    assert __is_expected_csv(data=actual, file_name="inventory_table_actual040.csv")


def test_timeseries_plot():
    data_file: str = os.path.join(TEST_DIR, "data", "niger50.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    output_path_actual: str = os.path.join(TEST_DIR, "results_actual", "")

    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name="timeseries_plot_actual010.jpg",
        data=data,
        date_time="date",
        elements="tmax",
        station="station_name",
        facet_by="stations",
    )

    assert True


def __is_expected_csv(data: DataFrame, file_name: str) -> bool:

    # write the actual results to csv file, and then read the results back in again
    # Note:We read the expected results from a csv file. Writing/reading this file may change the
    #      data frame's meta data. Therefore, we must also write/read the actual results to csv so
    #      that we are comparing like with like.
    output_file_actual: str = os.path.join(TEST_DIR, "results_actual", file_name)
    data.to_csv(output_file_actual, index=False)
    actual_from_csv: DataFrame = read_csv(output_file_actual)

    # read the expected reults from csv file
    output_file_expected: str = os.path.join(
        TEST_DIR, "results_expected", file_name.replace("actual", "expected")
    )
    expected_from_csv: DataFrame = read_csv(output_file_expected)

    # return if actual equals expected
    diffs: DataFrame = actual_from_csv.compare(expected_from_csv)
    return diffs.empty


def __is_expected_jpg(file_name: str) -> bool:
    output_file_actual, output_file_expected = __get_output_file_paths(file_name)
    return filecmp.cmp(output_file_actual, output_file_expected)


def __get_output_file_paths(file_name: str):
    output_file_actual: str = os.path.join(TEST_DIR, "results_actual", file_name)
    output_file_expected: str = os.path.join(
        TEST_DIR, "results_expected", file_name.replace("actual", "expected")
    )
    return output_file_actual, output_file_expected
