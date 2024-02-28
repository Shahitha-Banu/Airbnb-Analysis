import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit.components.v1 as components

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

str1 = """**:blue[Airbnb is an American company operating an online marketplace for short- and long-term homestays and experiences.
The company acts as a broker and charges a commission from each booking.
The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia.
Airbnb is a shortened version of its original name, AirBedandBreakfast.com. Airbnb is the most well-known company for short-term housing rentals.]**"""
with st.sidebar:
    img1 = Image.open("airbnb.jpg")
    st.image(img1,width = 250)
    #st.write(str1)

st.header(":rainbow[Airbnb Analysis]")
menuOption = option_menu(None, ["Property Analysis","Property Search", 'About'],
                         icons=['buildings-fill', "house-gear-fill", 'list-stars'],
                         menu_icon="cast", default_index=0, orientation="horizontal",
                         styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "2px", "--hover-color": "#00AABB"},
                               "icon": {"font-size": "15px"},
                               "container" : {"max-width": "8000px"},
                               "nav-link-selected": {"background-color": "#00BB00"}})

if menuOption == "Property Search":
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
            
elif menuOption == "Property Analysis":
    tab3, tab4, tab5 = st.tabs([":blue[Country Wise]", ":blue[Property Wise]", ":blue[Host Wise]"])
    countryList = list(df["country"].unique())
    countryList.sort()
    with tab4:
        df4 = df.groupby(["property_type"])[["room_type"]].count()
        df4.rename(columns = {'room_type':'Count'}, inplace = True)
        df4.reset_index(inplace = True)
        df4.sort_values("Count", ascending = False, inplace = True, ignore_index = True)

        df5 = df.groupby(["bed_type"])[["room_type"]].count()
        df5.rename(columns = {'room_type':'Count'}, inplace = True)
        df5.reset_index(inplace = True)
        df5.sort_values("bed_type", ascending = False, inplace = True, ignore_index = True)

        df6 = df.groupby(["room_type", "property_type"])[["number_of_reviews"]].sum()
        df6.rename(columns = {'number_of_reviews':'Review_Count'}, inplace = True)
        df6.reset_index(inplace = True)    

        df7 = df.groupby(["cancellation_policy"])[["property_type"]].count()
        df7.rename(columns = {'number_of_reviews':'Review_Count'}, inplace = True)
        df7.reset_index(inplace = True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig6 = px.bar(df4[:12], y ="Count", x = "property_type",title= "Major Available Property Types",
                           width=500, height= 400, color_discrete_sequence = px.colors.sequential.RdBu, color = "property_type")
            st.plotly_chart(fig6)

            fig7 = px.pie(df6, names="property_type", values= "Review_Count",title= "Property type based on User Reviews",
                           width=550, height= 900, color_discrete_sequence = px.colors.cyclical.Edge, hole = 0.3, color = "Review_Count")
            st.plotly_chart(fig7)
            
        with col2:           
            fig5 = px.bar(df5, x ="Count", y = "bed_type",title= "Available bed types",
                           width=500, height= 400, color_discrete_sequence = px.colors.sequential.Agsunset, color = "bed_type")
            st.plotly_chart(fig5)

            fig8 = px.pie(df7, names="cancellation_policy", values= "property_type",title= "Property available based on the Cancellation Policy",
                           width=400, height= 700, color_discrete_sequence = px.colors.cyclical.HSV, hole = 0.3, color = "cancellation_policy")
            st.plotly_chart(fig8)            
      
    with tab3:
        roomList = []
        for country in countryList:
            df1= df[df["country"] == country]
            df1.reset_index(inplace = True)
            countdf = df1.groupby(["country", "room_type"])[["property_type"]].count()
            countdf.reset_index(drop = True, inplace = True)
            roomList.append(countdf["property_type"].values.tolist())
        for i in range(len(countryList)):
            roomList[i].insert(0,countryList[i])
        stackedBarDF = pd.DataFrame(roomList, columns=["Country", "Entire home/apt", "Private room", "Shared room" ])
        st.subheader(":black[Type of rooms available in each country]")
        st.bar_chart(stackedBarDF, x = "Country", y = ["Entire home/apt", "Private room", "Shared room"],
                         color=["#FF00FF", "#0000FF", "#FFFF00"], height = 600, width = 400)
        st.subheader(":black[Average Cost of Per Day Stay]")
        fig3 = make_subplots(rows=1, cols=9, subplot_titles  = countryList)
        for i in range(len(countryList)):
            df2= df[df["country"] == countryList[i]]
            df2.reset_index(inplace = True)
            pricedf = df2.groupby(["country", "property_type"])[["price", "security_deposit", "cleaning_fee"]].mean()
            pricedf.reset_index(inplace = True)
            pricedf["total_cost"] = pricedf[["price", "security_deposit", "cleaning_fee"]].sum(axis = 1)
            pricedf.reset_index(inplace = True)
            fig3.append_trace(go.Bar(x = [pricedf["country"], pricedf['property_type']], y = pricedf['total_cost']), row = 1, col = i+1)

        fig3.update_layout(legend_title_text ='Counrties', showlegend = True, height=800, width=1100)
        st.plotly_chart(fig3)

        df1 = df.groupby(["country", "property_type", "room_type"])[["host_listings_count"]].sum()
        df1.reset_index(inplace = True)
        fig1= px.sunburst(df1, path = ["country", "room_type", "property_type"], values= "host_listings_count",
                              title= "Countyr based property distribution",width=1000, height= 900,
                              color_continuous_scale = px.colors.cyclical.HSV, color = "host_listings_count")
        st.plotly_chart(fig1)        

    with tab5:
        df3 = df.groupby(["country", "host_response_time"])[["room_type"]].count()
        df3.reset_index(inplace = True)
        fig4 = px.line(df3, x="country", y="room_type",title= "Response Rate of the Host",
                           width=800, height= 500, color_discrete_sequence = px.colors.diverging.Spectral, color = "host_response_time")
        st.plotly_chart(fig4)

        df8 = df.groupby(["country"])[["availability_30", "availability_60","availability_90", "availability_365"]].sum()
        df8.reset_index(inplace = True)
        
        fig9 = px.bar(df8, x='country', y=['availability_30', 'availability_60', 'availability_90', "availability_365"], 
                    title='Availability of the property for Next 30, 60, 90 and 365 days',barmode = 'group',
                    color_discrete_sequence = px.colors.sequential.Rainbow_r, width=1000)
        st.plotly_chart(fig9)

elif menuOption == "About":
    img2 = Image.open("airbnb3.jpg")
    st.image(img2)
    st.write(str1)
    
    components.html(
    """
    <font color="#9900FF">
    <h3 style="background-color:powderblue;"> Analysis Report</h3></font>
    <font color = "#FF0000">
    <ul type = "square">
    <li> The country with maximum number of property is <b>United States</b> whereas with least is <b>China.</b></li>
    <li> <b> Appartments </b> are most available option for stay.</li>
    <li> The average cost of the stay is high in <b> Australia</b> compared to other available countries.</li>
    <li> The most followed cancellation policy by the host is <b> Strict 14 with grace preriod.</b></li>
    <li> Based on the user reviews, <b> Appartments </b> are preffered by most.</li>
    <li> The host response is very high in <b> United States.</b></li>
    <li> Mostly the property is available for the <b>whole year</b> of stay</li>
    </ul></font>
    """,
    height=200)
