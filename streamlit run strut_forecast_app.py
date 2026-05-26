import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 1. EMBEDDED DATA
# ============================================================
# Data structure:
# Truck ID
# Strut Position
# Strut Type
# Truck Accumulated Hours
# Current Strut Hours
#
# NOTE:
# Your original data does not include a separate physical total life column.
# Therefore:
# Current Strut Total Life Hours = Current Strut Hours

EMBEDDED_STRUT_DATA = [
    {"Truck ID": "823", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1194.7, "Current Strut Total Life Hours": 1194.7},
    {"Truck ID": "823", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1194.7, "Current Strut Total Life Hours": 1194.7},
    {"Truck ID": "823", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 20823.53, "Current Strut Hours": 1954.2, "Current Strut Total Life Hours": 1954.2},
    {"Truck ID": "824", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 76178.88, "Current Strut Hours": 3401.24, "Current Strut Total Life Hours": 3401.24},
    {"Truck ID": "824", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 27505.09, "Current Strut Hours": 2414.7, "Current Strut Total Life Hours": 2414.7},
    {"Truck ID": "824", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 19801.05, "Current Strut Hours": 2396.9, "Current Strut Total Life Hours": 2396.9},
    {"Truck ID": "825", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 79424.13, "Current Strut Hours": 2608.9, "Current Strut Total Life Hours": 2608.9},
    {"Truck ID": "825", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 44419.69, "Current Strut Hours": 2608.9, "Current Strut Total Life Hours": 2608.9},
    {"Truck ID": "825", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 12639.56, "Current Strut Hours": 9972.06, "Current Strut Total Life Hours": 9972.06},
    {"Truck ID": "825", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1178.1, "Current Strut Total Life Hours": 1178.1},
    {"Truck ID": "826", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 39009.64, "Current Strut Hours": 7558.66, "Current Strut Total Life Hours": 7558.66},
    {"Truck ID": "826", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 21534.76, "Current Strut Hours": 2582.8, "Current Strut Total Life Hours": 2582.8},
    {"Truck ID": "826", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 6452.53, "Current Strut Hours": 347.5, "Current Strut Total Life Hours": 347.5},
    {"Truck ID": "826", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1185, "Current Strut Total Life Hours": 1185},
    {"Truck ID": "827", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 80898.4, "Current Strut Hours": 1889.6, "Current Strut Total Life Hours": 1889.6},
    {"Truck ID": "827", "Strut Position": "Rear Right", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 353, "Current Strut Total Life Hours": 353},
    {"Truck ID": "827", "Strut Position": "Rear Left", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 353, "Current Strut Total Life Hours": 353},
    {"Truck ID": "827", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 847.7, "Current Strut Total Life Hours": 847.7},
    {"Truck ID": "828", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 80544.67, "Current Strut Hours": 5198.84, "Current Strut Total Life Hours": 5198.84},
    {"Truck ID": "828", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 46058.11, "Current Strut Hours": 7298.94, "Current Strut Total Life Hours": 7298.94},
    {"Truck ID": "828", "Strut Position": "Rear Right", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 15304.32, "Current Strut Total Life Hours": 15304.32},
    {"Truck ID": "828", "Strut Position": "Rear Left", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 15304.32, "Current Strut Total Life Hours": 15304.32},
    {"Truck ID": "829", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 38962.98, "Current Strut Hours": 9376.77, "Current Strut Total Life Hours": 9376.77},
    {"Truck ID": "829", "Strut Position": "Rear Right", "Strut Type": "HD", "Truck Accumulated Hours": 16291.17, "Current Strut Hours": 901.7, "Current Strut Total Life Hours": 901.7},
    {"Truck ID": "829", "Strut Position": "Rear Left", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 453.1, "Current Strut Total Life Hours": 453.1},
    {"Truck ID": "829", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 453.1, "Current Strut Total Life Hours": 453.1},
    {"Truck ID": "830", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 70134.59, "Current Strut Hours": 5217.97, "Current Strut Total Life Hours": 5217.97},
    {"Truck ID": "830", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 30365.97, "Current Strut Hours": 267.9, "Current Strut Total Life Hours": 267.9},
    {"Truck ID": "830", "Strut Position": "Rear Left", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 300.1, "Current Strut Total Life Hours": 300.1},
    {"Truck ID": "830", "Strut Position": "Rear Right", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 300.1, "Current Strut Total Life Hours": 300.1},
    {"Truck ID": "831", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 92427.77, "Current Strut Hours": 309, "Current Strut Total Life Hours": 309},
    {"Truck ID": "831", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 20505.06, "Current Strut Hours": 309, "Current Strut Total Life Hours": 309},
    {"Truck ID": "831", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 2603.5, "Current Strut Hours": 4211.03, "Current Strut Total Life Hours": 4211.03},
    {"Truck ID": "831", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 990.7, "Current Strut Total Life Hours": 990.7},
    {"Truck ID": "832", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 86110.17, "Current Strut Hours": 3384.16, "Current Strut Total Life Hours": 3384.16},
    {"Truck ID": "832", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 16308.99, "Current Strut Hours": 909.1, "Current Strut Total Life Hours": 909.1},
    {"Truck ID": "832", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 3507.5, "Current Strut Hours": 909.1, "Current Strut Total Life Hours": 909.1},
    {"Truck ID": "832", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 3803.36, "Current Strut Total Life Hours": 3803.36},
    {"Truck ID": "833", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 71054.16, "Current Strut Hours": 5902.77, "Current Strut Total Life Hours": 5902.77},
    {"Truck ID": "833", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 14430.94, "Current Strut Hours": 2572.1, "Current Strut Total Life Hours": 2572.1},
    {"Truck ID": "833", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 13440, "Current Strut Hours": 50.7, "Current Strut Total Life Hours": 50.7},
    {"Truck ID": "833", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1315.7, "Current Strut Total Life Hours": 1315.7},
    {"Truck ID": "834", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 36116.17, "Current Strut Hours": 3019.1, "Current Strut Total Life Hours": 3019.1},
    {"Truck ID": "834", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 12077.37, "Current Strut Hours": 6854.95, "Current Strut Total Life Hours": 6854.95},
    {"Truck ID": "834", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 52306.92, "Current Strut Hours": 2083.1, "Current Strut Total Life Hours": 2083.1},
    {"Truck ID": "834", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 15135.21, "Current Strut Hours": 2525.2, "Current Strut Total Life Hours": 2525.2},
    {"Truck ID": "835", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 74646.12, "Current Strut Hours": 4327.5, "Current Strut Total Life Hours": 4327.5},
    {"Truck ID": "835", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 41655.97, "Current Strut Hours": 2684.1, "Current Strut Total Life Hours": 2684.1},
    {"Truck ID": "835", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 22419.38, "Current Strut Hours": 4768.3, "Current Strut Total Life Hours": 4768.3},
    {"Truck ID": "835", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1430.8, "Current Strut Total Life Hours": 1430.8},
    {"Truck ID": "836", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 69963.13, "Current Strut Hours": 9932.11, "Current Strut Total Life Hours": 9932.11},
    {"Truck ID": "836", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 23982.76, "Current Strut Hours": 14849.55, "Current Strut Total Life Hours": 14849.55},
    {"Truck ID": "836", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 31441.34, "Current Strut Hours": 997.8, "Current Strut Total Life Hours": 997.8},
    {"Truck ID": "836", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 16705.97, "Current Strut Hours": 997.8, "Current Strut Total Life Hours": 997.8},
    {"Truck ID": "837", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 74319.11, "Current Strut Hours": 6144.06, "Current Strut Total Life Hours": 6144.06},
    {"Truck ID": "837", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 60957.38, "Current Strut Hours": 3253.5, "Current Strut Total Life Hours": 3253.5},
    {"Truck ID": "837", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 8500.22, "Current Strut Hours": 5127.86, "Current Strut Total Life Hours": 5127.86},
    {"Truck ID": "837", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1167.6, "Current Strut Total Life Hours": 1167.6},
    {"Truck ID": "838", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 18203.06, "Current Strut Hours": 3836.7, "Current Strut Total Life Hours": 3836.7},
    {"Truck ID": "838", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 6560.91, "Current Strut Hours": 2069.5, "Current Strut Total Life Hours": 2069.5},
    {"Truck ID": "838", "Strut Position": "Rear Right", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 348.2, "Current Strut Total Life Hours": 348.2},
    {"Truck ID": "838", "Strut Position": "Rear Left", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 348.2, "Current Strut Total Life Hours": 348.2},
    {"Truck ID": "839", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 42249.26, "Current Strut Hours": 9711.72, "Current Strut Total Life Hours": 9711.72},
    {"Truck ID": "839", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 122.3, "Current Strut Hours": 7432, "Current Strut Total Life Hours": 7432},
    {"Truck ID": "839", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1560.4, "Current Strut Total Life Hours": 1560.4},
    {"Truck ID": "840", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 79977.13, "Current Strut Hours": 14390.54, "Current Strut Total Life Hours": 14390.54},
    {"Truck ID": "840", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 20878.53, "Current Strut Hours": 9844.54, "Current Strut Total Life Hours": 9844.54},
    {"Truck ID": "840", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 39083.96, "Current Strut Hours": 2335, "Current Strut Total Life Hours": 2335},
    {"Truck ID": "840", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 3645.4, "Current Strut Hours": 2736.4, "Current Strut Total Life Hours": 2736.4},
    {"Truck ID": "841", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 76704.77, "Current Strut Hours": 4233.59, "Current Strut Total Life Hours": 4233.59},
    {"Truck ID": "841", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 43743.15, "Current Strut Hours": 591.4, "Current Strut Total Life Hours": 591.4},
    {"Truck ID": "841", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 58790.57, "Current Strut Hours": 2503.2, "Current Strut Total Life Hours": 2503.2},
    {"Truck ID": "841", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 5137.3, "Current Strut Hours": 2503.2, "Current Strut Total Life Hours": 2503.2},
    {"Truck ID": "842", "Strut Position": "Rear Right", "Strut Type": "HD", "Truck Accumulated Hours": 16351.84, "Current Strut Hours": 1086, "Current Strut Total Life Hours": 1086},
    {"Truck ID": "842", "Strut Position": "Rear Left", "Strut Type": "HD", "Truck Accumulated Hours": 0, "Current Strut Hours": 9128.35, "Current Strut Total Life Hours": 9128.35},
    {"Truck ID": "842", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 447.9, "Current Strut Total Life Hours": 447.9},
    {"Truck ID": "842", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 447.9, "Current Strut Total Life Hours": 447.9},
    {"Truck ID": "843", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 38762.86, "Current Strut Hours": 611.6, "Current Strut Total Life Hours": 611.6},
    {"Truck ID": "843", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 21955.41, "Current Strut Hours": 611.6, "Current Strut Total Life Hours": 611.6},
    {"Truck ID": "843", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 57679.67, "Current Strut Hours": 122.5, "Current Strut Total Life Hours": 122.5},
    {"Truck ID": "843", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1585, "Current Strut Total Life Hours": 1585},
    {"Truck ID": "844", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 79462.5, "Current Strut Hours": 5561.55, "Current Strut Total Life Hours": 5561.55},
    {"Truck ID": "844", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 43274.15, "Current Strut Hours": 10270.45, "Current Strut Total Life Hours": 10270.45},
    {"Truck ID": "844", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 30792.31, "Current Strut Hours": 5771, "Current Strut Total Life Hours": 5771},
    {"Truck ID": "844", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 16621.27, "Current Strut Hours": 2846.8, "Current Strut Total Life Hours": 2846.8},
    {"Truck ID": "845", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 16690.84, "Current Strut Hours": 9490.35, "Current Strut Total Life Hours": 9490.35},
    {"Truck ID": "845", "Strut Position": "Rear Right", "Strut Type": "HD", "Truck Accumulated Hours": 14315.27, "Current Strut Hours": 6323.05, "Current Strut Total Life Hours": 6323.05},
    {"Truck ID": "845", "Strut Position": "Rear Left", "Strut Type": "HD", "Truck Accumulated Hours": 10514.73, "Current Strut Hours": 6323.05, "Current Strut Total Life Hours": 6323.05},
    {"Truck ID": "845", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 404.4, "Current Strut Total Life Hours": 404.4},
    {"Truck ID": "846", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 78622.13, "Current Strut Hours": 14562.47, "Current Strut Total Life Hours": 14562.47},
    {"Truck ID": "846", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 52302.54, "Current Strut Hours": 7824.38, "Current Strut Total Life Hours": 7824.38},
    {"Truck ID": "846", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 78264.55, "Current Strut Hours": 8828.08, "Current Strut Total Life Hours": 8828.08},
    {"Truck ID": "846", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 8182.98, "Current Strut Hours": 9292, "Current Strut Total Life Hours": 9292},
    {"Truck ID": "847", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 88590.68, "Current Strut Hours": 1580.9, "Current Strut Total Life Hours": 1580.9},
    {"Truck ID": "847", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 64161.48, "Current Strut Hours": 9365.22, "Current Strut Total Life Hours": 9365.22},
    {"Truck ID": "847", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 77278.72, "Current Strut Hours": 1476.2, "Current Strut Total Life Hours": 1476.2},
    {"Truck ID": "847", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 41638.15, "Current Strut Hours": 1949.9, "Current Strut Total Life Hours": 1949.9},
    {"Truck ID": "848", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 15931.73, "Current Strut Hours": 7102.69, "Current Strut Total Life Hours": 7102.69},
    {"Truck ID": "848", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 13355.22, "Current Strut Hours": 8463.69, "Current Strut Total Life Hours": 8463.69},
    {"Truck ID": "848", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 70979.48, "Current Strut Hours": 3178.4, "Current Strut Total Life Hours": 3178.4},
    {"Truck ID": "848", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 13377.87, "Current Strut Hours": 4132.99, "Current Strut Total Life Hours": 4132.99},
    {"Truck ID": "849", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 7846.12, "Current Strut Total Life Hours": 7846.12},
    {"Truck ID": "849", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1061.3, "Current Strut Total Life Hours": 1061.3},
    {"Truck ID": "849", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 22248.57, "Current Strut Hours": 2555.5, "Current Strut Total Life Hours": 2555.5},
    {"Truck ID": "849", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 1545, "Current Strut Total Life Hours": 1545},
    {"Truck ID": "850", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 24947.32, "Current Strut Hours": 4382.98, "Current Strut Total Life Hours": 4382.98},
    {"Truck ID": "850", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 15316.69, "Current Strut Hours": 5936.58, "Current Strut Total Life Hours": 5936.58},
    {"Truck ID": "850", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 20714.93, "Current Strut Hours": 4490.88, "Current Strut Total Life Hours": 4490.88},
    {"Truck ID": "850", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 431.3, "Current Strut Total Life Hours": 431.3},
    {"Truck ID": "851", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 74024.61, "Current Strut Hours": 592.2, "Current Strut Total Life Hours": 592.2},
    {"Truck ID": "851", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 31720.55, "Current Strut Hours": 115.2, "Current Strut Total Life Hours": 115.2},
    {"Truck ID": "851", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 4364.65, "Current Strut Hours": 592.2, "Current Strut Total Life Hours": 592.2},
    {"Truck ID": "851", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 7044.73, "Current Strut Total Life Hours": 7044.73},
    {"Truck ID": "852", "Strut Position": "Front Right", "Strut Type": "Std", "Truck Accumulated Hours": 23151.73, "Current Strut Hours": 819.5, "Current Strut Total Life Hours": 819.5},
    {"Truck ID": "852", "Strut Position": "Front Left", "Strut Type": "Std", "Truck Accumulated Hours": 0, "Current Strut Hours": 3828.21, "Current Strut Total Life Hours": 3828.21},
    {"Truck ID": "852", "Strut Position": "Rear Left", "Strut Type": "Std", "Truck Accumulated Hours": 87784.73, "Current Strut Hours": 3560.91, "Current Strut Total Life Hours": 3560.91},
    {"Truck ID": "852", "Strut Position": "Rear Right", "Strut Type": "Std", "Truck Accumulated Hours": 73080.36, "Current Strut Hours": 3559.41, "Current Strut Total Life Hours": 3559.41},
]


