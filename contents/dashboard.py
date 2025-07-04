import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@st.cache_data
def load_data():
    # 파일 read
    FILE_PATH = "docs"
    # FILE_PATH = "/content/drive/MyDrive/5조"
    fuel_df = pd.read_csv(f"{FILE_PATH}/유류비.csv", encoding="CP949")
    car_count_df = pd.read_excel(f"{FILE_PATH}/시도별_연료별_등록현황.xlsx")
    region_df = pd.read_csv(f"{FILE_PATH}/지역별 좌표.csv")
    return fuel_df, car_count_df, region_df


# -------------------- 대시보드 함수 --------------------
def show_dashboard():
    fuel_df, car_count_df, region_df = load_data()

    with st.container():
        st.markdown("##### 연도별 등록대수 & 유류비 요약")

        # (a) 월 단위 총합 → 연도로 변환 → 연간 합계
        monthly_tot = (
            car_count_df.groupby("기준연월")[["휘발유", "경유", "LPG"]]
            .sum()
            .div(24)
            .reset_index()
        )
        monthly_tot["year"] = monthly_tot["기준연월"].str[:4].astype(int)
        yearly_tot = (
            monthly_tot.groupby("year")[["휘발유", "경유", "LPG"]].sum().reset_index()
        )

        # (a) 연도 컬럼 추가 → 연도별 평균
        fuel_df["year"] = fuel_df["yearmonth"].str[:4].astype(int)
        yearly_cost = fuel_df.groupby(["year", "fueltype"])["cost"].mean().reset_index()

        # pivot 후 순서 강제
        yearly_cost_pivot = yearly_cost.pivot(
            index="year", columns="fueltype", values="cost"
        ).reset_index()
        yearly_cost_pivot = yearly_cost_pivot[["year", "휘발유", "경유", "LPG"]]

        df = pd.merge(yearly_tot, yearly_cost_pivot, on="year", how="inner")
        df.columns = [
            "연도",
            "휘발유 등록수",
            "경유 등록수",
            "LPG 등록수",
            "휘발유 유류비",
            "경유 유류비",
            "LPG 유류비",
        ]

        # st.dataframe(df.set_index('연도'))

        # Plotly를 사용한 이중 축 그래프
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # (1) 왼쪽 축: 스택드 바 (등록수)
        fig.add_trace(
            go.Bar(
                x=df["연도"],
                y=df["휘발유 등록수"],
                name="휘발유 등록수",
                marker_color="#F4A7A7",
                legendgroup="bar",
                legendgrouptitle_text="등록대수",
                xaxis="x",
                yaxis="y",
                hovertemplate="<b>%{x}년</b><br>"
                + "<b style='color: #F4A7A7;'>휘발유 등록수:</b> %{y:,.0f}대<br>"
                + "<extra></extra>",
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Bar(
                x=df["연도"],
                y=df["경유 등록수"],
                name="경유 등록수",
                marker_color="#9EC3E1",
                yaxis="y",
                legendgroup="bar",
                hovertemplate="<b>%{x}년</b><br>"
                + "<b style='color: #9EC3E1;'>경유 등록수:</b> %{y:,.0f}대<br>"
                + "<extra></extra>",
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Bar(
                x=df["연도"],
                y=df["LPG 등록수"],
                name="LPG 등록수",
                marker_color="#C6E2AE",
                yaxis="y",
                legendgroup="bar",
                hovertemplate="<b>%{x}년</b><br>"
                + "<b style='color: #C6E2AE;'>LPG 등록수:</b> %{y:,.0f}대<br>"
                + "<extra></extra>",
            ),
            secondary_y=False,
        )

        # (2) 오른쪽 축: 라인 (유류비)
        fig.add_trace(
            go.Scatter(
                x=df["연도"],
                y=df["휘발유 유류비"],
                name="휘발유 유류비",
                mode="lines+markers",
                line=dict(width=2),
                marker=dict(size=8, symbol="circle", color="blue"),
                yaxis="y2",
                legendgrouptitle_text="유류비",
                legendgroup="scatter",
                hovertemplate="<b>%{x}년</b><br>"
                + "<b style='color: blue;'>휘발유 유류비:</b> %{y:,.0f}원<br>"
                + "<extra></extra>",
            ),
            secondary_y=True,
        )
        fig.add_trace(
            go.Scatter(
                x=df["연도"],
                y=df["경유 유류비"],
                name="경유 유류비",
                mode="lines+markers",
                line=dict(width=2),
                marker=dict(size=8, symbol="square", color="orange"),
                yaxis="y2",
                legendgroup="scatter",
                hovertemplate="<b>%{x}년</b><br>"
                + "<b style='color: orange;'>경유 유류비:</b> %{y:,.0f}원<br>"
                + "<extra></extra>",
            ),
            secondary_y=True,
        )

        fig.add_trace(
            go.Scatter(
                x=df["연도"],
                y=df["LPG 유류비"],
                name="LPG 유류비",
                mode="lines+markers",
                line=dict(width=2),
                marker=dict(size=8, symbol="diamond", color="green"),
                yaxis="y2",
                legendgroup="scatter",
                hovertemplate="<b>%{x}년</b><br>"
                + "<b style='color: green;'>LPG 유류비:</b> %{y:,.0f}원<br>"
                + "<extra></extra>",
            ),
            secondary_y=True,
        )

        # 레이아웃 설정
        fig.update_layout(
            # title="연도별 등록대수 & 연평균 유류비",
            xaxis_title="연도",
            barmode="stack",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                xanchor="right",
                x=1,
                y=1.02,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1,
            ),
        )

        # Y축 레이블 설정
        fig.update_yaxes(title_text="등록대수", secondary_y=False)
        fig.update_yaxes(title_text="연평균 유류비 (원)", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown("##### 연료별 자동차 등록대수 구성비 변화")
        # 연도별 전체 등록대수 집계
        total_df = (
            car_count_df.groupby("기준연월")[["휘발유", "경유", "LPG"]]
            .sum()
            .reset_index()
        )

        # 스택 영역 차트 추가
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=total_df["기준연월"],
                y=total_df["LPG"],
                name="LPG",
                fill="tonexty",
                line=dict(color="#C6E2AE", width=0),
                fillcolor="rgba(198, 226, 174, 0.7)",
                hovertemplate="<b style='color: #C6E2AE;'>LPG:</b><br>"
                + "%{y:,.0f}대<br>"
                + "<extra></extra>",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=total_df["기준연월"],
                y=total_df["경유"],
                name="경유",
                fill="tonexty",
                line=dict(color="#9EC3E1", width=0),
                fillcolor="rgba(158, 195, 225, 0.7)",
                hovertemplate="<b style='color: #9EC3E1;'>경유:</b><br>"
                + "%{y:,.0f}대<br>"
                + "<extra></extra>",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=total_df["기준연월"],
                y=total_df["휘발유"],
                name="휘발유",
                fill="tonexty",
                line=dict(color="#F4A7A7", width=0),
                fillcolor="rgba(244, 167, 167, 0.7)",
                hovertemplate="<b style='color: #F4A7A7;'>휘발유:</b><br>"
                + "%{y:,.0f}대<br>"
                + "<extra></extra>",
            )
        )

        # 레이아웃 설정
        fig.update_layout(
            # title="연료별 자동차 등록대수 구성비 변화",
            xaxis_title="연도",
            yaxis_title="등록대수",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                xanchor="right",
                x=1,
                y=1.02,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1,
            ),
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)

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
