import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv("airbnb.csv")

#Get the hotel details
def getHotelDetails(hotelDF):
    hotelList = {"listing_url": [], "name": [], "minimum_nights": [],
             "maximum_nights": [], "accommodates": [], "bedrooms": [],
             "beds": [], "bathrooms":[], "price": [], "security_deposit": [],
             "cleaning_fee": [], "extra_people": [], "guests_included": [],
             "images": [], "review_scores": [], "street": [], "suburb": [],
             "government_area":[], "market": [], "country": [], "amenities":[]}
    amenitiesTemp = []
    for index, row in hotelDF.iterrows():
        hotelList["listing_url"].append(row["listing_url"])
        hotelList["name"].append(row["name"])
        hotelList["minimum_nights"].append(row["minimum_nights"])
        hotelList["maximum_nights"].append(row["maximum_nights"])
        hotelList["accommodates"].append(row["accommodates"])
        hotelList["bedrooms"].append(row["bedrooms"])
        hotelList["beds"].append(row["beds"])
        hotelList["bathrooms"].append(row["bathrooms"])
        hotelList["price"].append(row["price"])
        hotelList["security_deposit"].append(row["security_deposit"])
        hotelList["cleaning_fee"].append(row["cleaning_fee"])
        hotelList["extra_people"].append(row["extra_people"])
        hotelList["guests_included"].append(row["guests_included"])
        hotelList["review_scores"].append(row["review_scores"])
        hotelList["images"].append(row["images"])
        hotelList["street"].append(row["street"])
        hotelList["suburb"].append(row["suburb"])
        hotelList["government_area"].append(row["government_area"])
        hotelList["market"].append(row["market"])
        hotelList["country"].append(row["country"])
        amenitiesTemp.append(row["amenities"])

    for i in range(len(amenitiesTemp)):        
        temp = amenitiesTemp[i]
        temp = temp.replace("[","")
        temp = temp.replace("]","")
        temp = temp.replace("'","")
        hotelList["amenities"].append(temp.split(","))
    return hotelList

#Displaying the property details for the selected criteria
def displayDetails(list1, i):
    st.divider()
    st.write(":rainbow[**Name of the Property:**]", list1["name"][i])
    st.write(":blue[**Cost of the stay:**]", list1["price"][i])
    st.write(":blue[**Review score:**]", list1["review_scores"][i])
    st.write(":blue[**Property Address:**]")
    st.write(list1["street"][i])
    st.write(list1["suburb"][i])
    st.write(list1["government_area"][i])
    st.write(":blue[**View the rooms by clicking the link:**]", list1["images"][i])
    with st.expander("For more details look here!!"):
        st.write(":blue[**Minimum stay nights:**]", list1["minimum_nights"][i])
        st.write(":blue[**Maximun stay nights:**]", list1["maximum_nights"][i])
        st.write(":blue[**Capacity:**]", list1["accommodates"][i])
        st.write(":blue[**Number of beds:**]", list1["beds"][i])
        st.write(":blue[**Number of bedrooms:**]", list1["bedrooms"][i])
        st.write(":blue[**Number of bathrooms:**]", list1["bathrooms"][i])
        st.write(":blue[**Advance security deposit to be paid:**]", list1["security_deposit"][i])
        st.write(":blue[**Cleaning Charges:**]", list1["cleaning_fee"][i])
        st.write(":blue[**Charges for extra people than allowed!:**]", list1["extra_people"][i])
        st.write(":blue[**Number of guests accepted:**]", list1["guests_included"][i])
        st.write(":blue[**Number of guests accepted:**]", list1["guests_included"][i])
        st.write(":blue[**Amenities available**]", list1["amenities"][i])

#Adding the review slider
def addReviewSlide(slideDF):
    minSlide = slideDF["review_scores"].min()
    maxSlide = slideDF["review_scores"].max()
    slideList = list(slideDF["review_scores"].unique())
    slideList.sort()
    if len(slideList) != 1:
        minval, maxval = st.select_slider("The review score Range",options = slideList, value =(minSlide,maxSlide), key = "ss4")
        dfMin = slideDF[slideDF["review_scores"] >= minval]
        dfMin.reset_index(drop= True, inplace= True)
        reviewDF = dfMin[dfMin["price"] <= maxval]
        reviewDF.reset_index(drop= True, inplace= True)
    else:
        slide = st.slider("The review score Range", max_value = maxRate, value = maxRate, disabled = True)
        reviewDF = slideDF[slideDF["review_scores"] == slide]
        reviewDF.reset_index(drop= True, inplace= True)
    return reviewDF

