**Project Description:**

In this university project, I had the opportunity to explore all the phases that constitute a data science project, starting from various CSV files.
During the project, a data wrangling phase was conducted using basic Python to create the desired tables, while the libraries pandas, scikit-learn, and scipy were used for 
the data cleaning phase to derive and impute the missing values. Finally, the created tables were loaded into a database using a Python script.
![image](https://github.com/lordlordone/LDS_project/assets/125205569/a5b3db9a-7d07-4731-a183-1f9cc341d47f)

Through SSIS (SQL Server Integration Services), the following ETL (Extract, Transform, Load) tasks were performed:

  - For every country, the players were ordered by the number of matches won.
  - For each year, the players who participated in the most age mismatches (matches where the difference in years between the winner and loser is more than 6) were listed.
  - The total number of spectators that each player performed in front of was calculated.

Through SSAS (SQL Server Analysis Services), a data cube creation task was performed, and the following analysis tasks were carried out using MDX:

  - The percentage increase in loser rank points compared to the previous year was shown for each loser.
  - For each tournament, the percentage of total winner rank points was shown in relation to the total winner rank points of the corresponding year of the tournament.
  - The winners with a total winner rank points greater than the average winner rank points in each continent, grouped by continent and year, were shown.

Finally, using Power BI, the database created from the CSV files and the Python script were leveraged to visualize the geographic distribution of winner rank points 
and loser rank points, as well as the gender distribution in tennis matches in each continent/country for every year.

For more technical details, there are a powerpoint presentation and a report

**Technology used:**

- Python (pandas, scikit-learn, scipy)
- SSIS
- SSAS
- MDX
- PowerBI


**Project collaborators:**

Giuseppe Milazzo