# ============================================================
# 2. VALIDATION
# ============================================================

def validate_input_data(df: pd.DataFrame) -> list:
    required_columns = [
        "Truck ID",
        "Truck Accumulated Hours",
        "Strut Position",
        "Strut Type",
        "Current Strut Hours",
        "Current Strut Total Life Hours",
    ]

    errors = []

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")

    valid_positions = {"Front Left", "Front Right", "Rear Left", "Rear Right"}
    valid_types = {"Std", "HD"}

    if "Strut Position" in df.columns:
        invalid_positions = set(df["Strut Position"]) - valid_positions
        if invalid_positions:
            errors.append(f"Invalid strut positions found: {invalid_positions}")

    if "Strut Type" in df.columns:
        invalid_types = set(df["Strut Type"]) - valid_types
        if invalid_types:
            errors.append(f"Invalid strut types found: {invalid_types}")

    numeric_columns = [
        "Truck Accumulated Hours",
        "Current Strut Hours",
        "Current Strut Total Life Hours",
    ]

    for col in numeric_columns:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"Column '{col}' must be numeric.")
            elif (df[col] < 0).any():
                errors.append(f"Column '{col}' contains negative values.")

    return errors


# ============================================================
# 3. FORECAST ENGINE
# ============================================================

def simulate_strut_forecast(
    input_df: pd.DataFrame,
    start_year: int,
    end_year: int,
    annual_operating_hours: float,
    std_interval: float,
    hd_interval: float,
    max_life_hours: float,
):
    records = []
    working_df = input_df.copy()

    for year in range(start_year, end_year + 1):
        for idx, row in working_df.iterrows():
            truck_id = row["Truck ID"]
            position = row["Strut Position"]
            strut_type = row["Strut Type"]
            interval = std_interval if strut_type == "Std" else hd_interval

            current_interval_hours = float(row["Current Strut Hours"])
            current_total_life_hours = float(row["Current Strut Total Life Hours"])
            remaining_annual_hours = float(annual_operating_hours)
            replacement_number = 0

            while remaining_annual_hours > 0:
                hours_to_interval = interval - current_interval_hours
                hours_to_end_of_life = max_life_hours - current_total_life_hours

                # Immediate replacement if the strut is already beyond its interval or max life.
                if hours_to_interval <= 0 or hours_to_end_of_life <= 0:
                    replacement_number += 1
                    replacement_reason = "End of Life" if hours_to_end_of_life <= 0 else "Operating Interval"

                    records.append(
                        {
                            "Year": year,
                            "Truck ID": truck_id,
                            "Strut Position": position,
                            "Strut Type": strut_type,
                            "Replacement Number in Year": replacement_number,
                            "Replacement Reason": replacement_reason,
                            "Hours Into Year at Replacement": annual_operating_hours - remaining_annual_hours,
                            "Interval Hours at Replacement": current_interval_hours,
                            "Total Life Hours at Replacement": current_total_life_hours,
                            "New Strut Required": 1,
                        }
                    )

                    current_interval_hours = 0
                    current_total_life_hours = 0
                    continue

                next_event_hours = min(hours_to_interval, hours_to_end_of_life)

                if remaining_annual_hours >= next_event_hours:
                    replacement_number += 1
                    replacement_reason = "End of Life" if hours_to_end_of_life <= hours_to_interval else "Operating Interval"

                    current_interval_hours += next_event_hours
                    current_total_life_hours += next_event_hours
                    remaining_annual_hours -= next_event_hours

                    records.append(
                        {
                            "Year": year,
                            "Truck ID": truck_id,
                            "Strut Position": position,
                            "Strut Type": strut_type,
                            "Replacement Number in Year": replacement_number,
                            "Replacement Reason": replacement_reason,
                            "Hours Into Year at Replacement": annual_operating_hours - remaining_annual_hours,
                            "Interval Hours at Replacement": current_interval_hours,
                            "Total Life Hours at Replacement": current_total_life_hours,
                            "New Strut Required": 1,
                        }
                    )

                    current_interval_hours = 0
                    current_total_life_hours = 0
                else:
                    current_interval_hours += remaining_annual_hours
                    current_total_life_hours += remaining_annual_hours
                    remaining_annual_hours = 0

            working_df.at[idx, "Current Strut Hours"] = current_interval_hours
            working_df.at[idx, "Current Strut Total Life Hours"] = current_total_life_hours

    schedule_df = pd.DataFrame(records)
    all_years = pd.DataFrame({"Year": list(range(start_year, end_year + 1))})

    if schedule_df.empty:
        yearly_summary = all_years.copy()
        yearly_summary["Std Struts Required"] = 0
        yearly_summary["HD Struts Required"] = 0
        yearly_summary["Total Struts Required"] = 0
        yearly_summary["Operating Interval Replacements"] = 0
        yearly_summary["End of Life Replacements"] = 0
        truck_summary = pd.DataFrame(columns=["Truck ID", "Strut Type", "Total Replacements"])
        position_summary = pd.DataFrame(columns=["Strut Position", "Strut Type", "Total Replacements"])
        return yearly_summary, schedule_df, truck_summary, position_summary, working_df

    yearly_by_type = (
        schedule_df
        .pivot_table(index="Year", columns="Strut Type", values="New Strut Required", aggfunc="sum", fill_value=0)
        .reset_index()
    )

    if "Std" not in yearly_by_type.columns:
        yearly_by_type["Std"] = 0
    if "HD" not in yearly_by_type.columns:
        yearly_by_type["HD"] = 0

    yearly_by_type = yearly_by_type.rename(
        columns={"Std": "Std Struts Required", "HD": "HD Struts Required"}
    )

    reason_summary = (
        schedule_df
        .pivot_table(index="Year", columns="Replacement Reason", values="New Strut Required", aggfunc="sum", fill_value=0)
        .reset_index()
    )

    if "Operating Interval" not in reason_summary.columns:
        reason_summary["Operating Interval"] = 0
    if "End of Life" not in reason_summary.columns:
        reason_summary["End of Life"] = 0

    reason_summary = reason_summary.rename(
        columns={
            "Operating Interval": "Operating Interval Replacements",
            "End of Life": "End of Life Replacements",
        }
    )

    yearly_summary = (
        all_years
        .merge(yearly_by_type, on="Year", how="left")
        .merge(reason_summary, on="Year", how="left")
        .fillna(0)
    )

    yearly_summary["Std Struts Required"] = yearly_summary["Std Struts Required"].astype(int)
    yearly_summary["HD Struts Required"] = yearly_summary["HD Struts Required"].astype(int)
    yearly_summary["Total Struts Required"] = yearly_summary["Std Struts Required"] + yearly_summary["HD Struts Required"]
    yearly_summary["Operating Interval Replacements"] = yearly_summary["Operating Interval Replacements"].astype(int)
    yearly_summary["End of Life Replacements"] = yearly_summary["End of Life Replacements"].astype(int)

    truck_summary = (
        schedule_df
        .groupby(["Truck ID", "Strut Type"], as_index=False)["New Strut Required"]
        .sum()
        .rename(columns={"New Strut Required": "Total Replacements"})
        .sort_values(["Truck ID", "Strut Type"])
    )

    position_summary = (
        schedule_df
        .groupby(["Strut Position", "Strut Type"], as_index=False)["New Strut Required"]
        .sum()
        .rename(columns={"New Strut Required": "Total Replacements"})
        .sort_values(["Strut Position", "Strut Type"])
    )

    return yearly_summary, schedule_df, truck_summary, position_summary, working_df


