
import os
import json
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import mysql.connector
import requests


sql_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "gayathri@123",
    database = "phonepe"
)

sqlcursor = sql_connection.cursor()

sqlcursor.execute("SELECT *FROM aggregated_transaction;")
at_table = sqlcursor.fetchall()
sql_connection.commit()

sqlcursor.close()
sql_connection.close()


AT = pd.DataFrame(at_table, columns = ("States", "Years", "Quarter", "Transaction_type",
                                       "Transaction_count", "Transaction_amount"))

sql_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "gayathri@123",
    database = "phonepe"
)

sqlcursor = sql_connection.cursor()

sqlcursor.execute("SELECT *FROM aggregated_user;")
at_table = sqlcursor.fetchall()
sql_connection.commit()

sqlcursor.close()
sql_connection.close()

AU = pd.DataFrame(at_table, columns = ("States", "Years", "Quarter", "Brands",
                                       "Transaction_count", "Percentage"))

sql_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "gayathri@123",
    database = "phonepe"
)

sqlcursor = sql_connection.cursor()

sqlcursor.execute("SELECT *FROM map_transaction;")
at_table = sqlcursor.fetchall()
sql_connection.commit()

sqlcursor.close()
sql_connection.close()

MT = pd.DataFrame(at_table, columns = ("States", "Years", "Quarter", "Districts",
                                       "Transaction_count", "Transaction_amount"))

sql_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "gayathri@123",
    database = "phonepe"
)

sqlcursor = sql_connection.cursor()

sqlcursor.execute("SELECT *FROM map_user;")
at_table = sqlcursor.fetchall()
sql_connection.commit()

sqlcursor.close()
sql_connection.close()

MU = pd.DataFrame(at_table, columns = ("States", "Years", "Quarter", "Districts",
                                       "Registered_Users", "App_Opens"))

sql_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "gayathri@123",
    database = "phonepe"
)

sqlcursor = sql_connection.cursor()

sqlcursor.execute("SELECT *FROM top_transaction;")
at_table = sqlcursor.fetchall()
sql_connection.commit()

sqlcursor.close()
sql_connection.close()


TT = pd.DataFrame(at_table, columns = ("States", "Years", "Quarter","Pincodes" , "Transaction_count",
                                       "Transaction_amount"))

sql_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "gayathri@123",
    database = "phonepe"
)

sqlcursor = sql_connection.cursor()

sqlcursor.execute("SELECT *FROM top_users;")
at_table = sqlcursor.fetchall()
sql_connection.commit()

sqlcursor.close()
sql_connection.close()


TU = pd.DataFrame(at_table, columns = ("States", "Years", "Quarter","Pincodes" ,"Registered_Users"))


def transaction_amount_count(df , year):
    graphs = df[df["Years"] == year]
    graphs.reset_index(drop=True, inplace=True)

    graphs_data = graphs.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    graphs_data.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:
        fig_amount = px.pie(graphs_data,
                            names="States",
                            values="Transaction_amount",
                            title=f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Purp,
                            width = 600)

        fig_amount.update_traces(textinfo='none')
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.pie(graphs_data,
                           names="States",
                           values="Transaction_count",
                           title=f"{year} TRANSACTION COUNT",
                           color_discrete_sequence=px.colors.sequential.Aggrnyl,
                           width =600)
        fig_count.update_traces(textinfo='none')
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)

    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states = []
        for i in data1["features"]:
            states.append(i["properties"]["ST_NM"])

        states.sort()

        fig1 = px.choropleth(graphs_data, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                             color="Transaction_amount", color_continuous_scale="Purples",
                             range_color=(graphs_data["Transaction_amount"].min(), graphs_data["Transaction_amount"].max()),
                             hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations", height=600,
                             width=600)
        fig1.update_geos(visible=False)
        st.plotly_chart(fig1)

    with col2:
        fig2 = px.choropleth(graphs_data, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                             color="Transaction_count", color_continuous_scale="Aggrnyl",
                             range_color=(graphs_data["Transaction_count"].min(), graphs_data["Transaction_count"].max()),
                             hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations", height=600,
                             width=600)
        fig2.update_geos(visible=False)
        st.plotly_chart(fig2)

    return graphs

