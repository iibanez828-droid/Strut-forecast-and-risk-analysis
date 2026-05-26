import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO


# ============================================================
# 1. EMBEDDED DATA
# ============================================================
# Source columns in the embedded CSV:
# Truck; Strut location; Type of strut; Strut accumulated hours; Strut current hours
#
# Correct interpretation:
# - Strut accumulated hours = accumulated life hours of the physical strut.
# - Strut current hours = current operating cycle hours for that strut position.
#
# Forecast logic:
# - Operating change-out interval uses Current Cycle Hours.
# - Maximum total life rule uses Strut Accumulated Life Hours.
# - New struts required are counted only when a strut reaches maximum total life.

EMBEDDED_STRUT_CSV = """Truck;Strut location;Type of strut;Strut accumulated hours;Strut current hours
823;Right rear strut;Standard;0;1194,7
823;Left reat strut;Standard;0;1194,7
823;Left front strut;Standard;20823,53;1954,2
824;Right front strut;Standard;76178,88;3401,24
824;Left reat strut;Standard;27505,09;2414,7
824;Right rear strut;Standard;19801,05;2396,9
825;Right front strut;Standard;79424,13;2608,9
825;Left front strut;Standard;44419,69;2608,9
825;Right rear strut;Standard;12639,56;9972,06
825;Left reat strut;Standard;0;1178,1
826;Right front strut;Standard;39009,64;7558,66
826;Left front strut;Standard;21534,76;2582,8
826;Right rear strut;Standard;6452,53;347,5
826;Left reat strut;Standard;0;1185
827;Left front strut;Standard;80898,4;1889,6
827;Right rear strut;Heavy Duty;0;353
827;Left reat strut;Heavy Duty;0;353
827;Right front strut;Standard;0;847,7
828;Left front strut;Standard;80544,67;5198,84
828;Right front strut;Standard;46058,11;7298,94
828;Right rear strut;Heavy Duty;0;15304,32
828;Left reat strut;Heavy Duty;0;15304,32
829;Right front strut;Standard;38962,98;9376,77
829;Right rear strut;Heavy Duty;16291,17;901,7
829;Left reat strut;Heavy Duty;0;453,1
829;Left front strut;Standard;0;453,1
830;Left front strut;Standard;70134,59;5217,97
830;Right front strut;Standard;30365,97;267,9
830;Left reat strut;Heavy Duty;0;300,1
830;Right rear strut;Heavy Duty;0;300,1
831;Left front strut;Standard;92427,77;309
831;Right front strut;Standard;20505,06;309
831;Right rear strut;Standard;2603,5;4211,03
831;Left reat strut;Standard;0;990,7
832;Right front strut;Standard;86110,17;3384,16
832;Right rear strut;Standard;16308,99;909,1
832;Left reat strut;Standard;3507,5;909,1
832;Left front strut;Standard;0;3803,36
833;Right front strut;Standard;71054,16;5902,77
833;Left reat strut;Standard;14430,94;2572,1
833;Right rear strut;Standard;13440;50,7
833;Left front strut;Standard;0;1315,7
834;Left front strut;Standard;36116,17;3019,1
834;Right front strut;Standard;12077,37;6854,95
834;Right rear strut;Standard;52306,92;2083,1
834;Left reat strut;Standard;15135,21;2525,2
835;Right front strut;Standard;74646,12;4327,5
835;Left front strut;Standard;41655,97;2684,1
835;Right rear strut;Standard;22419,38;4768,3
835;Left reat strut;Standard;0;1430,8
836;Left front strut;Standard;69963,13;9932,11
836;Right front strut;Standard;23982,76;14849,55
836;Left reat strut;Standard;31441,34;997,8
836;Right rear strut;Standard;16705,97;997,8
837;Right front strut;Standard;74319,11;6144,06
837;Left reat strut;Standard;60957,38;3253,5
837;Right rear strut;Standard;8500,22;5127,86
837;Left front strut;Standard;0;1167,6
838;Right front strut;Standard;18203,06;3836,7
838;Left front strut;Standard;6560,91;2069,5
838;Right rear strut;Heavy Duty;0;348,2
838;Left reat strut;Heavy Duty;0;348,2
839;Left front strut;Standard;42249,26;9711,72
839;Left reat strut;Standard;122,3;7432
839;Right rear strut;Standard;0;1560,4
840;Right front strut;Standard;79977,13;14390,54
840;Left front strut;Standard;20878,53;9844,54
840;Right rear strut;Standard;39083,96;2335
840;Left reat strut;Standard;3645,4;2736,4
841;Left front strut;Standard;76704,77;4233,59
841;Right front strut;Standard;43743,15;591,4
841;Right rear strut;Standard;58790,57;2503,2
841;Left reat strut;Standard;5137,3;2503,2
842;Right rear strut;Heavy Duty;16351,84;1086
842;Left reat strut;Heavy Duty;0;9128,35
842;Left front strut;Standard;;447,9
842;Right front strut;Standard;;447,9
843;Right front strut;Standard;38762,86;611,6
843;Left front strut;Standard;21955,41;611,6
843;Right rear strut;Standard;57679,67;122,5
843;Left reat strut;Standard;0;1585
844;Right front strut;Standard;79462,5;5561,55
844;Left front strut;Standard;43274,15;10270,45
844;Left reat strut;Standard;30792,31;5771
844;Right rear strut;Standard;16621,27;2846,8
845;Right front strut;Standard;16690,84;9490,35
845;Right rear strut;Heavy Duty;14315,27;6323,05
845;Left reat strut;Heavy Duty;10514,73;6323,05
845;Left front strut;Standard;0;404,4
846;Right front strut;Standard;78622,13;14562,47
846;Left front strut;Standard;52302,54;7824,38
846;Right rear strut;Standard;78264,55;8828,08
846;Left reat strut;Standard;8182,98;9292
847;Left front strut;Standard;88590,68;1580,9
847;Right front strut;Standard;64161,48;9365,22
847;Left reat strut;Standard;77278,72;1476,2
847;Right rear strut;Standard;41638,15;1949,9
848;Right front strut;Standard;15931,73;7102,69
848;Left front strut;Standard;13355,22;8463,69
848;Left reat strut;Standard;70979,48;3178,4
848;Right rear strut;Standard;13377,87;4132,99
849;Right front strut;Standard;0;7846,12
849;Left front strut;Standard;0;1061,3
849;Right rear strut;Standard;22248,57;2555,5
849;Left reat strut;Standard;0;1545
850;Right front strut;Standard;24947,32;4382,98
850;Left front strut;Standard;15316,69;5936,58
850;Left reat strut;Standard;20714,93;4490,88
850;Right rear strut;Standard;0;431,3
851;Right front strut;Standard;74024,61;592,2
851;Left front strut;Standard;31720,55;115,2
851;Left reat strut;Standard;4364,65;592,2
851;Right rear strut;Standard;0;7044,73
852;Right front strut;Standard;23151,73;819,5
852;Left front strut;Standard;0;3828,21
852;Left reat strut;Standard;87784,73;3560,91
852;Right rear strut;Standard;73080,36;3559,41"""

