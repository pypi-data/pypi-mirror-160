# To install the module
```pip install statisticsmaniac```

# To import the module
```import statmaniac```

# To specify the format
```format = 1 for Tests```

```format = 2 for ODIs```

```format = 3 for T20Is```

# To find the stats of a player
```statmaniac.player_stats(player,format)```

Example:

```statmaniac.player_stats("Virat Kohli",3)```

Note : Use the player names as on cricinfo website , for example : don't write player name as "Rohit Sharma", it is "RG Sharma" on cricinfo

This will return a pandas dataframe which can be further used for data analysis

# To save the stats as a csv file
```statmaniac.save_stats_as_csv("Virat Kohli",3)```

# To get the player summary

```statmaniac.player_summary("Virat Kohli",3)```

This will return a list in this format ```[runs,notouts,batting average,hundreds]```