def transaction_amount_count_q(df, quarter):
    graphs = df[df["Quarter"] == quarter]
    graphs.reset_index(drop=True, inplace=True)

    graphs_data = graphs.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    graphs_data.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.pie(graphs_data,
                            names="States",
                            values="Transaction_amount",
                            title=f"{graphs['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Purp,
                            width= 600)

        fig_amount.update_traces(textinfo='none')

        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.pie(graphs_data,
                           names="States",
                           values="Transaction_count",
                           title=f"{graphs['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                           color_discrete_sequence=px.colors.sequential.Aggrnyl,
                           width=600)
        fig_count.update_traces(textinfo='none')
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)

    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states = []
        for i in data1["features"]:
            states.append(i["properties"]["ST_NM"])

        states.sort()

        fig1 = px.choropleth(graphs_data, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                             color="Transaction_amount", color_continuous_scale="Purples",
                             range_color=(graphs_data["Transaction_amount"].min(), graphs_data["Transaction_amount"].max()),
                             hover_name="States", title=f"{graphs['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION AMOUNT",
                             fitbounds="locations", width=600)
        fig1.update_geos(visible=False)
        st.plotly_chart(fig1)

    with col2:
        fig2 = px.choropleth(graphs_data, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                             color="Transaction_count", color_continuous_scale="Aggrnyl",
                             range_color=(graphs_data["Transaction_count"].min(), graphs_data["Transaction_count"].max()),
                             hover_name="States", title=f"{graphs['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION COUNT",
                             fitbounds="locations", width=600)
        fig2.update_geos(visible=False)
        st.plotly_chart(fig2)

    return graphs


#AGGREGATED TRANSACTION
def agg_t(df, state):
    graphs1 = df[df["States"] == state]
    graphs1.reset_index(drop=True, inplace=True)

    graphs_data1 = graphs1.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    graphs_data1.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:
        fig3 = px.pie(graphs_data1,
                      names="Transaction_type",
                      values="Transaction_amount",
                      title=f"{state.upper()} TRANSACTION AMOUNT",
                      color_discrete_sequence=px.colors.sequential.Purp,
                      width=600)
        fig3.update_traces(textinfo='none')
        st.plotly_chart(fig3)

    with col2:
        fig4 = px.pie(graphs_data1,
                      names="Transaction_type",
                      values="Transaction_count",
                      title=f"{state.upper()} TRANSACTION COUNT",
                      color_discrete_sequence=px.colors.sequential.Aggrnyl,
                      width=600)
        fig4.update_traces(textinfo='none')
        st.plotly_chart(fig4)

#AGGREGATED USER
def aggre_u(df, year):
    agg_u = df[df["Years"] == year]
    agg_u.reset_index(drop=True, inplace=True)

    aggu_b = pd.DataFrame(agg_u.groupby("Brands")["Transaction_count"].sum())
    aggu_b.reset_index(inplace=True)

    fig5 = px.bar(aggu_b,
                  x="Brands",
                  y="Transaction_count",
                  title=f"{year} BRANDS AND TRANSACTION AMOUNT",
                  color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
                  width=1000)

    st.plotly_chart(fig5)

    return agg_u

def agg_u_q(df, quarter):
    graphs2 = df[df["Quarter"] == quarter]
    graphs2.reset_index(drop = True, inplace = True)

    graphs_data2 = pd.DataFrame(graphs2.groupby("Brands")["Transaction_count"].sum())
    graphs_data2.reset_index(inplace = True)

    fig6 = px.bar(graphs_data2, x = "Brands" , y = "Transaction_count", title = f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                   width = 1000 , color_discrete_sequence=px.colors.sequential.Aggrnyl_r,hover_name = "Brands")
    st.plotly_chart(fig6)

    return graphs2


def aggre_u_p(df, state):
    graphs3 = df[df["States"] == state]
    graphs3.reset_index(drop=True, inplace=True)

    fig7 = px.bar(graphs3, x="Brands", y="Transaction_count", title= f"{state.upper()} BRANDS AND TRANSACTION COUNT", width=1000 , color_discrete_sequence=px.colors.sequential.Aggrnyl_r)

    st.plotly_chart(fig7)


