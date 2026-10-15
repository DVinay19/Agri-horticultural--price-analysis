import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Agri-Horticultural Commodity Price Analysis",
    page_icon="🌾",
    layout="wide"
)


# =========================================================
# BACKGROUND DESIGN
# =========================================================
def add_bg_from_url():
    st.markdown(
        """
        <style>
        [data-testid="stApp"] {
            background: url(
                "https://i.pinimg.com/736x/d3/e4/72/d3e47228c6543a1f5bf4d4c1ba05d352.jpg"
            ) no-repeat center center fixed;
            background-size: cover;
        }

        .block-container {
            background-color: rgba(0, 0, 0, 0.25);
            border-radius: 1rem;
            padding: 2rem;
            color: white;
        }

        section[data-testid="stSidebar"] > div:first-child {
            background-color: rgba(0, 0, 0, 0.4);
            color: white;
            border-radius: 0.5rem;
            padding: 1rem;
        }

        .stPlotlyChart {
            background-color: rgba(0, 0, 0, 0.2) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(0, 0, 0, 0.25);
            border-radius: 0.5rem;
        }

        .stTabs [aria-selected="true"] {
            color: white !important;
            border-bottom: 3px solid #f44336;
        }

        #MainMenu, footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


add_bg_from_url()


# =========================================================
# LOAD DATASET
# =========================================================
@st.cache_data
def load_data():
    csv_path = Path(__file__).resolve().parent / "agri_dataset.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            "agri_dataset.csv was not found. "
            "Keep it in the same folder as app.py."
        )

    data = pd.read_csv(
        csv_path,
        on_bad_lines="skip",
        low_memory=False
    )

    required_columns = [
        "Arrival_Date",
        "State",
        "Commodity",
        "Modal Price",
        "Market"
    ]

    missing = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    data["Date"] = pd.to_datetime(
        data["Arrival_Date"],
        errors="coerce",
        dayfirst=True
    )

    data["Modal Price"] = pd.to_numeric(
        data["Modal Price"],
        errors="coerce"
    )

    for column in ["State", "Commodity", "Market"]:
        data[column] = data[column].astype("string").str.strip()

    data = data.dropna(
        subset=[
            "Date",
            "State",
            "Commodity",
            "Modal Price",
            "Market"
        ]
    )

    data = data[
        (data["State"] != "") &
        (data["Commodity"] != "") &
        (data["Market"] != "") &
        (data["Modal Price"] >= 0)
    ].copy()

    data["Month"] = data["Date"].dt.month_name()
    data["Year"] = data["Date"].dt.year

    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Dataset loading failed: {error}")
    st.stop()

if df.empty:
    st.error("No valid records were found in the dataset.")
    st.stop()


# =========================================================
# CHART STYLE
# =========================================================
def style_chart(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0.3)",
        paper_bgcolor="rgba(0,0,0,0.3)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig


# =========================================================
# FORECASTING FUNCTIONS
# =========================================================
def seasonal_features(dates, origin_date):
    """
    Create regression features for a time trend and
    yearly seasonal patterns.
    """
    dates = pd.DatetimeIndex(pd.to_datetime(dates))
    origin_date = pd.Timestamp(origin_date)

    elapsed_months = (
        (dates.year - origin_date.year) * 12
        + dates.month - origin_date.month
    )

    trend = elapsed_months.astype(float) / 12.0

    month_angle = 2 * np.pi * (dates.month - 1) / 12

    return np.column_stack([
        np.ones(len(dates)),
        trend,
        np.sin(month_angle),
        np.cos(month_angle),
        np.sin(2 * month_angle),
        np.cos(2 * month_angle)
    ])


def fit_linear_trend(values):
    """Fit a simple linear trend using historical observations."""
    values = np.asarray(values, dtype=float)
    x = np.arange(len(values), dtype=float)

    return np.polyfit(x, values, 1)


def predict_linear_trend(coefficients, start_position, count):
    """Predict future values from a fitted linear trend."""
    x_future = np.arange(
        start_position,
        start_position + count,
        dtype=float
    )

    return np.polyval(coefficients, x_future)


def fit_seasonal_model(dates, values, origin_date):
    """
    Fit a regression with trend and annual seasonal
    components. This uses NumPy only.
    """
    features = seasonal_features(dates, origin_date)
    values = np.asarray(values, dtype=float)

    coefficients, _, _, _ = np.linalg.lstsq(
        features,
        values,
        rcond=None
    )

    return coefficients


def predict_seasonal_model(coefficients, dates, origin_date):
    """Predict prices using fitted trend and seasonal features."""
    features = seasonal_features(dates, origin_date)
    predictions = features @ coefficients

    return np.maximum(predictions, 0)


# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("Filter Options")

states = sorted(df["State"].unique().tolist())
commodities = sorted(df["Commodity"].unique().tolist())
months = list(calendar.month_name)[1:]
years = sorted(df["Year"].unique().tolist())

if not states or not commodities or not years:
    st.error("The dataset has no usable state, commodity, or year options.")
    st.stop()

state = st.sidebar.selectbox("Select State", states)
commodity = st.sidebar.selectbox("Select Commodity", commodities)
month = st.sidebar.selectbox("Select Month", months)
year = st.sidebar.selectbox("Select Year", years)

filtered = df[
    (df["State"] == state) &
    (df["Commodity"] == commodity) &
    (df["Month"] == month) &
    (df["Year"] == year)
].copy()


# =========================================================
# DASHBOARD HEADER
# =========================================================
st.title("🌾 Agri-Horticultural Commodity Price Analysis")

st.caption(
    "Explore agricultural prices, compare markets, "
    "analyze seasonal patterns, and forecast future prices."
)

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Price Trends",
    "📍 Regional Analysis",
    "📅 Seasonal Patterns",
    "📊 Commodity Comparison",
    "🔮 Forecast 2026–2027"
])


# =========================================================
# TAB 1: PRICE TRENDS
# =========================================================
with tab1:
    st.subheader("Price Trends")

    if not filtered.empty:
        trend_data = (
            filtered.groupby(
                ["Date", "Market"],
                as_index=False
            )["Modal Price"]
            .mean()
            .sort_values("Date")
        )

        fig = px.line(
            trend_data,
            x="Date",
            y="Modal Price",
            color="Market",
            markers=True,
            title=f"{commodity} Prices — {state}, {month} {year}"
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No data is available for these filters.")


# =========================================================
# TAB 2: REGIONAL ANALYSIS
# =========================================================
with tab2:
    st.subheader("Regional Price Comparison")

    regional_data = df[
        (df["State"] == state) &
        (df["Commodity"] == commodity) &
        (df["Month"] == month) &
        (df["Year"] == year)
    ]

    if not regional_data.empty:
        regional = (
            regional_data.groupby(
                "Market",
                as_index=False
            )["Modal Price"]
            .mean()
            .sort_values("Modal Price", ascending=False)
        )

        fig = px.bar(
            regional,
            x="Market",
            y="Modal Price",
            title=f"Average {commodity} Price by Market"
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No regional data is available for these filters.")


# =========================================================
# TAB 3: SEASONAL PATTERNS
# =========================================================
with tab3:
    st.subheader("Seasonal Price Patterns")

    seasonal_data = df[
        (df["State"] == state) &
        (df["Commodity"] == commodity) &
        (df["Year"] == year)
    ].copy()

    if not seasonal_data.empty:
        seasonal_data["MonthNumber"] = (
            seasonal_data["Date"].dt.month
        )

        seasonal_avg = (
            seasonal_data.groupby("MonthNumber")["Modal Price"]
            .mean()
            .reindex(range(1, 13))
            .rename_axis("MonthNumber")
            .reset_index()
        )

        seasonal_avg["Month"] = seasonal_avg[
            "MonthNumber"
        ].map(lambda number: calendar.month_name[number])

        seasonal_avg = seasonal_avg.dropna(
            subset=["Modal Price"]
        )

        fig = px.line(
            seasonal_avg,
            x="Month",
            y="Modal Price",
            markers=True,
            title=f"Monthly Average Prices — {commodity}, {year}",
            category_orders={"Month": months}
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No seasonal data is available for this year.")


# =========================================================
# TAB 4: COMMODITY COMPARISON
# =========================================================
with tab4:
    st.subheader("Commodity Comparison")

    comparison = df[
        (df["State"] == state) &
        (df["Month"] == month) &
        (df["Year"] == year)
    ]

    if not comparison.empty:
        comparison_avg = (
            comparison.groupby(
                "Commodity",
                as_index=False
            )["Modal Price"]
            .mean()
            .sort_values("Modal Price", ascending=False)
        )

        fig = px.bar(
            comparison_avg,
            x="Commodity",
            y="Modal Price",
            title=f"Commodity Prices — {state}, {month} {year}"
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No commodity comparison data is available.")


# =========================================================
# TAB 5: FORECAST JANUARY 2026 TO DECEMBER 2027
# =========================================================
with tab5:
    st.subheader("Agricultural Price Forecast")

    st.caption(
        "Monthly estimates from January 2026 through December 2027. "
        "These are model predictions, not observed market prices."
    )

    history = df[
        (df["State"] == state) &
        (df["Commodity"] == commodity) &
        (df["Date"] < pd.Timestamp("2026-01-01"))
    ][["Date", "Modal Price"]].copy()

    if history.empty:
        st.warning(
            "No historical price records were found for this selection."
        )

    else:
        # Convert daily or irregular market records into monthly averages.
        monthly_prices = (
            history.set_index("Date")["Modal Price"]
            .sort_index()
            .resample("MS")
            .mean()
        )

        # Fill only gaps that are surrounded by real observations.
        monthly_prices = monthly_prices.interpolate(
            method="linear",
            limit_area="inside"
        )

        training = monthly_prices.dropna()

        if len(training) < 6:
            st.warning(
                "At least six usable monthly observations are needed "
                "for a basic forecast. Select a commodity with "
                "more historical data."
            )

        else:
            historical_dates = training.index
            historical_values = training.to_numpy(dtype=float)

            # Hold out the latest months for validation.
            # These observations are not used to fit either model
            # during the initial validation comparison.
            validation_size = min(
                6,
                max(3, len(training) // 5)
            )

            split_position = len(training) - validation_size

            fit_dates = historical_dates[:split_position]
            fit_values = historical_values[:split_position]

            validation_dates = historical_dates[split_position:]
            validation_values = historical_values[split_position:]

            # ---------------------------------------------
            # Model A: Linear trend
            # ---------------------------------------------
            linear_coefficients = fit_linear_trend(fit_values)

            linear_validation_predictions = predict_linear_trend(
                linear_coefficients,
                start_position=len(fit_values),
                count=validation_size
            )

            linear_validation_predictions = np.maximum(
                linear_validation_predictions,
                0
            )

            linear_mae = float(
                np.mean(
                    np.abs(
                        validation_values -
                        linear_validation_predictions
                    )
                )
            )

            # ---------------------------------------------
            # Model B: Seasonal trend regression
            # Requires at least 24 monthly training observations.
            # ---------------------------------------------
            seasonal_mae = None

            if len(fit_values) >= 24:
                seasonal_coefficients = fit_seasonal_model(
                    fit_dates,
                    fit_values,
                    fit_dates[0]
                )

                seasonal_validation_predictions = predict_seasonal_model(
                    seasonal_coefficients,
                    validation_dates,
                    fit_dates[0]
                )

                seasonal_mae = float(
                    np.mean(
                        np.abs(
                            validation_values -
                            seasonal_validation_predictions
                        )
                    )
                )

            # Select the better model by held-out MAE.
            if (
                seasonal_mae is not None and
                seasonal_mae < linear_mae
            ):
                selected_model = "Seasonal trend regression"
            else:
                selected_model = "Linear trend"

            # ---------------------------------------------
            # Refit the selected model on all available history.
            # ---------------------------------------------
            origin_date = historical_dates[0]

            future_dates = pd.date_range(
                start="2026-01-01",
                end="2027-12-01",
                freq="MS"
            )

            if selected_model == "Seasonal trend regression":
                final_coefficients = fit_seasonal_model(
                    historical_dates,
                    historical_values,
                    origin_date
                )

                forecast_values = predict_seasonal_model(
                    final_coefficients,
                    future_dates,
                    origin_date
                )

            else:
                final_coefficients = fit_linear_trend(
                    historical_values
                )

                forecast_values = predict_linear_trend(
                    final_coefficients,
                    start_position=len(historical_values),
                    count=len(future_dates)
                )

                forecast_values = np.maximum(
                    forecast_values,
                    0
                )

            forecast_df = pd.DataFrame({
                "Month": future_dates.strftime("%B %Y"),
                "Date": future_dates,
                "Predicted Modal Price": np.round(
                    forecast_values,
                    2
                )
            })

            latest_date = historical_dates.max()
            latest_price = float(historical_values[-1])

            # ---------------------------------------------
            # Key metrics
            # ---------------------------------------------
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Historical Months",
                f"{len(training)}"
            )

            col2.metric(
                "Latest Monthly Average",
                f"{latest_price:,.2f}"
            )

            col3.metric(
                "Forecast Horizon",
                "24 months"
            )

            st.markdown("### Model Validation")

            metric1, metric2 = st.columns(2)

            metric1.metric(
                f"Linear Trend MAE ({validation_size}-month holdout)",
                f"{linear_mae:,.2f}"
            )

            if seasonal_mae is not None:
                metric2.metric(
                    f"Seasonal Model MAE ({validation_size}-month holdout)",
                    f"{seasonal_mae:,.2f}"
                )
            else:
                metric2.metric(
                    "Seasonal Model MAE",
                    "Not evaluated"
                )

                st.info(
                    "The seasonal model needs at least 24 monthly "
                    "observations in the training portion. More "
                    "historical data is needed to compare it fairly."
                )

            st.write(
                f"**Selected forecasting method:** {selected_model}"
            )

            st.caption(
                f"Validation uses the last {validation_size} historical "
                "months as a holdout. MAE is the average absolute "
                "difference between predictions and observed prices; "
                "lower is better."
            )

            if latest_date < pd.Timestamp("2025-12-01"):
                st.warning(
                    f"Usable historical data ends in "
                    f"{latest_date:%B %Y}. Forecast uncertainty is "
                    "higher when the available history ends earlier."
                )

            # ---------------------------------------------
            # Forecast chart
            # ---------------------------------------------
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=historical_dates,
                    y=historical_values,
                    name="Historical Monthly Average",
                    mode="lines+markers",
                    line=dict(
                        color="#55C2FF",
                        width=2
                    )
                )
            )

            # Connect the forecast visually to the latest history.
            connected_dates = pd.DatetimeIndex(
                [latest_date]
            ).append(future_dates)

            connected_values = np.concatenate((
                [latest_price],
                forecast_values
            ))

            fig.add_trace(
                go.Scatter(
                    x=connected_dates,
                    y=connected_values,
                    name=f"Forecast: {selected_model}",
                    mode="lines+markers",
                    line=dict(
                        color="#FFB347",
                        width=3,
                        dash="dash"
                    )
                )
            )

            fig.add_vline(
                x="2026-01-01",
                line_dash="dot",
                line_color="white",
                annotation_text="Forecast period"
            )

            fig.update_layout(
                title=f"{commodity} Price Forecast — {state}",
                xaxis_title="Month",
                yaxis_title="Modal Price",
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    y=1.12
                )
            )

            style_chart(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # ---------------------------------------------
            # Forecast table
            # ---------------------------------------------
            st.subheader("Monthly Predictions: 2026–2027")

            st.dataframe(
                forecast_df[
                    ["Month", "Predicted Modal Price"]
                ],
                use_container_width=True,
                hide_index=True
            )

            # ---------------------------------------------
            # Forecast download
            # ---------------------------------------------
            forecast_csv = forecast_df.to_csv(
                index=False
            ).encode("utf-8")

            safe_state = "".join(
                character if character.isalnum() else "_"
                for character in str(state)
            )

            safe_commodity = "".join(
                character if character.isalnum() else "_"
                for character in str(commodity)
            )

            st.download_button(
                label="Download 2026–2027 Forecast CSV",
                data=forecast_csv,
                file_name=(
                    f"{safe_state}_{safe_commodity}_"
                    "forecast_2026_2027.csv"
                ),
                mime="text/csv"
            )

            st.info(
                "The seasonal model represents recurring calendar-month "
                "patterns using smooth mathematical components. It is "
                "not a full agricultural forecasting system and does "
                "not explicitly account for weather, inflation, supply "
                "disruptions, demand, or government policy. The selected "
                "model is chosen by a limited historical holdout test; "
                "past validation performance does not guarantee future "
                "accuracy."
            )


# =========================================================
# DOWNLOAD FILTERED HISTORICAL DATA
# =========================================================
st.markdown("---")

st.subheader("⬇️ Download Filtered Historical Data")

if not filtered.empty:
    csv = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Filtered Data CSV",
        data=csv,
        file_name="filtered_agri_horticultural_data.csv",
        mime="text/csv"
    )

else:
    st.info("No historical data is available for the selected filters.")