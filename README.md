# delta-t-2021-2022
This repository contains all the scripts team DELTA-T wrote for the 2021-2022 Astro Pi Mission Space Lab project. It also contains the flight results (histograms.bin and data.csv) alongside the ground testing histograms file.

Flight scripts:


    - led_messages.py
    - main.py


Ground analysis scripts:


    - track.py - displays the ISS ground track alongside a 2D graph of measurements
    - histogram.py - display a 3D graph of all the histograms captured
    - data_series.py - used by track.py


To modify displayed data:


    - for track.py - choose the data series to display at line 76 from already defined series or create your own DataSeries(graph_title, unit, list_of_data_column_names)
    - for histogram.py - define histogram binary file on line 7