import pandas as pd

def perAttemptCalc(Attempt, Calculation):
    attempt = Attempt
    calculation = Calculation
    return (calculation / attempt)
    
def getNFLdata(minAttempts):
    nflData = pd.read_csv('tables/data/NFL Play by Play 2016 (v3).csv', delimiter=',')

    # Subset offensive data to get pass data that is relevant (i.e. passes that are actually complete... duh)
    pass_data = nflData[nflData['PlayType'] == "Pass"]
    pass_data = pass_data[pass_data['PassOutcome'] == "Complete"]
    pass_data = pass_data[["GameID","FirstDown","posteam", "DefensiveTeam", "Yards.Gained", "Touchdown", "Passer", "Passer_ID", "PassOutcome", "PassLength", "AirYards", "YardsAfterCatch","PassLocation", "InterceptionThrown", "Receiver", "Receiver_ID"]]

    # Group the data frame by passer/receiver combination and extract a number of stats from each group. Finally, rename a column for clarity
    passer_receiver_combination_grouped = pass_data.groupby(['Passer', 'Receiver']).agg({'Passer':"count", 'Yards.Gained':sum, 'Touchdown': sum,'FirstDown': sum}).rename(columns={'Passer': 'Pass.Attempts'}).reset_index()

    # Combine Passer + Receiver into one column
    passer_receiver_combination_grouped['Combination'] = ((passer_receiver_combination_grouped['Passer']) + " to " + (passer_receiver_combination_grouped['Receiver']))

    # Move column "Combination" to after "Receiver"
    passer_receiver_combination_grouped = passer_receiver_combination_grouped[['Passer','Receiver','Combination','Pass.Attempts', 'Yards.Gained','Touchdown','FirstDown']]

    # Add column to calculate values per pass, per touchdown and per first down
    passer_receiver_combination_grouped['Yards.Gained.Per.Pass'] = perAttemptCalc(passer_receiver_combination_grouped['Pass.Attempts'], passer_receiver_combination_grouped['Yards.Gained'])
    passer_receiver_combination_grouped['Touchdown.Per.Pass'] = perAttemptCalc(passer_receiver_combination_grouped['Pass.Attempts'], passer_receiver_combination_grouped['Touchdown'])
    passer_receiver_combination_grouped['FirstDown.Per.Pass'] = perAttemptCalc(passer_receiver_combination_grouped['Pass.Attempts'], passer_receiver_combination_grouped['FirstDown'])

    # Expected Value Calculation - Touchdown is 6 points.  First Down is 6/10 or 0.6 points.
    FirstDownMultiplier = 0.6
    YardMultiplier = 0.06
    passer_receiver_combination_grouped['Efficiency'] = (passer_receiver_combination_grouped['Touchdown.Per.Pass'] * 6) + (passer_receiver_combination_grouped['FirstDown.Per.Pass'] * FirstDownMultiplier) + (passer_receiver_combination_grouped['Yards.Gained.Per.Pass'] * YardMultiplier)

    # Order dataframe by expected value calculation'
    efficiency_calc = passer_receiver_combination_grouped.sort_values('Efficiency', ascending = False)

    # Create dataframe for min 5, 10, 25, 50, 100 receptions (Assumptions)
    min_two_receptions = efficiency_calc[efficiency_calc['Pass.Attempts'] >= minAttempts]

    # Return dataframe
    nfl_final_dataframe = min_two_receptions
    
    return nfl_final_dataframe