#MAP TRANSACTION
def map_t(df, state):
    graphs1 = df[df["States"] == state]
    graphs1.reset_index(drop=True, inplace=True)

    graphs_data1 = graphs1.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    graphs_data1.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:
        fig3 = px.pie(graphs_data1,
                      names="Districts",
                      values="Transaction_amount",
                      title=f"{state.upper()} TRANSACTION AMOUNT",
                      color_discrete_sequence=px.colors.sequential.Purp,
                      width=600)
        fig3.update_traces(textinfo='none')
        st.plotly_chart(fig3)

    with col2:
        fig4 = px.pie(graphs_data1,
                      names="Districts",
                      values="Transaction_count",
                      title=f"{state.upper()} TRANSACTION COUNT",
                      color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
                      width=600)
        fig4.update_traces(textinfo='none')
        st.plotly_chart(fig4)

#TOP TRANSACTION
def top_t(df, state):
    graphs1 = df[df["States"] == state]
    graphs1.reset_index(drop=True, inplace=True)

    graphs_data1 = graphs1.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    graphs_data1.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:
        fig3 = px.pie(graphs_data1,
                      names="Pincodes",
                      values="Transaction_amount",
                      title=f"{state.upper()} TRANSACTION AMOUNT",
                      color_discrete_sequence=px.colors.sequential.Purp,
                      width=600)
        fig3.update_traces(textinfo='none')
        st.plotly_chart(fig3)

    with col2:
        fig4 = px.pie(graphs_data1,
                      names="Pincodes",
                      values="Transaction_count",
                      title=f"{state.upper()} TRANSACTION COUNT",
                      color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
                      width=600)
        fig4.update_traces(textinfo='none')
        st.plotly_chart(fig4)

#MAP USER ANALYSIS
def map_u(df, year):
    graphs6 = df[df["Years"] == year]
    graphs6.reset_index(drop=True, inplace=True)

    graphs_data6 = graphs6.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    graphs_data6.reset_index(inplace=True)

    fig7 = px.line(graphs_data6, x="States", y=["Registered_Users", "App_Opens"],
                   title=f"{year} REGISTERED USER, APPOPENS", width=1000, height=800, markers=True,
                   color_discrete_sequence=px.colors.sequential.Purp)
    st.plotly_chart(fig7)

    return graphs6

def map_u_q(df, quarter):
    graphs7 = df[df["Quarter"] == quarter]
    graphs7.reset_index(drop=True, inplace=True)

    graphs_data7 = graphs7.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    graphs_data7.reset_index(inplace=True)

    fig8 = px.line(graphs_data7, x="States", y=["Registered_Users", "App_Opens"],
                   title=f"{df["Years"].min()} YEAR {quarter} QUARTER REGISTERED USER, APPOPENS", width=1000, height=800, markers=True,
                   color_discrete_sequence=px.colors.sequential.Purp)
    st.plotly_chart(fig8)

    return graphs7
def map_u_p(df, state):
    graphs9 = df[df["States"] == state]
    graphs9.reset_index(drop=True, inplace=True)

    fig7 = px.line(graphs9, x="Districts", y=["Registered_Users", "App_Opens"],
                   title="REGISTERED USERS, APPOPENS", width=1000, height=800, markers=True,
                   color_discrete_sequence=px.colors.sequential.Purp)
    st.plotly_chart(fig7)

#TOP USER ANALYSIS

def top_u(df, year):
    graphs6 = df[df["Years"] == year]
    graphs6.reset_index(drop=True, inplace=True)

    graphs_data6 = graphs6.groupby("States")[["Registered_Users"]].sum()
    graphs_data6.reset_index(inplace=True)

    fig_7 = px.treemap(graphs_data6, path=['States'], values='Registered_Users',
                             title=f"{year} Registered Users by State" )

    fig_7.update_layout(width=1000, height=800)

    st.plotly_chart(fig_7)

    return graphs6


