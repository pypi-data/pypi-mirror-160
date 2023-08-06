Outlier detection system for RATT's transient and variable source detection project
    Designed and implemented by: Olwethu Sigwela


USAGE:

    THe system uses lightcurves as input data, and requires Local Sky Model coordinates of the sources each lightcurve was extracted from
    
    Data directory must have the following structure:
        .
        ├── lightcurves
            ├──set_1
                ├──source_0.p (pickle file containing list with [light curve, light curve noise estimations, source coordinates] respectively)

                ├──source_1.p

                ├──source_2.p
                    .
                    .
                    .
            ├──set_2
                ├──source_100.p
                ├──source_101.p
                ├──source_102.p
                    .
                    .
                    .
            ├──set_3
                ├──source_200.p
                ├──source_201.p
                ├──source_202.p
                    .
                    .
                    .
