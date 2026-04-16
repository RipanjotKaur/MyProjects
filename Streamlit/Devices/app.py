import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(layout='wide', page_title='Certn Devices')

# ---- SUPABASE CONNECTION ----
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.success("✅ Supabase connected!")
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
    st.stop()
# ---- LOAD DATA FROM SUPABASE ----
@st.cache_data(ttl=10)
def load_data():
    response = supabase.table("devices").select("*").execute()
    df = pd.DataFrame(response.data)
    # Drop supabase system columns
    df = df.drop(columns=["id", "created_at"], errors="ignore")
    df.index = df.index + 1
    return df

df = load_data()

# ---- NAVIGATION ----
page = st.sidebar.selectbox("Navigate", ["🔍 Filter Devices", "📊 General Analysis", "➕ Add New Device"])

# ---- FILTER DEVICES ----
if page == "🔍 Filter Devices":
    st.title("Certn Devices")
    st.sidebar.title("🔍 Filter Devices")

    check_device = st.sidebar.selectbox("Select One", [
        "Search the devices on conditions",
        "Search by Serial Number"
    ])

    if check_device == "Search the devices on conditions":
        brand = st.sidebar.selectbox("Select Brand", ["All"] + list(df["Brand"].unique()))
        warranty = st.sidebar.selectbox("Select UnderWarranty", ["All"] + list(df["UnderWarranty"].unique()))
        condition = st.sidebar.selectbox("Used or Not", ["All"] + list(df["Used"].unique()))
        status = st.sidebar.selectbox("Available devices", ["All"] + list(df["Status"].unique()))

    elif check_device == "Search by Serial Number":
        serial = st.sidebar.text_input("Search Serial Number")

    search_clicked = st.sidebar.button("🔍 Search")

    if search_clicked:
        result = df.copy()

        if check_device == "Search the devices on conditions":
            if brand != "All":
                result = result[result["Brand"] == brand]
            if warranty != "All":
                result = result[result["UnderWarranty"] == warranty]
            if condition != "All":
                result = result[result["Used"] == condition]
            if status != "All":
                result = result[result["Status"] == status]

        elif check_device == "Search by Serial Number":
            result = result[result["Serial Number"] == serial]
            if len(result) == 0:
                st.warning("⚠️ No device found!")

        result = result.reset_index(drop=True)
        result.index += 1
        st.dataframe(result)

    else:
        st.dataframe(df)

# ---- GENERAL ANALYSIS ----
elif page == "📊 General Analysis":
    st.title("Analysis of Certn Devices")
    st.sidebar.title("📊 General Analysis")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔵 Devices by Status")
        status_count = df["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]
        st.bar_chart(status_count.set_index("Status"))

    with col2:
        st.subheader("📦 Devices by Brand")
        brand_count = df["Brand"].value_counts().reset_index()
        brand_count.columns = ["Brand", "Count"]
        st.bar_chart(brand_count.set_index("Brand"))

    with col3:
        st.subheader("Used Devices")
        used_count = df["Used"].value_counts().reset_index()
        used_count.columns = ["Used", "Count"]
        st.bar_chart(used_count.set_index("Used"))

# ---- ADD NEW DEVICE ----
elif page == "➕ Add New Device":
    st.title("➕ Add New Device")

    serial = st.text_input("Serial Number", placeholder="e.g. WYUBTIGMN")
    brand = st.selectbox("Brand", ["LENOVO", "MACBOOK PRO", "MACBOOK AIR"])
    used = st.selectbox("Used?", ["NO", "YES"])
    status = st.selectbox("Status", ["Available", "Not Available"])
    warranty = st.selectbox("Under Warranty?", ["YES", "NO"])
    ram = st.text_input("Please enter RAM of the device", placeholder="e.g. 32GB")
    ssd = st.text_input("Please enter SSD of the device", placeholder="e.g. 16GB")

    add_clicked = st.button("💾 Save Device")

    if add_clicked:
        if serial == "":
            st.warning("⚠️ Please enter a Serial Number!")
        else:
            new_device = {
                "Serial Number": serial,
                "Brand": brand,
                "Used": used,
                "Status": status,
                "UnderWarranty": warranty,
                "RAM": ram,
                "SSD": ssd,
            }
            supabase.table("devices").insert(new_device).execute()
            st.success("✅ Device added successfully!")
            st.cache_data.clear()  # Refresh data