def top_u_q(df, quarter):
    graphs7 = df[df["Quarter"] == quarter]
    graphs7.reset_index(drop=True, inplace=True)

    graphs_data7 = graphs7.groupby("States")[["Registered_Users"]].sum()
    graphs_data7.reset_index(inplace=True)

    fig_8 = px.treemap(graphs_data7, path=['States'], values='Registered_Users',
                             title=f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USERS")

    fig_8.update_layout(width=1000, height=800)

    st.plotly_chart(fig_8)

    return graphs7


def top_u_p(df, state):
    graphs9 = df[df["States"] == state]
    graphs9.reset_index(drop=True, inplace=True)

    fig_9 = px.treemap(graphs9, path=['Pincodes'], values='Registered_Users',
                             title=f"{state.upper()} PINCODE WISE REGISTERED USERS")

    fig_9.update_layout(width=600)

    st.plotly_chart(fig_9)


#UI INTERFACE

st.set_page_config(layout = "wide")
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-color: #5f309c;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("<h1 style='color: white;'>PhonePe</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: white;'>DATA VISUALIZATION AND EXPLORATION</h3>", unsafe_allow_html=True)



with st.sidebar:
    select = option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "DASHBOARD Q&A"])

if select == "HOME":
    pass
elif select == "DATA EXPLORATION":
    tab1 , tab2 , tab3 = st.tabs(["Aggregated", "Map", "Top"])

    with tab1:
        method = st.radio("Choose", ["Aggregated Transaction", "Aggregated User"])

        if method == "Aggregated Transaction":
            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",AT["Years"].unique())
            t = transaction_amount_count(AT, years)

            col1, col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the quarter",t["Quarter"].unique())
            tt = transaction_amount_count_q(t,quarter)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the state", tt["States"].unique())
            agg_t(tt, state)

        elif method == "Aggregated User":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the Year", AU["Years"].unique())
            aggre_user = aggre_u(AU, years)

            col1, col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the quarter", aggre_user["Quarter"].unique())
            aggregated_user_q = agg_u_q(aggre_user, quarter)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the state", aggregated_user_q["States"].unique())
            aggre_u_p(aggregated_user_q, state)

    with tab2:
        method = st.radio("Choose", ["Map Transaction", "Map User"])

        if method == "Map Transaction":
            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year for map analysis", MT["Years"].unique())
            t = transaction_amount_count(MT, years)

            col1, col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the quarter for map analysis", t["Quarter"].unique())
            tt = transaction_amount_count_q(t, quarter)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the state for map analysis", tt["States"].unique())
            map_t(tt, state)


        elif method == "Map User":
            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year for map analysis", MU["Years"].unique())
            t = map_u(MU, str(years))

            col1, col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the quarter for map analysis", t["Quarter"].unique())
            tt = map_u_q(t, quarter)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the state for map analysis", tt["States"].unique())
            map_u_p(tt, state)


    with tab3:
        method = st.radio("Choose", ["Top Transaction", "Top User"])

        if method == "Top Transaction":
            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year for top analysis", TT["Years"].unique())
            t = transaction_amount_count(TT, years)

            col1, col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the quarter for top analysis", t["Quarter"].unique())
            tt = transaction_amount_count_q(t, quarter)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the state for top analysis", tt["States"].unique())
            top_t(tt, state)

        elif method == "Top User":
            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year for top analysis", TU["Years"].unique())
            t1 = top_u(TU, str(years))

            col1, col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the quarter for top analysis", t["Quarter"].unique())
            tt = top_u_q(t1, quarter)

            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the state for top analysis", tt["States"].unique())
            top_u_p(tt, state)

