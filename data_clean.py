import pandas as pd
import numpy as np



# The number of the consecutive terms the incumbent party has been in office.

# Personal income.

# Electoral votes of the incumbent party in the previous election.

# Votes of the incumbent party in the last senate election.

# Votes of the incumbent party in the last house of representatives election.

# The president’s approval rate.

# Unemployment rate.

# The number of times that the 3-month GDP is above 3.2 within the last 4 years.


STATES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

def voteShare(df, year, state):
    candidate_total_dem = df["candidatevotes"].where((df["party"] == "democrat") & (df["year"] == year) & (df["state"] == state)).sum()
    total_dem = df["totalvotes"].where((df.year == year) & (df.state == state) & (df.party == "democrat")).sum()
    candidate_total_rep = df["candidatevotes"].where((df["party"] == "republican") & (df["year"] == year) & (df["state"] == state)).sum()
    total_rep = df["totalvotes"].where((df.year == year) & (df.state == state) & (df.party == "republican")).sum()
    
    return (candidate_total_dem/total_dem), (candidate_total_rep/total_rep)

def ApprovalClean():
    df = pd.read_csv("data/approval.csv")
    appdf = pd.DataFrame(columns=["year", "month", "approval"])
    
    index = 0
    for year in range(1980, 2020, 4): 
        apr_approve = df[(df["year"] == year) & (df["month"] == 4)].approve.mean()
        appdf.loc[index] = [year, 4, apr_approve]
        index += 1
        jun_approve = df[(df["year"] == year) & (df["month"] == 6)].approve.mean()
        appdf.loc[index] = [year, 6, jun_approve]
        index += 1

    appdf ["year"] = appdf["year"].astype("int64")
    return appdf

def incum_h(row):
    incum = {
        1976: "republican",
        1980: "democrat", 
        1984: "republican", 
        1988: "republican", 
        1992: "republican", 
        1996: "democrat", 
        2000: "democrat", 
        2004: "republican", 
        2008: "republican", 
        2012: "democrat", 
        2016: "democrat"
    }
    return incum[row["year"]]

def PresClean():
    df = pd.read_csv("data/1976-2016-president.csv")
    df = df.drop(
        [
            "state_po",
            "state_fips",
            "state_cen",
            "state_ic",
            "office",
            "writein",
            "version",
            "notes",
        ],
        axis=1,
    )
    df = df.drop(df[(df.party != "democrat") & (df.party != "republican")].index)

    df["voteshare"] = df["candidatevotes"] / df["totalvotes"]

    df = df.reset_index(drop=True)

    win = pd.DataFrame(columns=["year", "state", "winner"])
    index = 0
    for i in range(0, df.shape[0] - 1):
        if df.iloc[i]["state"] == df.iloc[i + 1]["state"]:
            if df.iloc[i]["voteshare"] > df.iloc[i + 1]["voteshare"]:
                win.loc[index] = [df.iloc[i]["year"], df.iloc[i]["state"], df.iloc[i]["party"]]
                index += 1

    df = df.reset_index(drop=True)

    df["incumbent"] = df.apply(lambda row: incum_h(row), axis=1)

    df["incumbent_win"] = df["incumbent"] == df["party"]

    return win, df


def SenateClean():
    df = pd.read_csv("data/1976-2018-senate.csv")
    df = df.drop(
        [
            "state_po",
            "state_fips",
            "state_cen",
            "state_ic",
            "office",
            "district",
            "stage",
            "special",
            "writein",
            "mode",
            "unofficial",
            "version",
        ],
        axis=1,
    )

    df = df.drop(df[(df.party != "democrat") & (df.party != "republican")].index)

    df["voteshare"] = df["candidatevotes"] / df["totalvotes"]
    df = df.reset_index(drop=True)

    s_df = pd.DataFrame(columns=["year", "state", "dem_voteshare", "rep_voteshare"])

    index = 0
    for year in range(1976, 2020, 2):
        for state in STATES:
            if state in df[df["year"] == year].state.values:
                share_dem, share_rep = voteShare(df, year, state)
                s_df.loc[index] = [year, state, share_dem, share_rep]
                index += 1
    
    return s_df


