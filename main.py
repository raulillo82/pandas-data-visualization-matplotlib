import pandas as pd
import matplotlib.pyplot as plt
'''
## Get the Data
    "Either use the provided .csv file or (optionally) get fresh (the freshest?) data from running an SQL query on StackExchange:,
    "Follow this link to run the query from [StackExchange](https://data.stackexchange.com/stackoverflow/query/675441/popular-programming-languages-per-over-time-eversql-com) to get your own .csv file",
    "<code>",
    "select dateadd(month, datediff(month, 0, q.CreationDate), 0) m, TagName, count(*)\n",
    "from PostTags pt\n",
    "join Posts q on q.Id=pt.PostId\n",
    "join Tags t on t.Id=pt.TagId\n",
    "where TagName in ('java','c','c++','python','c#','javascript','assembly','php','perl','ruby','visual basic','swift','r','object-c','scratch','go','swift','delphi')\n",
    "and q.CreationDate < dateadd(month, datediff(month, 0, getdate()), 0)\n",
    "group by dateadd(month, datediff(month, 0, q.CreationDate), 0), TagName\n",
    "order by dateadd(month, datediff(month, 0, q.CreationDate), 0)\n",
    "</code>"

'''

q1 = """
Read the .csv file and store it in a Pandas DataFrame called df. Have a look at the read_csv() documentation and try to provide these column names: ['DATE', 'TAG', 'POSTS']

Look at the first and last 5 rows of the DataFrame.
"""

q2 = """
How many rows and how many columns does it have?
"""
q3 = """
Count the number of entries in each column.
"""

print(q1)
df = pd.read_csv('QueryResults2.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
#print(df)
print(df.head())
print(df.tail())
print(q2)
print(df.shape)
print(q3)
print(df.count())

"""
In order to look at the number of entries and the number of posts by programming language, we need to make use of the .groupby() method. The key is combining .groupby() with the TAG column, which holds as our categories (the names of the programming languages).

If we .sum() the number of posts then we can see how many posts each programming language had since the creation of Stack Overflow.

"""
q4 = """
Calculate the total number of post per language. Which Programming language has
had the highest total number of posts of all time?
"""
print(q4)
print(df.groupby("TAG").sum()[['POSTS']])

q5 = """
How many months of data exist per language?
Which Language had the fewest months with an entry?
"""
print(q5)
print(df.groupby("TAG").count().sort_values('DATE'))

#print(df['DATE'][1])
#print(type(df.DATE[1]))
#Convert DATE to datetime objects
df.DATE = pd.to_datetime(df.DATE)
print("""
      Converting the dates into a better readable format
      """)
print(df.head())

print("""
      Pivot data around the value in the date,
      using the programming language as columns,
      and the number of posts for its value.
      Also change NaN values to 0's.
      """)
reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')
reshaped_df.fillna(0, inplace=True)
print(reshaped_df.head())
#print(reshaped_df.isna().values.any())
plt.figure(figsize=(16,10))
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)
plt.title("Popularity of programming languages in stackoverflow")

#plt.plot(reshaped_df.index, reshaped_df.java, label='java')
#plt.plot(reshaped_df.index, reshaped_df.python, label='python')

#Even better than the previous:
for column in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[column],
             linewidth=3, label=column)
plt.legend(fontsize=16)
plt.show(block=False)

#ROLL MEAN DF:
#Try a few values for window size: 3, 6, 9, 12
sizes = range(3, 13, 3)
#Try only with size = 6
#Comment next line if you want to see all combinations
sizes = [6]
roll_dfs = [[reshaped_df.rolling(window=size).mean(), size]
            for size in sizes]

# plot each of the possible roll_df's instead
for roll_df in roll_dfs:
    plt.figure(figsize=(16,10))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Number of Posts', fontsize=14)
    plt.ylim(0, 35000)
    plt.title(f"Popularity of programming languages in stackoverflow: rolling mean with size={roll_df[1]}")
    for column in roll_df[0].columns:
        plt.plot(roll_df[0].index, roll_df[0][column],
                 linewidth=3, label=roll_df[0][column].name)
    plt.legend(fontsize=16)
    if roll_df[1] == sizes[-1]:
        plt.show()
    else:
        plt.show(block=False)