elif select == "DASHBOARD Q&A":
    sql_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="gayathri@123",
        database="phonepe"
    )

    sqlcursor = sql_connection.cursor()
    question = st.selectbox("Select a question:",["1.Show me the total sum of transaction amount of each state in Aggregated Transaction",
                                                  "2.Show me the total sum of transaction count of each state in Aggregated Transaction",
                                                  "3.Show me the total average of transaction amount of each state in Map Transaction",
                                                  "4.Show me the total average of transaction count of each state in Map Transaction",
                                                  "5.Show me the total sum of transaction amount of each state in Top Transaction",
                                                  "6.Show me the total sum of transaction count of each state in Top Transaction",
                                                  "7.Show me the total sum of each brand's transaction count in Aggregated User",
                                                  "8.Show me the each state's total Registered users in Map User",
                                                  "9.Show me the each state's total Registered users in Top User",
                                                  "10.Show me the total registered users in each pincode of a state"
                                                  ])

    if question.startswith("1."):
        query1 = '''select states, SUM(transaction_amount) AS transaction_amount
                    from aggregated_transaction
                    group by states
                    order by Transaction_amount DESC;
                 '''
        sqlcursor.execute(query1)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table , columns = ("states", "transaction_amount"))


        fig = px.pie(df_1, values='transaction_amount', names='states', title='Aggregated Transaction Amount by State',
                     width=1000,height = 800,color_discrete_sequence=px.colors.sequential.Purples,hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)

    elif question.startswith("2."):
        query2 = '''select states, SUM(transaction_count) AS transaction_count
                    from aggregated_transaction
                    group by states
                    order by Transaction_count DESC;
                 '''
        sqlcursor.execute(query2)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("states", "transaction_count"))

        fig = px.pie(df_1, values='transaction_count', names='states', title='Aggregated Transaction count by State',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.Purples, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)

    elif question.startswith("3."):
        query3 = '''select states, AVG(transaction_amount) AS transaction_amount
                    from map_transaction
                    group by states
                    order by Transaction_amount DESC;
                 '''
        sqlcursor.execute(query3)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("states", "transaction_amount"))

        fig = px.pie(df_1, values='transaction_amount', names='states', title='Map Transaction amount by State',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.GnBu, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)

    elif question.startswith("4."):
        query4 = '''select states, AVG(transaction_count) AS transaction_count
                    from map_transaction
                    group by states
                    order by Transaction_count DESC;
                 '''
        sqlcursor.execute(query4)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("states", "transaction_count"))

        fig = px.pie(df_1, values='transaction_count', names='states', title='Map Transaction count by State',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.GnBu, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)

    elif question.startswith("5."):
        query5 = '''select states, SUM(transaction_amount) AS transaction_amount
                    from top_transaction
                    group by states
                    order by Transaction_amount DESC;
                 '''
        sqlcursor.execute(query5)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("states", "transaction_amount"))

        fig = px.pie(df_1, values='transaction_amount', names='states', title='Top Transaction amount by State',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.YlOrBr, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)

    elif question.startswith("6."):
        query6 = '''select states, SUM(transaction_count) AS transaction_count
                    from top_transaction
                    group by states
                    order by Transaction_count DESC;
                 '''
        sqlcursor.execute(query6)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("states", "transaction_count"))

        fig = px.pie(df_1, values='transaction_count', names='states', title='Top Transaction count by State',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.YlOrBr, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)


    elif question.startswith("7."):
        query7 = '''select brands, 	sum(transaction_count) AS transaction_count
                    from aggregated_user
                    group by brands
                    order by Transaction_count DESC;
                 '''
        sqlcursor.execute(query7)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("brands", "transaction_count"))

        fig = px.pie(df_1, values='transaction_count', names='brands', title='Transaction count of each Brand',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.Plasma, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)

    elif question.startswith("8."):
        query8 = '''select States, sum(Registered_Users) AS Registered_Users
                    from map_user
                    group by States
                    order by Registered_Users DESC;
                '''
        sqlcursor.execute(query8)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("states", "registered_users"))

        fig = px.pie(df_1, values='registered_users', names='states', title='Registered users of each state',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.Plasma, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)

    elif question.startswith("9."):
        query9 = '''select States, sum(Registered_Users) AS Registered_Users
                    from top_users
                    group by States
                    order by Registered_Users DESC;
                '''
        sqlcursor.execute(query9)
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("states", "registered_users"))

        fig = px.pie(df_1, values='registered_users', names='states', title='Registered users of each state',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.Plasma, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)

    elif question.startswith("10."):
        unique_states = TU["States"].unique().tolist()
        state = st.selectbox("select state",unique_states)
        query10 = '''select pincodes, sum(Registered_Users) AS Registered_Users
                    from top_users
                    where states = %s
                    group by pincodes
                    order by Registered_Users DESC;
                  '''
        sqlcursor.execute(query10,(state,))
        table = sqlcursor.fetchall()
        sql_connection.commit()

        df_1 = pd.DataFrame(table, columns=("pincodes", "registered_users"))

        fig = px.pie(df_1, values='registered_users', names='pincodes', title=f'Registered users of each pincode area of {state}',
                     width=1000, height=800, color_discrete_sequence=px.colors.sequential.Plasma, hole=0.3)
        fig.update_traces(textinfo='none')
        st.plotly_chart(fig)