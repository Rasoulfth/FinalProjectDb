import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder


API_URL = "http://127.0.0.1:8000"

#pass
ADMIN_PASSWORD = "rasoul"  

@st.cache_data
def get_categories():
    response = requests.get(f"{API_URL}/categories/")
    if response.status_code == 200:
        return response.json()
    return []

def fetch_data(params={}):
    response = requests.get(f"{API_URL}/apps/", params=params)
    if response.status_code == 200:
        st.write(f"Query Time:{response.json()['time']}")
        #st.dataframe(pd.DataFrame(response.json()['data']))
        return pd.DataFrame(response.json()['data'])

    return pd.DataFrame()

# display dashbord 
def dashboard():
    st.title("Google Play Store Dashboard")

    # Search Filters
    categories = get_categories()
    selected_category = st.selectbox("Select Category", [""] + categories)
    min_rating = st.slider(" Minimum Rating", 0.0, 5.0, 0.0, 0.1)
    min_price = st.slider("Minimum Price", 0.0, 50.0, 0.0, 0.5)
    content_rating = st.selectbox(" Content Rating", ["", "Everyone", "Teen", "Mature"])

    params = {}
    if selected_category:
        params["category"] = selected_category
    if min_rating > 0:
        params["min_rating"] = min_rating
    if min_price > 0:
        params["min_price"] = min_price
    if content_rating:
        params["content_rating"] = content_rating
    params["free"] = False

    data = fetch_data(params)

    if not data.empty:
        st.write("**Search Results:**")
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_pagination(paginationPageSize=100)  
        grid_options = gb.build()
        AgGrid(data, gridOptions=grid_options)

    # show free app social
    st.subheader("Free Apps in 'Social' Category")
    social_apps = fetch_data({"category": "Social"})
    #st.write(social_apps)
    free_social_apps = social_apps[social_apps["free"] == 1]

    if not free_social_apps.empty:
        gb_free_social = GridOptionsBuilder.from_dataframe(free_social_apps)
        gb_free_social.configure_pagination(paginationPageSize=1000)  # Adjust page size as needed
        grid_options_free_social = gb_free_social.build()
        AgGrid(free_social_apps, gridOptions=grid_options_free_social)

    # released last updated 
    st.subheader("Release & Last Updated Trends")
    if selected_category:
        category_apps = fetch_data({"category": selected_category})
        if not category_apps.empty:
            category_apps["released"] = pd.to_datetime(category_apps["released"], errors="coerce")
            category_apps["last_updated"] = pd.to_datetime(category_apps["last_updated"], errors="coerce")

            yearly_released = category_apps.groupby(category_apps["released"].dt.year).size().reset_index(name="count")
            yearly_updated = category_apps.groupby(category_apps["last_updated"].dt.year).size().reset_index(name="count")

            fig_released = px.line(yearly_released, x="released", y="count", title=" Apps Released Per Year")
            fig_updated = px.line(yearly_updated, x="last_updated", y="count", title=" Apps Last Updated Per Year")

            st.plotly_chart(fig_released)
            st.plotly_chart(fig_updated)

    # Average rating
    st.subheader("Average Rating Per Category")
    all_data = fetch_data()
    if not all_data.empty:
        category_ratings = all_data.groupby("category_name")["rating"].mean().reset_index()
        fig_avg_rating = px.bar(category_ratings, x="category_name", y="rating", title="Average Rating by Category")
        st.plotly_chart(fig_avg_rating)

#  Admin Panel
def admin_panel():
    st.title(" Admin Panel (CRUD Operations)")

    # Password Authentication
    password = st.text_input("Enter Admin Password", type="password")
    if password != ADMIN_PASSWORD:
        st.error(" Access Denied")
        return

    st.success("Access Granted")

    # CRUd
    st.subheader("Create a New App")
    app_name = st.text_input("App Name")
    category = st.selectbox("Category", get_categories())
    rating = st.slider("Rating", 0.0, 5.0, 4.0, 0.1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    developer = st.text_input("Developer Name")

    if st.button("Add App"):
        app_data = {
            "app_name": app_name,
            "category": category,
            "rating": rating,
            "rating_count": 0,
            "installs": 1000,
            "min_installs": 500,
            "max_installs": 10000,
            "free": True if price == 0 else False,
            "price": price,
            "currency": "USD",
            "size": "10MB",
            "min_android": "5.0",
            "developer": developer,
            "released": "2024-01-01",
            "last_updated": "2024-06-01",
            "content_rating": "Everyone",
            "privacy_policy": "https://example.com/privacy",
            "ad_supported": True,
            "in_app_purchases": True,
            "editors_choice": False
        }
        response = requests.post(f"{API_URL}/apps/", json=app_data)
        if response.status_code == 201:
            st.success("App Added Successfully")
        else:
            st.error(f"Error: {response.text}")

    # DELETE
    st.subheader("🗑 Delete an App")
    app_id = st.text_input("Enter App ID to Delete")
    if st.button("Delete App"):
        response = requests.delete(f"{API_URL}/apps/{app_id}")
        if response.status_code == 204:
            st.success("App Deleted Successfully")
        else:
            st.error(f"Error: {response.text}")

# Main
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Admin Panel"])

    if page == "Dashboard":
        dashboard()
    elif page == "Admin Panel":
        admin_panel()

if __name__ == "__main__":
    main()
