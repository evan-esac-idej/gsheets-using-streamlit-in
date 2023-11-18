import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title('Vendor Management Portal')
st.markdown('Enter the details of the new vendor below.')

# Establishing a Google Sheets Connection
conn = st.experimental_connection('gsheets', type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet='Vendors', usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how='all')

# List of Business Types and Products
BUSINESS_TYPES = [
    'Manufacturer',
    'Distributor',
    'Wholesaler',
    'Retalier',
    'Service provider',
]
PRODUCTS = [
    'Electronis',
    'Apparel',
    'Graceries',
    'Software',
    'Other',
]

# Onboarding New Vendor Form
with st.form(key='vendor_form'):
    company_name = st.text_input(label='Company Name')
    business_type = st.selectbox('Business Type*', options=BUSINESS_TYPES, index=None)
    products = st.multiselect('Products Offered', options=PRODUCTS)
    years_in_business = st.slider('Years in Business', 0, 50, 5)
    onboarding_date = st.date_input(label='Onboarding Date')
    additional_info = st.text_area(label='Additional Notes')

    # Mark mandatory fields
    st.markdown('**required*')

    submit_button = st.form_submit_button(label='Submit Vendor Details')

    # if the submit button is pressed
    if submit_button:
        if not company_name or not business_type:
            st.warning('Ensure all mandatory fields are filled')
            st.stop()
        elif existing_data['CompanyName'].str.contains(company_name).any():
            st.warning('A vendor with this company name already exists.')
            st.stop()
        else:
            vendor_data = pd.DataFrame(
                [
                    {
                        'CompanyName': company_name,
                        'BusinessType': business_type,
                        'Products': ', '.join(products),
                        'YearsInBusiness': years_in_business,
                        'OnboardingDate': onboarding_date.strftime('%Y-%m-%d'),
                        'Additionalinfo': additional_info,
                    }
                ]
            )

            # Add the new vendor data to the existing date
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor date
            conn.update(worksheet='Vendors', data=updated_df)

            st.success('Vendor datails successfully submitted!')