def HouseClean():
    df = pd.read_csv("data/1976-2018-house.csv")
    df = df.drop(
        [
            "state_po",
            "state_fips",
            "state_cen",
            "state_ic",
            "office",
            "district",
            "stage",
            "runoff",
            "special",
            "writein",
            "mode",
            "unofficial",
            "version",
        ],
        axis=1,
    )
    df = df.drop(df[(df.party != "democrat") & (df.party != "republican")].index)

    h_df = pd.DataFrame(columns=["year", "state", "dem_voteshare", "rep_voteshare"])
    index = 0
    for year in range(1976, 2020, 2):
        for state in STATES:
            share_dem, share_rep = voteShare(df, year, state)
            h_df.loc[index] = [year, state, share_dem, share_rep]
            index += 1

    return h_df

def SaveAll():
    # ApprovalClean().to_csv("data/approvalClean.csv", index=False)
    HouseClean().to_csv("data/houseClean.csv", index=False)
    SenateClean().to_csv("data/senateClean.csv", index=False)
    win, pres = PresClean()
    win.to_csv("data/winClean.csv", index=False)
    pres.to_csv("data/presClean.csv", index=False)

def AllClean():
    a_df = pd.read_csv("data/jar.csv")
    h_df = pd.read_csv("data/houseClean.csv")
    s_df = pd.read_csv("data/senateClean.csv")
    win_df = pd.read_csv("data/winClean.csv")
    p_df = pd.read_csv("data/presClean.csv")
    incum = {
        1976: "republican",
        1980: "democrat", 
        1984: "republican", 
        1988: "republican", 
        1992: "republican", 
        1996: "democrat", 
        2000: "democrat", 
        2004: "republican", 
        2008: "republican", 
        2012: "democrat", 
        2016: "democrat",
        2020: "republican"
    }

    df = pd.DataFrame(columns=
        [
            "year",
            "state", 
            "inc_prev_house", 
            "inc_prev_sen", 
            "inc_prev_pres", 
            "inc_appr", 
            "inc_win"
        ]
    )
    
    index = 0
    for year in range(1980, 2024, 4):
        for state in STATES:
            if incum[year] == "republican":
                inc_prev_house = h_df[(h_df["year"] == year-2) & (h_df["state"] == state)].rep_voteshare.values[0]
                if state in s_df[(s_df["year"] == year-2)].state.values:
                    inc_prev_sen = s_df[(s_df["year"] == year-2) & (s_df["state"] == state)].rep_voteshare.values[0]
                else:
                    inc_prev_sen = s_df[(s_df["year"] == year-4) & (s_df["state"] == state)].rep_voteshare.values[0]
            else:
                inc_prev_house = h_df[(h_df["year"] == year-4) & (h_df["state"] == state)].dem_voteshare.values[0]
                if state in s_df[(s_df["year"] == year-2)].state.values:
                    inc_prev_sen = s_df[(s_df["year"] == year-2) & (s_df["state"] == state)].dem_voteshare.values[0]
                else:
                    inc_prev_sen = s_df[(s_df["year"] == year-4) & (s_df["state"] == state)].dem_voteshare.values[0]
            inc_prev_pres = p_df[(p_df["year"] == year-4) & (p_df["state"] == state) & (p_df["party"] == incum[year])].voteshare.values[0]
            inc_appr = a_df[(a_df["ELECYR"] == year-4) & (a_df["STATE"] == STATES.index(state)+1)]["POS PCT"].mean()
            if incum[year] == win_df[(win_df["year"] == year) & (win_df["state"] == state)].winner.values[0]:
                inc_win = 1
            else:
                inc_win = 0

            df.loc[index] = [year, state, inc_prev_house, inc_prev_sen, inc_prev_pres, inc_appr, inc_win]
            index += 1
    df = df.fillna(method="ffill", axis=0)
    return df

# SaveAll()
df = AllClean()
df.to_csv("data/train.csv", index = False)