POSITION_MAP = {
    "Right rear strut": "Rear Right",
    "Left reat strut": "Rear Left",
    "Left rear strut": "Rear Left",
    "Right front strut": "Front Right",
    "Left front strut": "Front Left",
}

TYPE_MAP = {
    "Standard": "Std",
    "Heavy Duty": "HD",
}


def load_embedded_data() -> pd.DataFrame:
    df = pd.read_csv(StringIO(EMBEDDED_STRUT_CSV), sep=";", decimal=",")

    df = df.rename(
        columns={
            "Truck": "Truck ID",
            "Strut location": "Strut Position",
            "Type of strut": "Strut Type",
            "Strut accumulated hours": "Strut Accumulated Life Hours",
            "Strut current hours": "Current Cycle Hours",
        }
    )

    df["Truck ID"] = df["Truck ID"].astype(str)
    df["Strut Position"] = df["Strut Position"].map(POSITION_MAP).fillna(df["Strut Position"])
    df["Strut Type"] = df["Strut Type"].map(TYPE_MAP).fillna(df["Strut Type"])

    numeric_columns = ["Strut Accumulated Life Hours", "Current Cycle Hours"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df[
        [
            "Truck ID",
            "Strut Position",
            "Strut Type",
            "Strut Accumulated Life Hours",
            "Current Cycle Hours",
        ]
    ]


# ============================================================
# 2. VALIDATION
# ============================================================

def validate_input_data(df: pd.DataFrame) -> list:
    required_columns = [
        "Truck ID",
        "Strut Position",
        "Strut Type",
        "Strut Accumulated Life Hours",
        "Current Cycle Hours",
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

    for col in ["Strut Accumulated Life Hours", "Current Cycle Hours"]:
        if col in df.columns:
            if df[col].isna().any():
                errors.append(f"Column '{col}' contains missing or non-numeric values.")
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

            current_cycle_hours = float(row["Current Cycle Hours"])
            accumulated_life_hours = float(row["Strut Accumulated Life Hours"])
            remaining_annual_hours = float(annual_operating_hours)
            event_number = 0

            while remaining_annual_hours > 0:
                hours_to_interval = interval - current_cycle_hours
                hours_to_end_of_life = max_life_hours - accumulated_life_hours

                # Immediate event at the beginning of the year if already beyond a limit.
                if hours_to_interval <= 0 or hours_to_end_of_life <= 0:
                    event_number += 1
                    is_eol = hours_to_end_of_life <= 0
                    event_reason = "End of Life" if is_eol else "Operating Interval"

                    records.append(
                        {
                            "Year": year,
                            "Truck ID": truck_id,
                            "Strut Position": position,
                            "Strut Type": strut_type,
                            "Event Number in Year": event_number,
                            "Event Reason": event_reason,
                            "Hours Into Year at Event": annual_operating_hours - remaining_annual_hours,
                            "Cycle Hours at Event": current_cycle_hours,
                            "Strut Life Hours at Event": accumulated_life_hours,
                            "Operating Change-Out Required": 0 if is_eol else 1,
                            "End-of-Life Replacement": 1 if is_eol else 0,
                            "Total Replacement Events": 1,
                            "New Strut Required": 1 if is_eol else 0,
                        }
                    )

                    if is_eol:
                        # New physical strut installed: both counters restart.
                        current_cycle_hours = 0
                        accumulated_life_hours = 0
                    else:
                        # Operating change-out: operating cycle restarts, physical life remains.
                        current_cycle_hours = 0

                    continue

                next_event_hours = min(hours_to_interval, hours_to_end_of_life)

                if remaining_annual_hours >= next_event_hours:
                    event_number += 1
                    current_cycle_hours += next_event_hours
                    accumulated_life_hours += next_event_hours
                    remaining_annual_hours -= next_event_hours

                    is_eol = hours_to_end_of_life <= hours_to_interval
                    event_reason = "End of Life" if is_eol else "Operating Interval"

                    records.append(
                        {
                            "Year": year,
                            "Truck ID": truck_id,
                            "Strut Position": position,
                            "Strut Type": strut_type,
                            "Event Number in Year": event_number,
                            "Event Reason": event_reason,
                            "Hours Into Year at Event": annual_operating_hours - remaining_annual_hours,
                            "Cycle Hours at Event": current_cycle_hours,
                            "Strut Life Hours at Event": accumulated_life_hours,
                            "Operating Change-Out Required": 0 if is_eol else 1,
                            "End-of-Life Replacement": 1 if is_eol else 0,
                            "Total Replacement Events": 1,
                            "New Strut Required": 1 if is_eol else 0,
                        }
                    )

                    if is_eol:
                        current_cycle_hours = 0
                        accumulated_life_hours = 0
                    else:
                        current_cycle_hours = 0

                else:
                    current_cycle_hours += remaining_annual_hours
                    accumulated_life_hours += remaining_annual_hours
                    remaining_annual_hours = 0

            working_df.at[idx, "Current Cycle Hours"] = current_cycle_hours
            working_df.at[idx, "Strut Accumulated Life Hours"] = accumulated_life_hours

    schedule_df = pd.DataFrame(records)
    all_years = pd.DataFrame({"Year": list(range(start_year, end_year + 1))})

    if schedule_df.empty:
        yearly_summary = all_years.copy()
        for col in [
            "Std Operating Change-Outs",
            "HD Operating Change-Outs",
            "Std End-of-Life Replacements",
            "HD End-of-Life Replacements",
            "Total Operating Change-Outs",
            "Total End-of-Life Replacements",
            "Total Replacement Events",
            "New Std Struts Required",
            "New HD Struts Required",
            "Total New Struts Required",
        ]:
            yearly_summary[col] = 0
        truck_summary = pd.DataFrame()
        position_summary = pd.DataFrame()
        return yearly_summary, schedule_df, truck_summary, position_summary, working_df

    yearly_operating = (
        schedule_df
        .pivot_table(index="Year", columns="Strut Type", values="Operating Change-Out Required", aggfunc="sum", fill_value=0)
        .reset_index()
        .rename(columns={"Std": "Std Operating Change-Outs", "HD": "HD Operating Change-Outs"})
    )

    yearly_eol = (
        schedule_df
        .pivot_table(index="Year", columns="Strut Type", values="End-of-Life Replacement", aggfunc="sum", fill_value=0)
        .reset_index()
        .rename(columns={"Std": "Std End-of-Life Replacements", "HD": "HD End-of-Life Replacements"})
    )

    yearly_new = (
        schedule_df
        .pivot_table(index="Year", columns="Strut Type", values="New Strut Required", aggfunc="sum", fill_value=0)
        .reset_index()
        .rename(columns={"Std": "New Std Struts Required", "HD": "New HD Struts Required"})
    )

    yearly_summary = (
        all_years
        .merge(yearly_operating, on="Year", how="left")
        .merge(yearly_eol, on="Year", how="left")
        .merge(yearly_new, on="Year", how="left")
        .fillna(0)
    )

    for col in [
        "Std Operating Change-Outs",
        "HD Operating Change-Outs",
        "Std End-of-Life Replacements",
        "HD End-of-Life Replacements",
        "New Std Struts Required",
        "New HD Struts Required",
    ]:
        if col not in yearly_summary.columns:
            yearly_summary[col] = 0
        yearly_summary[col] = yearly_summary[col].astype(int)

    yearly_summary["Total Operating Change-Outs"] = (
        yearly_summary["Std Operating Change-Outs"] + yearly_summary["HD Operating Change-Outs"]
    )
    yearly_summary["Total End-of-Life Replacements"] = (
        yearly_summary["Std End-of-Life Replacements"] + yearly_summary["HD End-of-Life Replacements"]
    )
    yearly_summary["Total Replacement Events"] = (
        yearly_summary["Total Operating Change-Outs"] + yearly_summary["Total End-of-Life Replacements"]
    )
    yearly_summary["Total New Struts Required"] = (
        yearly_summary["New Std Struts Required"] + yearly_summary["New HD Struts Required"]
    )

    truck_summary = (
        schedule_df
        .groupby(["Truck ID", "Strut Type"], as_index=False)
        .agg(
            **{
                "Total Replacement Events": ("Total Replacement Events", "sum"),
                "Operating Change-Outs": ("Operating Change-Out Required", "sum"),
                "End-of-Life Replacements": ("End-of-Life Replacement", "sum"),
                "New Struts Required": ("New Strut Required", "sum"),
            }
        )
        .sort_values(["Truck ID", "Strut Type"])
    )

    position_summary = (
        schedule_df
        .groupby(["Strut Position", "Strut Type"], as_index=False)
        .agg(
            **{
                "Total Replacement Events": ("Total Replacement Events", "sum"),
                "Operating Change-Outs": ("Operating Change-Out Required", "sum"),
                "End-of-Life Replacements": ("End-of-Life Replacement", "sum"),
                "New Struts Required": ("New Strut Required", "sum"),
            }
        )
        .sort_values(["Strut Position", "Strut Type"])
    )

    return yearly_summary, schedule_df, truck_summary, position_summary, working_df


# ============================================================
# 4. STREAMLIT APP
# ============================================================

st.set_page_config(page_title="Truck Strut Replacement Forecast", layout="wide")

st.title("Truck Strut Replacement Forecast")
st.caption("Forecast of operating change-outs and end-of-life new-strut demand")

st.sidebar.header("Forecast Assumptions")

start_year = st.sidebar.number_input("Start Year", min_value=2026, max_value=2050, value=2027, step=1)
end_year = st.sidebar.number_input("End Year", min_value=int(start_year), max_value=2050, value=2030, step=1)
annual_operating_hours = st.sidebar.number_input("Annual Truck Operating Hours", min_value=0, value=6000, step=100)
std_interval = st.sidebar.number_input("Std Strut Operating Change-Out Interval", min_value=1, value=4500, step=100)
hd_interval = st.sidebar.number_input("HD Strut Operating Change-Out Interval", min_value=1, value=7500, step=100)
max_life_hours = st.sidebar.number_input("Strut Maximum Total Life Hours", min_value=1, value=45000, step=1000)

input_df = load_embedded_data()

st.subheader("Embedded Input Data")
st.dataframe(input_df, use_container_width=True)

total_trucks = input_df["Truck ID"].nunique()
total_struts = len(input_df)

col_a, col_b, col_c = st.columns(3)
col_a.metric("Trucks in Data", total_trucks)
col_b.metric("Struts in Data", total_struts)
col_c.metric("Expected Struts if 4 per Truck", total_trucks * 4)

errors = validate_input_data(input_df)
if errors:
    st.error("Input data validation failed.")
    for error in errors:
        st.warning(error)
    st.stop()

position_check = input_df.groupby("Truck ID")["Strut Position"].nunique().reset_index(name="Number of Positions")
incomplete_trucks = position_check[position_check["Number of Positions"] < 4]
if not incomplete_trucks.empty:
    st.warning("Some trucks have fewer than 4 struts. The forecast will only simulate the listed struts.")
    st.dataframe(incomplete_trucks, use_container_width=True)

already_over_life = input_df[input_df["Strut Accumulated Life Hours"] >= max_life_hours]
if not already_over_life.empty:
    st.warning("Some struts already exceed the maximum total life assumption and will be counted as immediate end-of-life replacements in the first forecast year.")
    st.dataframe(already_over_life, use_container_width=True)

with st.expander("View strut position completeness by truck"):
    position_count_table = (
        input_df
        .pivot_table(index="Truck ID", columns="Strut Position", values="Current Cycle Hours", aggfunc="count", fill_value=0)
        .reset_index()
    )
    st.dataframe(position_count_table, use_container_width=True)


# ============================================================
# 5. STRUT AGE POPULATION CHARTS
# ============================================================

st.subheader("Strut Age Population by Total Accumulated Life Hours")

age_bin_size = st.number_input(
    "Hour bin size for strut age population",
    min_value=500,
    max_value=10000,
    value=2500,
    step=500,
)

age_population_df = input_df.copy()
max_strut_hours = age_population_df["Strut Accumulated Life Hours"].max()
upper_bin_limit = int(((max_strut_hours // age_bin_size) + 1) * age_bin_size)
bins = list(range(0, upper_bin_limit + age_bin_size, age_bin_size))
labels = [f"{bins[i]:,} - {bins[i + 1]:,}" for i in range(len(bins) - 1)]

age_population_df["Life Hour Bucket"] = pd.cut(
    age_population_df["Strut Accumulated Life Hours"],
    bins=bins,
    labels=labels,
    include_lowest=True,
    right=False,
)

age_bucket_summary = (
    age_population_df
    .groupby(["Life Hour Bucket", "Strut Type"], observed=False)
    .size()
    .reset_index(name="Strut Count")
)

fig_age_population = px.bar(
    age_bucket_summary,
    x="Life Hour Bucket",
    y="Strut Count",
    color="Strut Type",
    title="Strut Age Population by Accumulated Life Hour Buckets",
    text_auto=True,
)
fig_age_population.update_layout(xaxis_title="Accumulated Strut Life Hours", yaxis_title="Number of Struts")
st.plotly_chart(fig_age_population, use_container_width=True)

st.subheader("Population Over Strut Accumulated Life Hours")

sorted_population_df = age_population_df.sort_values("Strut Accumulated Life Hours").reset_index(drop=True)
sorted_population_df["Cumulative Strut Population"] = sorted_population_df.index + 1
sorted_population_df["Cumulative Population %"] = (
    sorted_population_df["Cumulative Strut Population"] / len(sorted_population_df) * 100
)

fig_cumulative_population = px.line(
    sorted_population_df,
    x="Strut Accumulated Life Hours",
    y="Cumulative Strut Population",
    color="Strut Type",
    markers=True,
    title="Cumulative Strut Population Over Accumulated Life Hours",
    hover_data=["Truck ID", "Strut Position", "Current Cycle Hours", "Cumulative Population %"],
)
fig_cumulative_population.update_layout(
    xaxis_title="Accumulated Strut Life Hours",
    yaxis_title="Cumulative Number of Struts",
)
st.plotly_chart(fig_cumulative_population, use_container_width=True)

with st.expander("View strut age bucket summary"):
    st.dataframe(age_bucket_summary, use_container_width=True)


# ============================================================
# 6. RUN FORECAST
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

    total_operating = yearly_summary["Total Operating Change-Outs"].sum()
    total_eol = yearly_summary["Total End-of-Life Replacements"].sum()
    total_events = yearly_summary["Total Replacement Events"].sum()
    total_new_std = yearly_summary["New Std Struts Required"].sum()
    total_new_hd = yearly_summary["New HD Struts Required"].sum()
    total_new = yearly_summary["Total New Struts Required"].sum()

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    kpi1.metric("Operating Change-Outs", int(total_operating))
    kpi2.metric("End-of-Life Replacements", int(total_eol))
    kpi3.metric("Total Events", int(total_events))
    kpi4.metric("New Std Struts", int(total_new_std))
    kpi5.metric("New HD Struts", int(total_new_hd))
    kpi6.metric("Total New Struts", int(total_new))

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

    st.subheader("Forecast Charts")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig_operating = px.bar(
            yearly_summary,
            x="Year",
            y=["Std Operating Change-Outs", "HD Operating Change-Outs"],
            title="Operating Change-Outs by Year and Strut Type",
            barmode="group",
            text_auto=True,
        )
        st.plotly_chart(fig_operating, use_container_width=True)

    with chart_col2:
        fig_new = px.bar(
            yearly_summary,
            x="Year",
            y=["New Std Struts Required", "New HD Struts Required"],
            title="New Struts Required by Year Due to End of Life",
            barmode="group",
            text_auto=True,
        )
        st.plotly_chart(fig_new, use_container_width=True)

    fig_total = px.bar(
        yearly_summary,
        x="Year",
        y="Total Replacement Events",
        title="Total Replacement Events by Year",
        text_auto=True,
    )
    st.plotly_chart(fig_total, use_container_width=True)

    fig_truck = px.bar(
        truck_summary,
        x="Truck ID",
        y="Total Replacement Events",
        color="Strut Type",
        title="Total Replacement Events by Truck",
        text_auto=True,
    )
    fig_truck.update_layout(xaxis_type="category")
    st.plotly_chart(fig_truck, use_container_width=True)

    fig_truck_new = px.bar(
        truck_summary,
        x="Truck ID",
        y="New Struts Required",
        color="Strut Type",
        title="New Struts Required by Truck Due to End of Life",
        text_auto=True,
    )
    fig_truck_new.update_layout(xaxis_type="category")
    st.plotly_chart(fig_truck_new, use_container_width=True)

    fig_position = px.bar(
        position_summary,
        x="Strut Position",
        y="Total Replacement Events",
        color="Strut Type",
        title="Total Replacement Events by Strut Position",
        text_auto=True,
    )
    st.plotly_chart(fig_position, use_container_width=True)

    if not schedule_df.empty:
        reason_chart_df = (
            schedule_df
            .groupby(["Year", "Event Reason"], as_index=False)["Total Replacement Events"]
            .sum()
        )

        fig_reason = px.bar(
            reason_chart_df,
            x="Year",
            y="Total Replacement Events",
            color="Event Reason",
            title="Replacement Events by Reason",
            text_auto=True,
        )
        st.plotly_chart(fig_reason, use_container_width=True)
else:
    st.info("Click 'Run Forecast' to generate the replacement forecast.")
