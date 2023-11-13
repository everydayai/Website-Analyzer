import streamlit as st

# Sample database of neighborhoods (replace with real data)
neighborhood_data = {
    'Neighborhood A': {'price_range': (300000, 500000), 'amenities': {'school': 2, 'park': 5}, 'distance': 10},
    'Neighborhood B': {'price_range': (200000, 400000), 'amenities': {'school': 5, 'supermarket': 3}, 'distance': 5},
    # Add more neighborhoods...
}

def match_neighborhoods(price_range, amenities, max_distance):
    matches = []
    for name, data in neighborhood_data.items():
        if data['price_range'][0] <= price_range[1] and data['price_range'][1] >= price_range[0]:
            if all(amenity in data['amenities'] and data['amenities'][amenity] <= max_distance for amenity in amenities):
                matches.append(name)
    return matches

st.title('Neighborhood Matchmaker')

min_price, max_price = st.slider("Select your price range", 100000, 1000000, (200000, 500000))
selected_amenities = st.multiselect("Select desired amenities", ['school', 'park', 'supermarket', 'public transport'])
max_distance = st.selectbox("Maximum distance to amenities (in miles)", [1, 2, 5, 10, 20])

if st.button('Find Match'):
    matches = match_neighborhoods((min_price, max_price), selected_amenities, max_distance)
    if matches:
        st.write('Matching Neighborhoods:')
        for match in matches:
            st.write(match)
    else:
        st.write('No matches found. Try adjusting your criteria.')

# Remember to handle user data responsibly.
