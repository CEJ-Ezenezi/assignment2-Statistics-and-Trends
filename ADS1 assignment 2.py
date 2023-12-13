# -*- coding: utf-8 -*-+
"""original_data?.,

Created on Sun Dec  3 19:41:24 2023

@author: CHIAMAKA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import stats

#Defining functions

def read_data(csv_filename):
    """reads a csv file into a dataframe
    and returns the original dataframe df1 and the
    transposed dataframe, df_T
    """
    
    #read original csv file into pandas dataframe
    df1 = pd.read_csv(csv_filename)

    #setting index
    df1 = df1.set_index(["Series Name","Country Name"])
    
    #cleaning the data, drop irrelevant columns
    df1 = df1.drop(["Series Code", "Country Code"], axis=1)
    #drop last two rows with Nan values
    df1 = df1.dropna()
    #get rid of '..' from the data
    df1 = df1.replace('..', np.nan)
    #assigning appropriate data type
    df1 = df1.astype("float")
    #rename columns
    df1.columns = ["1990", "2000", "2010", "2011", "2012", "2013", 
                          "2014", "2015", "2016", "2017", "2018", "2019", 
                          "2020", "2021"]

    #transposes the dataframe
    df_T = df1.transpose()
    df_T.rename(columns={"Agriculture, forestry, and fishing, value added (% of GDP)":
    "Agriculture(% of GDP)", 
    "Unemployment, total (% of total labor force) (national estimate)":
     "Unemployment(% of labor force"}, level=0, inplace=True)
    
    return (df1, df_T)


#defining a line plot function 
def lineplot(df, country_to_plot, y):
    """ Function to create a lineplot. 
    Arguments:
    A dataframe with columns "country" and index "x"
    A list containing values of a column to iterate over to plot.
    A label for the y axis "y"

    """
    plt.figure(figsize=(9,7))

    for country in country_to_plot:
        plt.plot(df[country], label=country)


    plt.xlabel("year")
    plt.ylabel(y)
    #removing white space left and right.
    
    plt.legend(loc='upper right', bbox_to_anchor=(0, 0))
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



def plot_bubble_chart(data, indicator1, indicator2, indicator3, size_variable, title="Bubble Chart"):
    """
    Plot a bubble chart for three economic indicators for different countries.

    Parameters:
    - data: DataFrame containing the economic indicators for different countries.
    - indicator1, indicator2, indicator3: Names of the economic indicators.
    - size_variable: Name of the variable to be used for bubble size.
    - title: Title of the plot.
    """

    plt.figure(figsize=(10, 8))

    # Scatter plot with bubble size determined by the third variable
    plt.scatter(data[indicator1], data[indicator2], s=data[size_variable], alpha=0.7, cmap='viridis', c=data[indicator3])

    # Add labels and title
    plt.xlabel(indicator1)
    plt.ylabel(indicator2)
    plt.title(title)

    # Add a colorbar to represent the third economic indicator
    cbar = plt.colorbar()
    cbar.set_label(indicator3)

    # Show the plot
    plt.show()



#calling the read_data function
csv_filename = "eco_activity2.csv"
original_data, transposed_data = read_data(csv_filename)
print("Original Data:")
print(original_data)

print("\nTransposed Data:")
print(transposed_data)



#calling the line_plot function on the GDP for each country
df_GDP = transposed_data["GDP (current LCU)"]
print(df_GDP)

country_to_plot = ["Algeria", "Australia", "Brazil", "Cameroon", 
                   "China", "Canada",	"Ghana", "France",	"Germany",	
                   "Egypt, Arab Rep.","India","Japan", "Jamaica","South Africa"
                   ,"New Zealand", "Nigeria", "Russian Federation", "Turkiye"
                   , "United States", "United Kingdom", "United Arab Emirates"
                   , "Zimbabwe"]

#calling the linplot function on the GDP for each country
lineplot(df_GDP, country_to_plot, y="GDP")

#calling the lineplot function on the total population of each country
df_pop = transposed_data["Population, total"]
lineplot(df_pop, country_to_plot, y="Population")

#for series in transposed_data.columns.levels[0]:
    #df_pop = transposed_data[series]
    #lineplot(df_pop, country_to_plot, y="series")



#plotting correlation heatmap for the economic indicators of each country
#for country in country_to_plot:
    #sliced_data = transposed_data.xs(country, level="Country Name", axis=1)
    #plot_correlation_heatmap(sliced_data, title=country)
    
for country in country_to_plot:
    sliced_data = transposed_data.xs(country, level="Country Name", axis=1)
    plot_bubble_chart(transposed_data, "GDP per capita (current LCU)", 
            "CO2 emissions (kg per PPP $ of GDP)", "Population, total",
            size_variable="Population, total", title=country)
    



#three summary statistics
transposed_data.describe()    
data_Tstat = transposed_data.agg([stats.skew, stats.kurtosis])
    
    
