import matplotlib.pyplot as plt #Visualization
import pandas as pd             #Exploratory data Analysis
import plotly.express as px     #Visulaization

#To import and clean the data....For the first CSV file
df1 = pd.read_csv("data/brasil-real-estate-1.csv")
df1.head()

#To drop all rows with vales "Nan" from Dataframe df1
df1.dropna(inplace=True)
#From the data, we can see there is a column called lat-lon combine together with each values differentiated by a comma in betwen them,
#to seperate both lat and lon by placing them in different columns and also removing the Delimeter (,) that is in between them,
# and also making sure the datatype for this new coloumns is float instead of object
df1[["lat", "lon"]] = df1["lat-lon"].str.split("," , expand=True).astype(float)

#Using the "place_with_parent_names" column to create a "state" column for df1
df1["state"] = df1["place_with_parent_names"].str.split("|", expand=True)[2]

#Transform the "price_usd" column of df1 so that all values are floating-point numbers instead of strings
df1["price_usd"] = df1["price_usd"].str.replace("$","", regex=False).str.replace(",","").astype(float)

#Drop the "lat-lon" and "place_with_parent_names" columns from df1
df1.drop(columns=["place_with_parent_names", "lat-lon"], inplace=True)

#Import the CSV file brasil-real-estate-2.csv into the DataFrame df2
df2 = pd.read_csv("data/brasil-real-estate-2.csv")

#Use the "price_brl" column to create a new column named "price_usd". 
#(Keep in mind that, when this data was collected in 2015 and 2016, a US dollar cost 3.19 Brazilian reals.)
df2["price_usd"] = (df2["price_brl"] / 3.19).round(2)

#Drop the "price_brl" column from df2, as well as any rows that have NaN values.
df2.dropna(inplace=True)
df2.drop(columns = ["price_brl"], inplace=True)

#Concatenate df1 and df2 to create a new DataFrame named df
df = pd.concat([df1,df2])
print("df shape:", df.shape)

#Exploratory data Analysis
# create a scatter_mapbox showing the location of the properties in df
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    center={"lat": -10.3, "lon": -53.2},  # Map will be centered on Brazil
    width=600,
    height=600,
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

fig.update_layout(mapbox_style="open-street-map")

fig.show()

#Use the describe method to create a DataFrame summary_stats with the summary statistics for the "area_m2" and "price_usd" columns.
summary_stats = df[["area_m2", "price_usd"]].describe()
summary_stats

#Create a histogram of `"price_usd"`, with x-axis and y-axis label as `"Price [USD]"` and `"Frequency"` respectively. 
# And the plot title has  `"Distribution of Home Prices"`. Using Matplotlib (`plt`).
plt.hist(df["price_usd"])
plt.xlabel("Price [USD]")
plt.ylabel("Frequency")
plt.title("Distribution of Home Prices");

#Create a horizontal boxplot of "area_m2", with the x-axis label as  "Area [sq meters]" and the plot has the title "Distribution of Home Sizes".
plt.boxplot(df["area_m2"], vert=False)
plt.xlabel("Area [sq meters]")
plt.title("Distribution of Home Sizes");

#Use the groupby method to create a Series named mean_price_by_region that shows the mean home price in each region in Brazil, sorted from smallest to largest.
mean_price_by_region = df.groupby("region")["price_usd"].mean()
mean_price_by_region

# Use mean_price_by_region to create a bar chart, with x-axis and y-axis label as "Region" and "Mean Price [USD]" respectiovely, and title "Mean Home Price by Region", Using Pandas
mean_price_by_region.plot(
    kind="bar",
    xlabel="Region",
    ylabel="Mean Price [USD]",
    title="Mean Home Price by Region"
);
#Shifting my focus to the southern region of Brazil, I want to determine the relationship between home size and price.
#Create a DataFrame df_south that contains all the homes from df that are in the "South" region.
df_south = df[df["region"] == "South"]

#Use the value_counts method to create a Series homes_by_state that contains the number of properties in each state in df_south
homes_by_state = df_south["state"].value_counts()

#Create a scatter plot showing price vs. area for the state in df_south that has the largest number of properties, with x-axis and y-axis label as "Area [sq meters]" and "Price [USD]" respectively; Titled "<name of state>: Price vs. Area"
df_south_rgs = df_south[df_south["state"] == homes_by_state.idxmax()]

plt.scatter(x=df_south_rgs["area_m2"], y=df_south_rgs["price_usd"])
plt.xlabel("Area [sq meters]")
plt.ylabel("Price [USD]")
plt.title(f'{homes_by_state.idxmax()}: Price vs. Area');

#Create a dictionary south_states_corr, where the keys are the names of the three states in the "South" region of Brazil, 
#and their associated values are the correlation coefficient between "area_m2" and "price_usd" in that state.
south_states_corr = {}

for state in df_south["state"].unique():
    df_state = df_south[df_south["state"] == state]
    p_correlation = df_state["area_m2"].corr(df_state["price_usd"])
    south_states_corr[state] = p_correlation
print(south_states_corr)    