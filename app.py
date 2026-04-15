import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide',page_title='Certn Devices')

# Load data
df = pd.read_csv("DevicesHealth.csv")

df.index = df.index + 1
page = st.sidebar.selectbox("Navigate", ["🔍 Filter Devices", "📊 General Analysis", "➕ Add New Device" ])

if page == "🔍 Filter Devices":
    st.title("Certn Devices")
# ---- SIDEBAR ----
    st.sidebar.title("🔍 Filter Devices")

    check_device = st.sidebar.selectbox("Select One", [
    "Search the devices on conditions",
    "Search by Serial Number"
])

# ---- FILTERS BEFORE BUTTON ----
    if check_device == "Search the devices on conditions":
        brand = st.sidebar.selectbox("Select Brand", ["All"] + list(df["Brand"].unique()))
        warranty = st.sidebar.selectbox("Select UnderWarranty", ["All"] + list(df["UnderWarranty"].unique()))
        condition = st.sidebar.selectbox("Used or Not", ["All"] + list(df["Used"].unique()))
        status = st.sidebar.selectbox("Available devices", ["All"] + list(df["Status"].unique()))
        
    elif check_device == "Search by Serial Number":
        serial = st.sidebar.text_input("Search Serial Number")

# ---- BUTTON ----
    search_clicked = st.sidebar.button("🔍 Search")

# ---- FILTERING LOGIC ----
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

elif page == "📊 General Analysis":
    st.title("Analysis of Certn Devices")
    st.sidebar.title("📊 General Analysis")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔵 Devices by Status")
        status_count = df["Status"].value_counts()

        fig1, ax1 = plt.subplots(figsize=(4,4))
        ax1.pie(status_count, labels=status_count.index, autopct="%0.01f%%")
        ax1.set_title("Device Status")
        st.pyplot(fig1, use_container_width=False)

    with col2:
        st.subheader("📦 Devices by Brand")
        brand_count = df["Brand"].value_counts()

        fig2, ax2 = plt.subplots(figsize=(4,4))
        ax2.bar(brand_count.index, brand_count.values, color="skyblue")
        ax2.set_xlabel("Brand")
        ax2.set_ylabel("Count")
        st.pyplot(fig2, use_container_width=False)
    with col3:
        st.subheader("Used Devices")
        Used_count = df["Used"].value_counts()
        fig3, ax3 = plt.subplots(figsize=(4,4))
        ax3.bar(Used_count.index, Used_count.values, color="skyblue")
        ax3.set_xlabel("Used")
        ax3.set_ylabel("Count")
        st.pyplot(fig3, use_container_width=False)

elif page == "➕ Add New Device":
    st.title("➕ Add New Device")

    # ---- INPUT FIELDS ----
    serial = st.text_input("Serial Number",placeholder="e.g. WYUBTIGMN")
    brand = st.selectbox("Brand",["LENOVO", "MACBOOK PRO","MACBOOK AIR"] )
    used = st.selectbox("Used?", ["NO", "YES"])
    status = st.selectbox("Status", ["Available", "Not Available"])
    warranty = st.selectbox("Under Warranty?", ["YES", "NO"])
    ram = st.text_input("Please enter RAM of the device",placeholder="e.g. 32GB")  
    ssd = st.text_input("Please enter SSD of the device", placeholder="e.g. 16GB")                       
    

    # ---- SAVE BUTTON ----
    add_clicked = st.button("💾 Save Device")
    if add_clicked:

        # Check all fields are filled
        if serial == "":
            st.warning("⚠️ Please fill all fields!")

        # Create new row
        new_row = {
                "Serial Number": serial,
                "Brand": brand,
                "Used": used,
                "Status": status,
                "UnderWarranty": warranty,
                "RAM" : ram,
                "SSD" : ssd,
                "Assigned To": assigned_to
        }

        # Add to dataframe
        new_df = pd.DataFrame([new_row])

        # ✅ Append to CSV
        new_df.to_csv("DevicesHealth.csv", mode="a", header=False, index=False)

        st.success("The device is added successfully!")