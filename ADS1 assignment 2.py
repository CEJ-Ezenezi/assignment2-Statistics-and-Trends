"""

Created on Sun Dec  3 19:41:24 2023

@author: CHIAMAKA
"""
#importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kurtosis
from scipy.stats import skew



#Defining relevant functions
def read_data(csv_filename):
    """reads a csv file into a dataframe
    and returns the original dataframe df1 and the
    cleaned transposed dataframe, df_T
    """
    
    #read original csv file into pandas dataframe
    df1 = pd.read_csv(csv_filename)

    #setting multi-index
    df1 = df1.set_index(["Series Name","Country Name"])
    
    #cleaning the data, drop irrelevant columns
    df1 = df1.drop(["Series Code", "Country Code"], axis=1)
    #drop last rows with Nan values
    df1 = df1.dropna()
    #get rid of '..' from the data
    df1 = df1.replace('..', np.nan)
    #assigning appropriate data type tothe dataframe
    df1 = df1.astype("float")
    #rename columns
    df1.columns = ["2010", "2011", "2012", "2013", "2014", "2015", 
                   "2016", "2017", "2018", "2019", "2020", "2021"]

    #transposes the dataframe
    df_T = df1.transpose()
    #rename long column names
    df_T.rename(columns={"Agriculture, forestry, and fishing, value added (% of GDP)":
    "Agriculture(% of GDP)", 
    "Unemployment, total (% of total labor force) (national estimate)":
     "Unemployment(% of labor force"}, level=0, inplace=True)
    
    return (df1, df_T)


#defining a line plot function 
def lineplot(df, country_to_plot, y):
    """ Function to create a lineplot. 
    Arguments:
    A dataframe with multi-index columns "country"  at level 1 and 
    columns "x" at level 0
    A list containing values of a column to iterate over to plot.
    A label for the y axis "y"

    """
    plt.figure(figsize=(9,7))

    for country in country_to_plot:
        plt.plot(df[country], label=country)


    plt.xlabel("year")
    plt.ylabel(y)
    
    
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1))
    plt.show()
    
    return plt.figure()


def plot_correlation_heatmap(country_data, title):
    """
    Plots a heatmap of the correlation among economic indicators for a given
    country.

    Parameters:
    - country_data: Pandas DataFrame containing economic indicators. 
      Rows represent different years, and columns represent different
      indicators.
    - title: Title of the heatmap.
    """
    # Calculate the correlation matrix
    correlation_matrix = country_data.corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(5, 3))

    # Create a heatmap using seaborn
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f",
                linewidths=.5, cbar_kws={'label': 'Correlation Coefficient'})

    # Set title and labels
    plt.title(title)
    plt.xlabel('Economic Indicators')
    plt.ylabel('Economic Indicators')
    # Display the plot
    plt.show()



def plot_bubble_chart(data, x_indicator, y_indicator, size_indicator, title):
    plt.figure(figsize=(10, 8))
    
    for country in data.columns.levels[1]:
        x_values = data[x_indicator][country].mean()
        y_values = data[y_indicator][country].mean()
        size_values = data[size_indicator][country].mean()

        plt.scatter(x_values, y_values, s = np.log(size_values) * 10 
            #adjusted the size_values so that the bubbles are visible
            ,alpha=0.7, edgecolors="k", cmap="viridis",label=country)

    plt.title(f'Bubble Chart: {x_indicator} vs {y_indicator} by {size_indicator}')
    plt.xlabel(x_indicator)
    plt.ylabel(y_indicator)

    plt.legend(markerscale=0.5)  
    plt.grid(True)
    plt.show()



#calling the read_data function
csv_filename = "world_eco_activity.csv"
original_data, transposed_data = read_data(csv_filename)
print("Original Data:")
print(original_data)

print("\nTransposed Data:")
print(transposed_data)

#three summary statistics to explore the dataframe
print(transposed_data.describe())
print(transposed_data["Agriculture(% of GDP)"].describe().transpose())
data_Tstat = [skew(transposed_data), kurtosis(transposed_data)]
print(data_Tstat)

#checking the skewness and kurtosis of the distribution
GDP_stat = [skew(transposed_data["GDP per capita growth (annual %)"]),
              kurtosis(transposed_data["GDP per capita growth (annual %)"])]
print(GDP_stat)
country_to_plot = ["Brazil", "China", "Canada",	"Germany","India","South Africa"
                   ,"Nigeria", "New Zealand", "United States", "United Kingdom"
                   ,"South Africa", "Russian Federation"]


#calling the lineplot function on the GDP for each country
for series in transposed_data.columns.levels[0]:
    df_by_indicator = transposed_data[series]
    lineplot(df_by_indicator, country_to_plot, y=series)



#plotting correlation heatmap for the economic indicators of each country
for country in country_to_plot:
     sliced_data = transposed_data.xs(country, level="Country Name", axis=1)
     plot_correlation_heatmap(sliced_data, title=country)
    
#plotting the bubble chart for three economic indicator
    
plot_bubble_chart(transposed_data, "GNI per capita growth (annual %)"
                  ,"GDP per capita growth (annual %)", "Population, total",
                  "Bubble Chart")



    