# ============================================================
# 4. STREAMLIT APP
# ============================================================

st.set_page_config(page_title="Truck Strut Replacement Forecast", layout="wide")

st.title("Truck Strut Replacement Forecast")
st.caption("Forecast of Std and HD strut replacement demand from embedded fleet data")


# ============================================================
# 5. SIDEBAR ASSUMPTIONS
# ============================================================

st.sidebar.header("Forecast Assumptions")

start_year = st.sidebar.number_input(
    "Start Year",
    min_value=2026,
    max_value=2050,
    value=2027,
    step=1,
)

end_year = st.sidebar.number_input(
    "End Year",
    min_value=int(start_year),
    max_value=2050,
    value=2030,
    step=1,
)

annual_operating_hours = st.sidebar.number_input(
    "Annual Truck Operating Hours",
    min_value=0,
    value=6000,
    step=100,
)

std_interval = st.sidebar.number_input(
    "Std Strut Replacement Interval",
    min_value=1,
    value=4500,
    step=100,
)

hd_interval = st.sidebar.number_input(
    "HD Strut Replacement Interval",
    min_value=1,
    value=7500,
    step=100,
)

max_life_hours = st.sidebar.number_input(
    "Strut Maximum Total Life Hours",
    min_value=1,
    value=45000,
    step=1000,
)


