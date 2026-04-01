import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Uber Ride Analytics",
    layout="wide",
    page_icon="🚖"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — subtle dark-accent polish
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0f0f0f; }
    /* Metric cards */
    [data-testid="metric-container"] {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 16px;
    }
    /* Download button */
    .stDownloadButton > button {
        background-color: #1DB954;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
    /* Chat messages */
    .stChatMessage { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOAD
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("uber.csv", encoding="latin-1")
    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🚖 Uber Analytics")
    st.markdown("---")
    selected = option_menu(
        "Main Menu",
        ["Dataset", "Overview", "Ride Analytics", "Data Assistant"],
        icons=["table", "bar-chart", "graph-up", "robot"],
        menu_icon="car-front",
        default_index=0,
        styles={
            "container": {"background-color": "#0f0f0f"},
            "icon": {"color": "#1DB954"},
            "nav-link-selected": {"background-color": "#1a1a2e", "color": "#1DB954"},
        }
    )
    st.markdown("---")
    st.caption(f"📦 Dataset: {df.shape[0]:,} rows × {df.shape[1]} cols")


# ══════════════════════════════════════════════
# MODULE 1 ── DATASET EXPLORER (IMPROVED)
# ══════════════════════════════════════════════
if selected == "Dataset":
    st.title("📋 Dataset Explorer")
    st.divider()

    # ── KPI row ──
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", f"{df.shape[0]:,}")
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", f"{df.isna().sum().sum():,}")
    col4.metric("Duplicate Rows", f"{df.duplicated().sum():,}")

    st.divider()

    # ── Column selector ──
    st.subheader("🔎 Column Selector")
    selected_cols = st.multiselect(
        "Choose columns to display",
        df.columns.tolist(),
        default=df.columns.tolist()
    )
    filtered_df = df[selected_cols].copy()

    # ── Search ──
    st.subheader("🔍 Search in Dataset")
    search_value = st.text_input("Search any value across all columns")
    if search_value:
        mask = filtered_df.astype(str).apply(
            lambda row: row.str.contains(search_value, case=False, na=False).any(), axis=1
        )
        filtered_df = filtered_df[mask]
        st.caption(f"Found **{len(filtered_df)}** matching rows")

    # ── Column filter — uses session_state so Apply Filter persists ──
    st.subheader("🎛️ Column Filter")
    col1, col2, col3 = st.columns([3, 3, 1])
    with col1:
        filter_col = st.selectbox("Select Column", filtered_df.columns)
    with col2:
        filter_val = st.selectbox("Select Value", filtered_df[filter_col].dropna().unique())
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        apply = st.button("Apply ✅")
        reset = st.button("Reset 🔄")

    # Persist filter across reruns
    if "filter_active" not in st.session_state:
        st.session_state.filter_active = False
    if apply:
        st.session_state.filter_active = True
        st.session_state.filter_col = filter_col
        st.session_state.filter_val = filter_val
    if reset:
        st.session_state.filter_active = False

    if st.session_state.filter_active:
        filtered_df = filtered_df[
            filtered_df[st.session_state.filter_col] == st.session_state.filter_val
        ]
        st.info(f"Filter active: **{st.session_state.filter_col}** = **{st.session_state.filter_val}** → {len(filtered_df):,} rows")

    st.divider()

    # ── Row display ──
    st.subheader("📄 Dataset Table")
    row = st.slider("Rows to display", 10, max(10, len(filtered_df)), min(50, len(filtered_df)))
    st.dataframe(filtered_df.head(row), use_container_width=True)

    if st.checkbox("Show Full Dataset"):
        st.dataframe(filtered_df, use_container_width=True)

    st.divider()

    # ── Column Stats — FIXED: correct dtype filter ──
    st.subheader("📊 Column Statistics")
    st.write(filtered_df.describe(include="all"))

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()  # ← bug fixed
    if numeric_cols:
        st.subheader("🔢 Numeric Column Deep Dive")
        sel_num = st.multiselect("Select Numeric Columns", numeric_cols, default=numeric_cols[:3])
        if sel_num:
            st.dataframe(filtered_df[sel_num].describe(), use_container_width=True)

            # Distribution charts for selected numeric cols
            for col_name in sel_num[:3]:
                fig = px.histogram(
                    filtered_df, x=col_name,
                    title=f"Distribution of {col_name}",
                    color_discrete_sequence=["#1DB954"]
                )
                fig.update_layout(bargap=0.1)
                st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Download ──
    st.subheader("⬇️ Download Data")
    col1, col2 = st.columns(2)
    with col1:
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Filtered CSV",
            csv, "filtered_dataset.csv", "text/csv",
            use_container_width=True
        )
    with col2:
        st.caption(f"Will download **{len(filtered_df):,} rows** × **{len(filtered_df.columns)} cols**")


# ══════════════════════════════════════════════
# MODULE 2 ── OVERVIEW (IMPROVED)
# ══════════════════════════════════════════════
elif selected == "Overview":
    st.title("📊 Business Overview")
    st.markdown("---")

    completed = df[df["Booking Status"] == "Completed"]
    total_rides = len(df)
    total_revenue = completed["Booking Value"].sum()
    avg_dis = completed["Ride Distance"].mean()
    success_rate = (len(completed) / total_rides) * 100 if total_rides > 0 else 0
    avg_rating = completed["Customer Rating"].dropna().mean()

    # ── KPI Row ──
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("💰 Gross Revenue", f"₹{total_revenue:,.0f}", "vs Target: ₹1.1M")
    kpi2.metric("✅ Fulfilment Rate", f"{success_rate:.1f}%", "-2.4% vs Last Month")
    kpi3.metric("📍 Avg Trip Distance", f"{avg_dis:.1f} km")
    kpi4.metric("⭐ Avg Rating", f"{avg_rating:.2f} / 5.0")
    kpi5.metric("🚖 Total Bookings", f"{total_rides:,}")

    st.divider()

    # ── Vehicle Performance Matrix ── FIXED formatting ──
    st.subheader("🚗 Business Unit Performance Matrix")
    bu_metric = df.groupby("Vehicle Type").agg(
        Total_Bookings=("Booking ID", "count"),
        Revenue_Generated=("Booking Value", "sum"),
        Avg_dis=("Ride Distance", "mean"),
        Avg_Rating=("Customer Rating", "mean")
    ).reset_index()
    bu_metric["Revenue Share %"] = (
        bu_metric["Revenue_Generated"] / total_revenue * 100
    ) if total_revenue > 0 else 0

    st.dataframe(
        bu_metric.style.format({
            "Revenue_Generated": "₹{:,.0f}",        # ← fixed key + symbol
            "Avg_dis": "{:,.1f} km",                 # ← fixed key name
            "Avg_Rating": "{:,.2f} / 5.0",           # ← removed $
            "Revenue Share %": "{:,.1f}%"            # ← removed $
        }).background_gradient(subset=["Revenue_Generated"], cmap="YlGnBu"),
        use_container_width=True                      # ← fixed width
    )

    st.divider()

    # ── Revenue over Vehicle Type (bar) ──
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig_rev = px.bar(
            bu_metric, x="Vehicle Type", y="Revenue_Generated",
            title="Revenue by Vehicle Type",
            color="Vehicle Type",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_rev.update_layout(showlegend=False)
        st.plotly_chart(fig_rev, use_container_width=True)

    with col_chart2:
        fig_rating = px.bar(
            bu_metric, x="Vehicle Type", y="Avg_Rating",
            title="Avg Rating by Vehicle Type",
            color="Vehicle Type",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_rating.update_layout(showlegend=False, yaxis_range=[0, 5])
        st.plotly_chart(fig_rating, use_container_width=True)

    st.divider()

    # ── Operational Efficiency + Cancellation ──
    col_eff, col_can = st.columns(2)

    with col_eff:
        st.subheader("⚙️ Operational Efficiency")
        eff_df = df.groupby("Vehicle Type")[["Avg VTAT", "Avg CTAT"]].mean().round(2)
        st.caption("Average Turnaround Time (minutes)")
        st.dataframe(
            eff_df.style
            .highlight_max(axis=0, color="#ffcccc")
            .highlight_min(axis=0, color="#ccffcc"),
            use_container_width=True
        )

    with col_can:
        st.subheader("❌ Cancellation Audit")
        status_count = df["Booking Status"].value_counts().to_frame(name="Count")
        status_count["Share %"] = (status_count["Count"] / total_rides * 100).round(1)
        st.dataframe(status_count, use_container_width=True)

        fig_pie = px.pie(
            values=status_count["Count"],
            names=status_count.index,
            title="Booking Status Split",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # ── Financial Deep Dive ──
    st.header("💳 Financial Deep Dive")
    pay_col, reason_col = st.columns([4, 6])

    with pay_col:
        st.markdown("**Payment Method Preference**")
        pay_summary = (completed["Payment Method"].value_counts(normalize=True) * 100).round(1)
        st.dataframe(pay_summary.rename("Usage %"), use_container_width=True)

        fig_pay = px.pie(
            values=pay_summary.values,
            names=pay_summary.index,
            title="Payment Methods",
            hole=0.35
        )
        st.plotly_chart(fig_pay, use_container_width=True)

    with reason_col:
        st.markdown("**Top Cancellation Reasons**")
        cust_reason = df["Reason for cancelling by Customer"].dropna().value_counts().head(3)
        drv_reason = df["Driver Cancellation Reason"].dropna().value_counts().head(3)
        cust_reason.index = "Customer: " + cust_reason.index
        drv_reason.index = "Driver: " + drv_reason.index
        reason_df = pd.concat([cust_reason, drv_reason]).to_frame("Incident Count")
        st.dataframe(reason_df, use_container_width=True)

        fig_bar = px.bar(
            reason_df.reset_index(),
            x="index", y="Incident Count",
            title="Cancellation Reasons Breakdown",
            color="index",
            color_discrete_sequence=px.colors.qualitative.Antique
        )
        fig_bar.update_layout(showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(fig_bar, use_container_width=True)


# ══════════════════════════════════════════════
# MODULE 3 ── RIDE ANALYTICS (IMPROVED)
# ══════════════════════════════════════════════
elif selected == "Ride Analytics":
    st.title("🚀 Advanced Ride Intelligence Dashboard")
    st.divider()

    completed = df[df["Booking Status"] == "Completed"]

    # ── Filters in sidebar for this page ──
    with st.sidebar:
        st.markdown("### 🎛️ Analytics Filters")
        vehicle_filter = st.multiselect(
            "Vehicle Type",
            df["Vehicle Type"].unique(),
            default=df["Vehicle Type"].unique()
        )
        completed = completed[completed["Vehicle Type"].isin(vehicle_filter)]
        st.caption(f"Showing {len(completed):,} completed rides")

    # ── Row 1: Sunburst + Treemap ──
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌞 Revenue Hierarchy (Sunburst)")
        fig1 = px.sunburst(
            completed,
            path=["Vehicle Type", "Payment Method"],
            values="Booking Value",
            color="Booking Value",
            color_continuous_scale="Turbo",
            title="Revenue by Vehicle & Payment Method"
        )
        fig1.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig1, use_container_width=True)          # ← fixed width

    with col2:
        st.subheader("🗺️ Revenue Treemap")
        fig2 = px.treemap(
            completed,
            path=["Vehicle Type", "Payment Method"],
            values="Booking Value",
            color="Booking Value",
            color_continuous_scale="Blues",
            title="Revenue Distribution"
        )
        fig2.update_layout(margin=dict(t=40, l=0, r=0, b=0))    # ← removed hardcoded width=500
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ── Row 2: Box plot + Scatter ──
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("⭐ Customer Rating Spread")
        fig3 = px.box(
            completed,
            x="Vehicle Type",
            y="Customer Rating",
            color="Vehicle Type",
            points="outliers",
            title="Rating Distribution by Vehicle Type"
        )
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("📍 Distance vs Revenue")
        fig_scatter = px.scatter(
            completed,
            x="Ride Distance",
            y="Booking Value",
            color="Vehicle Type",
            size="Booking Value",
            opacity=0.6,
            title="Ride Distance vs Booking Value",
            trendline="ols"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # ── Sankey ──
    st.subheader("🔀 Ride Flow Analysis (Sankey)")
    flow = df.groupby(["Vehicle Type", "Booking Status"]).size().reset_index(name="count")
    source_labels = flow["Vehicle Type"].unique().tolist()
    target_labels = flow["Booking Status"].unique().tolist()
    labels = source_labels + target_labels
    source = flow["Vehicle Type"].apply(lambda x: labels.index(x)).tolist()
    target = flow["Booking Status"].apply(lambda x: labels.index(x)).tolist()
    value = flow["count"].tolist()

    fig4 = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15, thickness=25,
            line=dict(color="#1DB954", width=1),
            label=labels,
            color=["#1a1a2e"] * len(labels)
        ),
        link=dict(source=source, target=target, value=value)
    )])
    fig4.update_layout(height=500, font_size=13)
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # ── NEW: Rating heatmap by Vehicle × Payment ──
    st.subheader("🔥 Rating Heatmap — Vehicle Type × Payment Method")
    heatmap_data = completed.pivot_table(
        values="Customer Rating",
        index="Vehicle Type",
        columns="Payment Method",
        aggfunc="mean"
    ).round(2)
    fig5 = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale="RdYlGn",
        title="Avg Customer Rating by Vehicle & Payment Method",
        aspect="auto"
    )
    st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════
