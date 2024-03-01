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
    imgStr = list1["images"][i]
    imgStr = imgStr.replace("?aki_policy=large", "")
    imgStr = imgStr.replace("?t=r:w1200-h720-sfit,e:fjpg-c85", "")
    st.image(imgStr, width = 300)
    st.write(":rainbow[**Name of the Property:**]", list1["name"][i])
    st.write(":blue[**Cost of the stay:**]", list1["price"][i])
    st.write(":blue[**Review score:**]", list1["review_scores"][i])
    st.write(":blue[**Property Address:**]")
    st.write(list1["street"][i])
    st.write(list1["suburb"][i])
    st.write(list1["government_area"][i])
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

#Adding the property details
def addPropertyList(propertyDF):
    try:
        propertyList = list(propertyDF["property_type"].unique())
        propertyList.sort()
        propertyOption = st.multiselect("Select the Propery Type!!", propertyList, default = propertyList[0])
        if len(propertyOption) > 0:
            propertyUpdatedDF = propertyDF[propertyDF["property_type"] == propertyOption[0]]
            propertyUpdatedDF.reset_index(drop= True, inplace= True)
            for i in range(1,len(propertyOption)):
                tempDF = propertyDF[propertyDF["property_type"] == propertyOption[i]]
                propertyUpdatedDF= pd.concat([propertyUpdatedDF, tempDF], axis=0, ignore_index=True)
                propertyUpdatedDF.reset_index(drop= True, inplace= True)
        return propertyUpdatedDF
    except:
        st.warning("Select the property!")

#Adding the bed type details
def addBedList(bedDF):
    try:
        bedList = list(bedDF["bed_type"].unique())
        bedList.sort()
        bedOption = st.multiselect("Select the Bed Type!!", bedList, default = bedList[0])
        bedUpdateDF = bedDF[bedDF["bed_type"] == bedOption[0]]
        bedUpdateDF.reset_index(drop= True, inplace= True)
        for i in range(1,len(bedOption)):
            tempDF = bedDF[bedDF["bed_type"] == bedOption[i]]
            bedUpdateDF= pd.concat([bedUpdateDF, tempDF], axis=0, ignore_index=True)
            bedUpdateDF.reset_index(drop= True, inplace= True)
        return bedUpdateDF
    except:
        st.warning("The bed option is needed!")

#Adding the Cancellation policy details
def addCancelPolicyList(cancelDF):
    cancelList = list(cancelDF["cancellation_policy"].unique())
    cancelList.sort()
    cancelOption = st.radio("Available Cancellation Policy. Select the suitable!!", cancelList)
    if cancelOption != None:
        cancelUpdateDF = cancelDF[cancelDF["cancellation_policy"] == cancelOption]
        cancelUpdateDF.reset_index(drop= True, inplace= True)
    return cancelUpdateDF

#Adding price slider
def addPriceSlider(priceDF):
    try:
        minRate = priceDF["price"].min()
        maxRate = priceDF["price"].max()
        priceList = list(priceDF["price"].unique())
        priceList.sort()
        if len(priceList) != 1:
            minval, maxval = st.select_slider("The price Range",options = priceList, value =(minRate,maxRate))
            dfMin = priceDF[priceDF["price"] >= minval]
            dfMin.reset_index(drop= True, inplace= True)
            priceUpdateDF = dfMin[dfMin["price"] <= maxval]
            priceUpdateDF.reset_index(drop= True, inplace= True)
        else:
            rate = st.slider("The price Range", max_value = maxRate, value = maxRate, disabled = True)
            priceUpdateDF = priceDF[priceDF["price"] == rate]
            priceUpdateDF.reset_index(drop= True, inplace= True)
        return priceUpdateDF
    except:
        st.warning("Modify your search!")

#Adding the review slider
def addReviewSlide(slideDF):
    try:
        minSlide = slideDF["review_scores"].min()
        maxSlide = slideDF["review_scores"].max()
        slideList = list(slideDF["review_scores"].unique())
        slideList.sort()
        if minSlide == 0 and maxSlide == 0:
            reviewDF = slideDF.copy()
            st.write("The review score is 0 for all the selection!")
        else:
            if len(slideList) != 1:
                minval, maxval = st.select_slider("The review score Range",options = slideList, value =(minSlide,maxSlide))
                dfMin = slideDF[slideDF["review_scores"] >= minval]
                dfMin.reset_index(drop= True, inplace= True)
                reviewDF = dfMin[dfMin["review_scores"] <= maxval]
                reviewDF.reset_index(drop= True, inplace= True)
            else:
                slide = st.slider("The review score Range", max_value = maxSlide, value = maxSlide, disabled = True)
                reviewDF = slideDF[slideDF["review_scores"] == slide]
                reviewDF.reset_index(drop= True, inplace= True)
        return reviewDF
    except:
        st.warning("Review score is Zero for all the selection!")