# ============================================================
# 6. LOAD DATA
# ============================================================

input_df = pd.DataFrame(EMBEDDED_STRUT_DATA)
input_df["Truck ID"] = input_df["Truck ID"].astype(str)

st.subheader("Embedded Input Data")
st.dataframe(input_df, use_container_width=True)

total_trucks = input_df["Truck ID"].nunique()
total_struts = len(input_df)

col_a, col_b, col_c = st.columns(3)
col_a.metric("Trucks in Data", total_trucks)
col_b.metric("Struts in Data", total_struts)
col_c.metric("Expected Struts if 4 per Truck", total_trucks * 4)


# ============================================================
# 7. DATA QUALITY WARNINGS
# ============================================================

errors = validate_input_data(input_df)

if errors:
    st.error("Input data validation failed.")
    for error in errors:
        st.warning(error)
    st.stop()

position_check = (
    input_df
    .groupby("Truck ID")["Strut Position"]
    .nunique()
    .reset_index(name="Number of Positions")
)

incomplete_trucks = position_check[position_check["Number of Positions"] < 4]

if not incomplete_trucks.empty:
    st.warning(
        "Some trucks have fewer than 4 struts in the embedded data. "
        "The forecast will only simulate the struts currently listed."
    )
    st.dataframe(incomplete_trucks, use_container_width=True)

