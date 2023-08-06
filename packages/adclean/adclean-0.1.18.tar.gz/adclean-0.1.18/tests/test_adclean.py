from adclean.cleaner import Cleaner
import pandas as pd
import pytest


@pytest.mark.parametrize(
    "serie, detect_method, replace_method, output",
    [
        (pd.Series([1, 2, 3, 4]), None, None, pd.Series([1, 2, 3, 4])),
        (pd.Series([1, 2, 3, 4]), ["test1"], None, ValueError("The detection method test1 does not exist")),
        (pd.Series([1, 2, 3, 4]), None, ["test1"], ValueError("he replace method test1 does not exist")),
        ([1, 2, 7, 1000], None, None, TypeError("The type of the series must be pd.Series"))
    ]
)
def test_init(serie, detect_method, replace_method, output):
    if isinstance(output, Exception):
        with pytest.raises(output.__class__) as e:
            Cleaner(serie, detect_method, replace_method)
        assert str(output) in str(e.value)
    else:
        Cleaner(serie, detect_method, replace_method).serie.equals(output)


@pytest.mark.parametrize(
    "cleaner, maximum, output",
    [
        (Cleaner(serie=pd.Series([200, 210, 700, 240]), detect_methods=["maximum"]), 500, [700])
    ]
)
def test_max(cleaner, maximum, output):
    assert cleaner._maximum(maximum) == output


@pytest.mark.parametrize(
    "cleaner, minimum, output",
    [
        (Cleaner(serie=pd.Series([200, 210, 5, 240]), detect_methods=["minimum"]), 100, [5])
    ]
)
def test_min(cleaner, minimum, output):
    assert cleaner._minimum(minimum) == output


# @pytest.mark.parametrize(
#     "cleaner, output",
#     [
#         (Cleaner(pd.Series([1, 2, 6, 3])), [3])
#     ]
# )
# def test_mean(cleaner, output):
#     assert (cleaner._mean() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([1, 2, 1000])), [1000])
    ]
)
def test_standard_devation(cleaner, output):
    assert (cleaner._standard_deviation() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([1, 2, 800])), [800])
    ]
)
def test_gaussian_mixture_model(cleaner, output):
    assert (cleaner._gaussian_mixture_model() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([2, 5, 400])), [400])
    ]
)
def test_extreme_value_analysis(cleaner, output):
    assert (cleaner._extreme_value_analysis() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([1, 3, 500])), [500])
    ]
)
def test_local_outlier_factor(cleaner, output):
    assert (cleaner._local_outlier_factor() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([2, 5, 600])), [600])
    ]
)
def test_connectivity_based_outlier_detection(cleaner, output):
    assert (cleaner._connectivity_based_outlier_detection() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([4, 2, 700])), [700])
    ]
)
def test_angular_based_outlier_detection(cleaner, output):
    assert (cleaner._angular_based_outlier_detection() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([2, 6, 450])), [450])
    ]
)
def test_dbscan_clustering(cleaner, output):
    assert (cleaner._dbscan_clustering() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([6, 2, 900])), [900])
    ]
)
def test_kmeans_clustering(cleaner, output):
    assert (cleaner._kmeans_clustering() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([3, 8, 750])), [750])
    ]
)
def test_knearest_neighbor(cleaner, output):
    assert (cleaner._knearest_neighbor() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([3, 4, 650])), [650])
    ]
)
def test_mahalanobis_distance(cleaner, output):
    assert (cleaner._mahalanobis_distance() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([3, 2, 550])), [550])
    ]
)
def test_isolation_forest(cleaner, output):
    assert (cleaner._isolation_forest() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([5, 2, 50])), [50])
    ]
)
def test_robust_random_cut_forest(cleaner, output):
    assert (cleaner._robust_random_cut_forest() == output)


@pytest.mark.parametrize(
    "cleaner, output",
    [
        (Cleaner(pd.Series([5, 6, 150])), [150])
    ]
)
def test_support_vector_machine(cleaner, output):
    assert (cleaner._support_vector_machine() == output)
