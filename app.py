import streamlit as st
import pandas as pd
from datetime import date

# --- PAGE SETUP ---
st.set_page_config(page_title="Dubai Luxe Real Estate", page_icon="🏢", layout="wide")

# --- DUMMY DATABASE (Using Session State so data stays while the app is running) ---
if 'properties' not in st.session_state:
    st.session_state.properties = [
        {"id": 1, "type": "For Sale", "category": "Villa", "location": "Palm Jumeirah", "price": "15,000,000 AED", "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=500"},
        {"id": 2, "type": "For Rent", "category": "Apartment", "location": "Downtown Dubai", "price": "120,000 AED/year", "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=500"}
    ]

if 'clients' not in st.session_state:
    st.session_state.clients = pd.DataFrame(columns=["Name", "Age", "DOB", "Address", "Interested In"])

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 Dubai Luxe Admin")
menu = st.sidebar.radio("Navigation", ["🏠 View Properties", "➕ Add New Property", "👥 Client Database"])

# --- PAGE 1: VIEW PROPERTIES ---
if menu == "🏠 View Properties":
    st.title("Available Properties in Dubai")
    st.write("Browse our current listings for sale and rent.")
    
    # Create columns for a grid layout
    cols = st.columns(2)
    for index, prop in enumerate(st.session_state.properties):
        with cols[index % 2]:
            st.image(prop["image"], width="stretch")
            st.subheader(f"{prop['category']} in {prop['location']}")
            st.write(f"**Status:** {prop['type']}")
            st.write(f"**Price:** {prop['price']}")
            st.button(f"View Details ##{prop['id']}", key=f"btn_{prop['id']}")
            st.divider()

# --- PAGE 2: ADD PROPERTY ---
elif menu == "➕ Add New Property":
    st.title("Add a New Listing")
    
    with st.form("property_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            prop_type = st.selectbox("Status", ["For Sale", "For Rent"])
            prop_category = st.selectbox("Property Type", ["Apartment", "Villa", "Townhouse", "Penthouse"])
        with col2:
            prop_location = st.text_input("Location (e.g., Dubai Marina)")
            prop_price = st.text_input("Price (AED)")
            
        prop_image = st.text_input("Image URL (Paste an image link here)")
        
        submitted = st.form_submit_button("Publish Listing")
        
        if submitted:
            new_prop = {
                "id": len(st.session_state.properties) + 1,
                "type": prop_type,
                "category": prop_category,
                "location": prop_location,
                "price": prop_price,
                "image": prop_image if prop_image else "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=500"
            }
            st.session_state.properties.append(new_prop)
            st.success("Property added successfully! Go to 'View Properties' to see it.")

# --- PAGE 3: CLIENT DATABASE ---
elif menu == "👥 Client Database":
    st.title("Client CRM System")
    st.write("Manage your buyers, renters, and leads.")
    
    with st.expander("➕ Add New Client"):
        with st.form("client_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                client_name = st.text_input("Full Name")
                client_dob = st.date_input("Date of Birth", min_value=date(1920, 1, 1), max_value=date.today())
                client_age = st.number_input("Age", min_value=18, max_value=100, step=1)
            with col2:
                client_interest = st.selectbox("Looking for", ["Buying", "Renting"])
                client_address = st.text_area("Current Address")
                
            client_submit = st.form_submit_button("Save Client")
            
            if client_submit:
                new_client = pd.DataFrame([{
                    "Name": client_name, 
                    "Age": client_age, 
                    "DOB": client_dob.strftime("%Y-%m-%d"), 
                    "Address": client_address, 
                    "Interested In": client_interest
                }])
                st.session_state.clients = pd.concat([st.session_state.clients, new_client], ignore_index=True)
                st.success(f"{client_name} added to the database!")
                
    st.subheader("Current Client List")
    if not st.session_state.clients.empty:
        st.dataframe(st.session_state.clients, width="stretch")
    else:
        st.info("No clients added yet. Use the form above to add one.")