position_count_table = (
    input_df
    .pivot_table(
        index="Truck ID",
        columns="Strut Position",
        values="Current Strut Hours",
        aggfunc="count",
        fill_value=0,
    )
    .reset_index()
)

with st.expander("View strut position completeness by truck"):
    st.dataframe(position_count_table, use_container_width=True)


# ============================================================
# 8. RUN FORECAST
# ============================================================

run_forecast = st.button("Run Forecast", type="primary")

if run_forecast:
    yearly_summary, schedule_df, truck_summary, position_summary, ending_state_df = simulate_strut_forecast(
        input_df=input_df,
        start_year=int(start_year),
        end_year=int(end_year),
        annual_operating_hours=float(annual_operating_hours),
        std_interval=float(std_interval),
        hd_interval=float(hd_interval),
        max_life_hours=float(max_life_hours),
    )

    st.success("Forecast completed successfully.")

    # ========================================================
    # 9. KPI SECTION
    # ========================================================

    total_std = yearly_summary["Std Struts Required"].sum()
    total_hd = yearly_summary["HD Struts Required"].sum()
    total_required = yearly_summary["Total Struts Required"].sum()
    total_interval = yearly_summary["Operating Interval Replacements"].sum()
    total_eol = yearly_summary["End of Life Replacements"].sum()

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Std Required", int(total_std))
    kpi2.metric("Total HD Required", int(total_hd))
    kpi3.metric("Total Struts Required", int(total_required))
    kpi4.metric("Interval Replacements", int(total_interval))
    kpi5.metric("End-of-Life Replacements", int(total_eol))

    # ========================================================
    # 10. TABLES
    # ========================================================

    st.subheader("Yearly Summary")
    st.dataframe(yearly_summary, use_container_width=True)

    st.subheader("Detailed Replacement Schedule")
    st.dataframe(schedule_df, use_container_width=True)

    st.subheader("Demand by Truck")
    st.dataframe(truck_summary, use_container_width=True)

    st.subheader("Demand by Strut Position")
    st.dataframe(position_summary, use_container_width=True)

    with st.expander("View Ending State After Forecast"):
        st.dataframe(ending_state_df, use_container_width=True)

    # ========================================================
    # 11. CHARTS
    # ========================================================

    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_std = px.bar(
            yearly_summary,
            x="Year",
            y="Std Struts Required",
            title="Std Struts Required by Year",
            text_auto=True,
        )
        st.plotly_chart(fig_std, use_container_width=True)

    with chart_col2:
        fig_hd = px.bar(
            yearly_summary,
            x="Year",
            y="HD Struts Required",
            title="HD Struts Required by Year",
            text_auto=True,
        )
        st.plotly_chart(fig_hd, use_container_width=True)

    fig_total = px.bar(
        yearly_summary,
        x="Year",
        y="Total Struts Required",
        title="Total Struts Required by Year",
        text_auto=True,
    )
    st.plotly_chart(fig_total, use_container_width=True)

    fig_truck = px.bar(
        truck_summary,
        x="Truck ID",
        y="Total Replacements",
        color="Strut Type",
        title="Demand by Truck",
        text_auto=True,
    )
    fig_truck.update_layout(xaxis_type="category")
    st.plotly_chart(fig_truck, use_container_width=True)

    fig_position = px.bar(
        position_summary,
        x="Strut Position",
        y="Total Replacements",
        color="Strut Type",
        title="Demand by Strut Position",
        text_auto=True,
    )
    st.plotly_chart(fig_position, use_container_width=True)

    if not schedule_df.empty:
        reason_chart_df = (
            schedule_df
            .groupby(["Year", "Replacement Reason"], as_index=False)["New Strut Required"]
            .sum()
        )

        fig_reason = px.bar(
            reason_chart_df,
            x="Year",
            y="New Strut Required",
            color="Replacement Reason",
            title="Replacement Demand by Reason",
            text_auto=True,
        )
        st.plotly_chart(fig_reason, use_container_width=True)
else:
    st.info("Click 'Run Forecast' to generate the replacement forecast.")
