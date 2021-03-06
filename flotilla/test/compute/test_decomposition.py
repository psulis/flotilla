import numpy.testing as npt
import pandas as pd
import pandas.util.testing as pdt
import pytest
from sklearn.decomposition import PCA, NMF


@pytest.fixture(params=[None, 2])
def n_components(request):
    return request.param


class TestDataFramePCA():
    def test_init(self, df_norm, n_components):
        from flotilla.compute.decomposition import DataFramePCA

        test_pca = DataFramePCA(df_norm, n_components=n_components)

        true_pca = PCA(n_components=n_components)
        true_pca.fit(df_norm.values)
        pc_names = ['pc_{}'.format(i + 1) for i in
                    range(true_pca.components_.shape[0])]
        true_pca.components_ = pd.DataFrame(true_pca.components_,
                                            index=pc_names,
                                            columns=df_norm.columns)
        true_pca.explained_variance_ = pd.Series(
            true_pca.explained_variance_, index=pc_names)
        true_pca.explained_variance_ratio_ = pd.Series(
            true_pca.explained_variance_ratio_, index=pc_names)
        true_pca.reduced_space = true_pca.transform(df_norm.values)
        true_pca.reduced_space = pd.DataFrame(true_pca.reduced_space,
                                              index=df_norm.index,
                                              columns=pc_names)

        npt.assert_array_equal(test_pca.X, df_norm.values)
        pdt.assert_frame_equal(test_pca.components_,
                               true_pca.components_)
        pdt.assert_series_equal(test_pca.explained_variance_,
                                true_pca.explained_variance_)
        pdt.assert_series_equal(test_pca.explained_variance_ratio_,
                                true_pca.explained_variance_ratio_)
        pdt.assert_frame_equal(test_pca.reduced_space,
                               true_pca.reduced_space)


class TestDataFrameNMF():
    def test_init(self, df_nonneg, RANDOM_STATE):
        from flotilla.compute.decomposition import DataFrameNMF

        test_nmf = DataFrameNMF(df_nonneg, n_components=2,
                                random_state=RANDOM_STATE)

        true_nmf = NMF(n_components=2, random_state=RANDOM_STATE,
                       init='nndsvd')
        reduced_space = true_nmf.fit_transform(df_nonneg.values)
        pc_names = ['pc_{}'.format(i + 1) for i in
                    range(true_nmf.components_.shape[0])]
        true_nmf.reduced_space = pd.DataFrame(reduced_space,
                                              index=df_nonneg.index,
                                              columns=pc_names)
        true_nmf.components_ = pd.DataFrame(true_nmf.components_,
                                            index=pc_names,
                                            columns=df_nonneg.columns)

        npt.assert_almost_equal(test_nmf.X, df_nonneg.values, decimal=4)
        pdt.assert_frame_equal(test_nmf.components_,
                               true_nmf.components_)
        pdt.assert_frame_equal(test_nmf.reduced_space,
                               true_nmf.reduced_space,
                               check_less_precise=True)
