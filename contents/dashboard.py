import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


@st.cache_data
def load_data():
    # 파일 read
    FILE_PATH = "SKN16-1st-5Team/docs"
    # FILE_PATH = "/content/drive/MyDrive/5조"
    fuel_df = pd.read_csv(f"{FILE_PATH}/유류비.csv", encoding="CP949")
    car_count_df = pd.read_excel(f"{FILE_PATH}/시도별_연료별_등록현황.xlsx")
    region_df = pd.read_csv(f"{FILE_PATH}/지역별 좌표.csv")
    return fuel_df, car_count_df, region_df


# -------------------- 대시보드 함수 --------------------
def show_dashboard():
    fuel_df, car_count_df, region_df = load_data()

    with st.container():
        st.write("유류비, 연료별 자동차 등록대수 변화")

    with st.container():
        st.write("연료별 자동차 등록대수 구성비 변화")

    with st.container():
        st.markdown("##### 20년 ~ 25년 연료별 등록대수")

        col1, col2 = st.columns(2)

        with col1:
            fuel_types = ["휘발유", "경유", "LPG"]
            st.selectbox("연료 타입", fuel_types, key="fuel")
            selected_fuel = st.session_state["fuel"]

        with col2:
            st.selectbox("지역", ["전국"] + list(region_df["지역"]), key="region")
            selected_region = st.session_state["region"]

        region_fuel_sum = car_count_df.groupby("시도")[fuel_types].sum()
        heatmap_data = []
        for _, row in region_df.iterrows():
            region = row["지역"]
            lat = row["Latitude"]
            lon = row["Longitude"]
            value = (
                region_fuel_sum.at[region, selected_fuel]
                if region in region_fuel_sum.index
                else 0
            )
            value = 0 if pd.isna(value) else float(value)
            heatmap_data.append([lat, lon, value])

        if selected_region == "전국":
            heatmap = folium.Map(location=[36.5, 127.8], zoom_start=7)

            for _, row in region_df.iterrows():
                region = row["지역"]
                lat = row["Latitude"]
                lon = row["Longitude"]
                gasoline = (
                    region_fuel_sum.at[region, "휘발유"]
                    if region in region_fuel_sum.index
                    else 0
                )
                diesel = (
                    region_fuel_sum.at[region, "경유"]
                    if region in region_fuel_sum.index
                    else 0
                )
                lpg = (
                    region_fuel_sum.at[region, "LPG"]
                    if region in region_fuel_sum.index
                    else 0
                )
                folium.Marker(
                    location=[lat, lon],
                    tooltip=folium.Tooltip(
                        f"<div style='min-width: max-content;'>{region}<br/><strong>휘발유:</strong> {gasoline:,}<br/><strong>경유:</strong> {diesel:,}<br/><strong>LPG:</strong> {lpg:,}</div>"
                    ),
                    icon=folium.Icon(color="blue", icon="car", prefix="fa"),
                ).add_to(heatmap)
        else:
            row = region_df[region_df["지역"] == selected_region].iloc[0]
            lat = row["Latitude"]
            lon = row["Longitude"]

            map_center = [lat, lon]

            heatmap = folium.Map(location=map_center, zoom_start=10)

            gasoline = (
                region_fuel_sum.at[selected_region, "휘발유"]
                if selected_region in region_fuel_sum.index
                else 0
            )
            diesel = (
                region_fuel_sum.at[selected_region, "경유"]
                if selected_region in region_fuel_sum.index
                else 0
            )
            lpg = (
                region_fuel_sum.at[selected_region, "LPG"]
                if selected_region in region_fuel_sum.index
                else 0
            )
            folium.Marker(
                location=[lat, lon],
                tooltip=folium.Tooltip(
                    f"<div style='min-width: max-content;'>{selected_region}<br/><strong>휘발유:</strong> {gasoline:,}<br/><strong>경유:</strong> {diesel:,}<br/><strong>LPG:</strong> {lpg:,}</div>"
                ),
                icon=folium.Icon(color="blue", icon="car", prefix="fa"),
            ).add_to(heatmap)

        HeatMap(heatmap_data).add_to(heatmap)
        st_folium(heatmap, height=400, use_container_width=True)