# MODULE 4 ── DATA ASSISTANT (MAJOR UPGRADE)
# ══════════════════════════════════════════════
elif selected == "Data Assistant":

    st.title("Data Assistant")
    st.divider()

    st.write("Ask Question About the Dataset And get visual insight.")
    user_question = st.text_input("Ask Your Question")

    if user_question:
        q = user_question.lower()

        completed = df[df["Booking Status"] == "Completed"]

        if "total rides" in q:
            total = len(df)
            st.success(f"Total Rides: {total}")

            status = df["Booking Status"].value_counts()

            fig = px.bar(
                x=status.index,
                y=status.values,
                labels={"x": "Booking Status", "y": "Ride Count"},
                title="Ride Distribution by status"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif "revenue" in q:
            revenue = completed.groupby("Vehicle Type")["Booking Value"].sum()
            st.success(f"Total Revenue: {revenue.sum():,.2f}")

            fig = px.bar(
                x=revenue.index,
                y=revenue.values,
                title="Revenue Distribution by Vehicle Type",
                labels={"x": "Vehicle Type", "y": "Revenue"}
            )
            st.plotly_chart(fig, use_container_width=True)

        elif "distance" in q:
            fig = px.scatter(
                completed,
                x="Ride Distance",
                y="Booking Value",
                color="Vehicle Type",
                title="Ride Distance vs Booking Value"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.success(f"Average Distance: {completed['Ride Distance'].mean():,.2f}")

else:
    st.warning("Question not recognized, try asking about revenue, total rides, distance.")
    st.divider()