#Streamlit Designing Part
st.set_page_config(page_title= "Airbnb Analysis",
                   layout= "wide",
                   initial_sidebar_state= "expanded")

str1 = """Airbnb is an American company operating an online marketplace for short- and long-term homestays and experiences.
The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky,
Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com.
Airbnb is the most well-known company for short-term housing rentals."""
with st.sidebar:
    img1 = Image.open("airbnb.jpg")
    st.image(img1,width = 250)
    #st.write(str1)

st.header(":rainbow[Airbnb Analysis]")
menuOption = option_menu(None, ["Property Search", "Tasks", 'Settings'],
                         icons=['search', "list-task", 'gear'],
                         menu_icon="cast", default_index=0, orientation="horizontal",
                         styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "2px", "--hover-color": "#00AABB"},
                               "icon": {"font-size": "15px"},
                               "container" : {"max-width": "8000px"},
                               "nav-link-selected": {"background-color": "#00BB00"}})

if menuOption == "Property Search":
    tab1, tab2 = st.tabs([":blue[Property Selection]", ":blue[Property Analysis]"])
    with tab1:
        countryList = list(df["country"].unique())
        countryList.sort()
        country = st.selectbox("Select the country", options = countryList, index = None, placeholder = "select the option")
        if country != None:
            df1= df[df["country"] == country]
            df1.reset_index(drop= True, inplace= True)
            roomType = ["Entire home/apt", "Shared Room", "Private Room"]
            roomOption = st.radio("Select the type of room you are looking for!!", roomType, horizontal = True)
            if roomOption == "Private Room":
                privateDF = (df1[df1["room_type"] == "Private room"])
                privateDF.reset_index(drop= True, inplace= True)
                with st.sidebar:
                    propertyList1 = list(privateDF["property_type"].unique())
                    propertyList1.sort()
                    propertyOption1 = st.multiselect("Select the Propery Type!!", propertyList1, default = propertyList1[0])
                    if len(propertyOption1) > 0:
                        private_propDF = privateDF[privateDF["property_type"] == propertyOption1[0]]
                        private_propDF.reset_index(drop= True, inplace= True)
                        for i in range(1,len(propertyOption1)):
                            tempDF = privateDF[privateDF["property_type"] == propertyOption1[i]]
                            private_propDF= pd.concat([private_propDF, tempDF], axis=0, ignore_index=True)
                            private_propDF.reset_index(drop= True, inplace= True)
                        try:
                            bedList1 = list(private_propDF["bed_type"].unique())
                            bedList1.sort()
                            bedOption1 = st.multiselect("Select the Bed Type!!", bedList1, default = bedList1[0])
                            private_bedDF = private_propDF[private_propDF["bed_type"] == bedOption1[0]]
                            private_bedDF.reset_index(drop= True, inplace= True)
                            for i in range(1,len(bedOption1)):
                                tempDF = private_propDF[private_propDF["bed_type"] == bedOption1[i]]
                                private_bedDF= pd.concat([private_bedDF, tempDF], axis=0, ignore_index=True)
                                private_bedDF.reset_index(drop= True, inplace= True)
                            cancelList1 = list(private_bedDF["cancellation_policy"].unique())
                            cancelList1.sort()
                            cancelOption1 = st.radio("Available Cancellation Policy. Select the suitable!!", cancelList1)
                            if cancelOption1 != None:
                                private_cancelDF = private_bedDF[private_bedDF["cancellation_policy"] == cancelOption1]
                                private_cancelDF.reset_index(drop= True, inplace= True)
                            minRate = private_cancelDF["price"].min()
                            maxRate = private_cancelDF["price"].max()
                            priceList = list(private_cancelDF["price"].unique())
                            priceList.sort()
                            if len(priceList) != 1:
                                minval, maxval = st.select_slider("The price Range",options = priceList, value =(minRate,maxRate), key = "ss1")
                                dfMin = private_cancelDF[private_cancelDF["price"] >= minval]
                                dfMin.reset_index(drop= True, inplace= True)
                                private_RateDF = dfMin[dfMin["price"] <= maxval]
                                private_RateDF.reset_index(drop= True, inplace= True)
                            else:
                                rate = st.slider("The price Range", max_value = maxRate, value = maxRate, key = "s1", disabled = True)
                                private_RateDF = private_cancelDF[private_cancelDF["price"] == rate]
                                private_RateDF.reset_index(drop= True, inplace= True)
                            private_SlideDF = addReviewSlide(private_RateDF)
                        except:
                            st.warning("Select the Bed type please!!")
                try:
                    finalLen1 = private_SlideDF.shape[0]
                    if finalLen1 != 0:
                        st.map(private_SlideDF, latitude = private_SlideDF.latitude, longitude = private_SlideDF.longitude, color = "#FF00FF")                 
                    privateHotelList = getHotelDetails(private_SlideDF)
                    listLen = private_SlideDF.shape[0]
                    col1, col2 = st.columns(2, gap = "medium")
                    for i in range(0,listLen, +2):
                        with col1:
                            displayDetails(privateHotelList, i)
                        with col2:
                            displayDetails(privateHotelList, i+1)
                except:
                    st.warning("**Mofify the search criteria for more options!!**")
                
            elif roomOption == "Entire home/apt":
                home_aptDF = (df1[df1["room_type"] == "Entire home/apt"])
                home_aptDF.reset_index(drop= True, inplace= True)
                with st.sidebar:
                    propertyList2 = list(home_aptDF["property_type"].unique())
                    propertyList2.sort()
                    propertyOption2 = st.multiselect("Select the propery Type", propertyList2, default = propertyList2[0])
                    if len(propertyOption2) > 0:
                        home_apt_propDF = (home_aptDF[home_aptDF["property_type"] == propertyOption2[0]])
                        home_apt_propDF.reset_index(drop= True, inplace= True)
                        for i in range(1,len(propertyOption2)):
                            tempDF = (home_aptDF[home_aptDF["property_type"] == propertyOption2[i]])
                            home_apt_propDF= pd.concat([home_apt_propDF, tempDF], axis=0, ignore_index=True)
                            home_apt_propDF.reset_index(drop= True, inplace= True)
                        try:
                            bedList2 = list(home_apt_propDF["bed_type"].unique())
                            bedList2.sort()
                            bedOption2 = st.multiselect("Select the Bed Type!!", bedList2, default = bedList2[0] )
                            home_bedDF = (home_apt_propDF[home_apt_propDF["bed_type"] == bedOption2[0]])
                            home_bedDF.reset_index(drop= True, inplace= True)
                            for i in range(1,len(bedOption2)):
                                tempDF = (home_apt_propDF[home_apt_propDF["bed_type"] == bedOption2[i]])
                                home_bedDF= pd.concat([home_bedDF, tempDF], axis=0, ignore_index=True)
                                home_bedDF.reset_index(drop= True, inplace= True)
                            cancelList2 = list(home_bedDF["cancellation_policy"].unique())
                            cancelList2.sort()
                            cancelOption2 = st.radio("Available Cancellation Policy. Select the suitable!!", cancelList2)
                            if cancelOption2 != None:
                                home_cancelDF = (home_bedDF[home_bedDF["cancellation_policy"] == cancelOption2])
                                home_cancelDF.reset_index(drop= True, inplace= True)
                            minRate = home_cancelDF["price"].min()
                            maxRate = home_cancelDF["price"].max()
                            priceList = list(home_cancelDF["price"].unique())
                            priceList.sort()
                            if len(priceList) != 1:
                                minval, maxval = st.select_slider("The price Range",options = priceList, value =(minRate,maxRate), key = "ss2")
                                dfMin = home_cancelDF[home_cancelDF["price"] >= minval]
                                dfMin.reset_index(drop= True, inplace= True)
                                home_RateDF = dfMin[dfMin["price"] <= maxval]
                                home_RateDF.reset_index(drop= True, inplace= True)
                            else:
                                rate = st.slider("The price Range", max_value = maxRate, value = maxRate, key = "s2", disabled = True)
                                home_RateDF = home_cancelDF[home_cancelDF["price"] == rate]
                                home_RateDF.reset_index(drop= True, inplace= True)
                            home_SlideDF = addReviewSlide(home_RateDF)
                        except:
                            st.warning("Select the Bed type please!!")
                try:
                    finalLen2 = home_SlideDF.shape[0]
                    if finalLen2 != 0:
                        st.map(home_SlideDF, latitude = home_SlideDF.latitude, longitude = home_SlideDF.longitude, color = "#FF00FF")

                    homeHotelList = getHotelDetails(home_SlideDF)
                    listLen = home_SlideDF.shape[0]
                    col1, col2 = st.columns(2, gap = "medium")
                    for i in range(0,listLen, +2):
                        with col1:
                            displayDetails(homeHotelList, i)
                        with col2:
                            displayDetails(homeHotelList, i+1)
                except:
                    st.warning("**Mofify the search criteria for more options!!**")
                        
            elif roomOption == "Shared Room":
                sharedDF = (df1[df1["room_type"] == "Shared room"])
                sharedDF.reset_index(drop= True, inplace= True)
                with st.sidebar:
                    propertyList3 = list(sharedDF["property_type"].unique())
                    propertyList3.sort()
                    propertyOption3 = st.multiselect("Select the propery Type", propertyList3, default = propertyList3[0])
                    if len(propertyOption3) > 0:
                        shared_propDF = (sharedDF[sharedDF["property_type"] == propertyOption3[0]])
                        shared_propDF.reset_index(drop= True, inplace= True)
                        for i in range(1,len(propertyOption3)):
                            tempDF = (sharedDF[sharedDF["property_type"] == propertyOption3[i]])
                            shared_propDF= pd.concat([shared_propDF, tempDF], axis=0, ignore_index=True)
                            shared_propDF.reset_index(drop= True, inplace= True)
                        try:
                            bedList3 = list(shared_propDF["bed_type"].unique())
                            bedList3.sort()
                            bedOption3 = st.multiselect("Select the Bed Type!!", bedList3, default = bedList3[0])
                            shared_bedDF = (shared_propDF[shared_propDF["bed_type"] == bedOption3[0]])
                            shared_bedDF.reset_index(drop= True, inplace= True)
                            for i in range(1,len(bedOption3)):
                                tempDF = (shared_propDF[shared_propDF["bed_type"] == bedOption3[i]])
                                shared_bedDF= pd.concat([shared_bedDF, tempDF], axis=0, ignore_index=True)
                                shared_bedDF.reset_index(drop= True, inplace= True)
                            cancelList3 = list(shared_bedDF["cancellation_policy"].unique())
                            cancelList3.sort()
                            cancelOption3 = st.radio("Available Cancellation Policy. Select the suitable!!", cancelList3)
                            if cancelOption3 != None:
                                shared_cancelDF = (shared_bedDF[shared_bedDF["cancellation_policy"] == cancelOption3])
                                shared_cancelDF.reset_index(drop= True, inplace= True)
                            minRate = shared_cancelDF["price"].min()
                            maxRate = shared_cancelDF["price"].max()
                            priceList = list(shared_cancelDF["price"].unique())
                            priceList.sort()
                            if len(priceList) != 1:
                                minval, maxval = st.select_slider("The price Range",options = priceList, value =(minRate,maxRate), key = "ss3")
                                dfMin = shared_cancelDF[shared_cancelDF["price"] >= minval]
                                dfMin.reset_index(drop= True, inplace= True)
                                shared_RateDF = dfMin[dfMin["price"] <= maxval]
                                shared_RateDF.reset_index(drop= True, inplace= True)
                            else:
                                rate = st.slider("The price Range", max_value = maxRate, value = maxRate, key = "s3", disabled = True)
                                shared_RateDF = shared_cancelDF[shared_cancelDF["price"] == rate]
                                shared_RateDF.reset_index(drop= True, inplace= True)
                            shared_SlideDF = addReviewSlide(shared_RateDF) 
                        except:
                            st.warning("Select the Bed type please!!")
                try:
                    finalLen3 = shared_SlideDF.shape[0]
                    if finalLen3 != 0:
                        st.map(shared_SlideDF, latitude = shared_SlideDF.latitude, longitude = shared_SlideDF.longitude, color = "#FF00FF")
                    sharedHotelList = getHotelDetails(shared_SlideDF)
                    listLen = shared_SlideDF.shape[0]
                    col1, col2 = st.columns(2, gap = "medium")
                    for i in range(0,listLen, +2):
                        with col1:
                            displayDetails(sharedHotelList, i)
                        with col2:
                            displayDetails(sharedHotelList, i+1)
                except:
                    st.warning("**Mofify the search criteria for more options!!**")
    with tab2:
        tab3, tab4, tab5 = st.tabs([":blue[Country Wise]", ":blue[Property Type Wise]", ":blue[Host Response Rate Wise]"])
        with tab4:
            df1 = df.groupby(["country", "property_type", "room_type"])[["host_listings_count"]].sum()
            df1.reset_index(inplace = True)
            fig1= px.sunburst(df1, path = ["country", "property_type", "room_type"], values= "host_listings_count",
                              title= "Countyr based property distribution",width=1000, height= 1000,
                              color_continuous_scale = px.colors.cyclical.HSV, color = "host_listings_count")
            st.plotly_chart(fig1)
        with tab3:
            
   

    




















            
elif menuOption == "Tasks":
    st.dataframe(df)
    list1 = list(df["room_type"].unique())
    st.write(list1)