#plotting the hotel details based on the selection
def displaySelectedStayDetails(stayDF):
    finalLen = stayDF.shape[0]
    if finalLen != 0:
        st.map(stayDF, latitude = stayDF.latitude, longitude = stayDF.longitude, color = "#FF00FF")
                    
    stayHotelList = getHotelDetails(stayDF)
    #listLen = stayDF.shape[0]
    col1, col2 = st.columns(2, gap = "medium")
    for i in range(0,finalLen, +2):
        with col1:
            displayDetails(stayHotelList, i)
        with col2:
            displayDetails(stayHotelList, i+1)

#Streamlit Designing Part
st.set_page_config(page_title= "Airbnb Analysis",
                   layout= "wide",
                   initial_sidebar_state= "expanded")

str1 = """**:orange[Airbnb is an American company operating an online marketplace for short- and long-term homestays and experiences.
The company acts as a broker and charges a commission from each booking.
The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia.
Airbnb is a shortened version of its original name, AirBedandBreakfast.com. Airbnb is the most well-known company for short-term housing rentals.]**"""
with st.sidebar:
    img1 = Image.open("airbnb.jpg")
    st.image(img1,width = 250)
    #st.write(str1)

st.header(":rainbow[Airbnb Analysis]")
menuOption = option_menu(None, ["Property Search","Property Analysis", 'Insights'],
                         icons=['house-gear-fill', "buildings-fill", 'list-stars'],
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
                try:
                    private_propDF = addPropertyList(privateDF)
                    private_bedDF = addBedList(private_propDF)
                    private_cancelDF = addCancelPolicyList(private_bedDF)
                    private_RateDF = addPriceSlider(private_cancelDF)
                    private_SlideDF = addReviewSlide(private_RateDF)
                except:
                    st.warning("Select the search creteria from sidebar")
            try:
                displaySelectedStayDetails(private_SlideDF)
            except:
                st.warning("Modify your search for more ooptions!")
                
        elif roomOption == "Entire home/apt":
            homeDF = (df1[df1["room_type"] == "Entire home/apt"])
            homeDF.reset_index(drop= True, inplace= True)
            with st.sidebar:
                try:
                    home_propDF = addPropertyList(homeDF)
                    home_bedDF = addBedList(home_propDF)
                    home_cancelDF = addCancelPolicyList(home_bedDF)
                    home_RateDF = addPriceSlider(home_cancelDF)
                    home_SlideDF = addReviewSlide(home_RateDF)
                except:
                    st.warning("Select the search creteria from sidebar!")
            try:
                displaySelectedStayDetails(home_SlideDF)
            except:
                st.warning("Modify your search for more ooptions!")

        elif roomOption == "Shared Room":
            sharedDF = (df1[df1["room_type"] == "Shared room"])
            sharedDF.reset_index(drop= True, inplace= True)
            with st.sidebar:
                try:
                    shared_propDF = addPropertyList(sharedDF)
                    shared_bedDF = addBedList(shared_propDF)
                    shared_cancelDF = addCancelPolicyList(shared_bedDF)
                    shared_RateDF = addPriceSlider(shared_cancelDF)
                    shared_SlideDF = addReviewSlide(shared_RateDF)
                except:
                    st.warning("Select the search creteria from sidebar!")
            try:
                displaySelectedStayDetails(shared_SlideDF)
            except:
                st.warning("Modify your search for more ooptions!")

            
elif menuOption == "Property Analysis":
    tab3, tab4, tab5 = st.tabs([":blue[Country Wise]", ":blue[Property Wise]", ":blue[Host Wise]"])
    countryList = list(df["country"].unique())
    countryList.sort()
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

        fig3.update_layout(legend_title_text ='Counrties', showlegend = True, height=900, width=1100)
        st.plotly_chart(fig3)
        
        st.subheader(":black[Host Neighbourhood and sub-urban Distribution]")
        df1 = df.groupby(["country", "host_neighbourhood", "suburb"])[["host_listings_count"]].sum()
        df1.reset_index(inplace = True)
        fig1= px.sunburst(df1, path = ["country", "host_neighbourhood", "suburb"], values= "host_listings_count",
                        width=1000, height= 900, color_continuous_scale = px.colors.cyclical.HSV, color = "host_listings_count")
        st.plotly_chart(fig1)
        
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

elif menuOption == "Insights":
    #st.dataframe(df)
    img2 = Image.open("airbnb3.jpg")
    st.image(img2)
    st.write(str1)
    
    components.html(
    """
    <font color = "#490400">
    <h3 style="background-color:powderblue;"> Analysis Report</h3></font>
    <font color = "#4b3f52">
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
