import numpy as np
import pandas as pd

k  = pd.read_csv("BambooAE.csv") #BambooHR
# print(k.head(5))
h  = pd.read_csv("MAXIO.csv") #MAXIO
# print(h.head(5))

m = h[~h["User Email"].isin(k["Work Email"])]  ##for deactivated users in MAXIO
# m.to_csv("Maxiodeactivated_users.csv", index=False)
# print(m.drop_duplicates("User Email"))

j  = pd.read_csv("LaunchDarkly.csv")
n = j[~j["email"].isin(k["Work Email"])]
# print(n)
# n.to_csv("LaunchDarklydeactivated_users.csv", index=False)

p  = pd.read_csv("Assem.csv") #ASSEMBLED
q = p[~p["Email"].isin(k["Work Email"])]
# print(q)

a  = pd.read_csv("Microsoft.csv")
b = a[
    ~a["User principal name"].str.lower().fillna("").isin(
        k["Work Email"].str.lower().fillna("")
    )
]
print(b)

c  = pd.read_csv("Adobe.csv")
d = c[
      ~c["Email"].str.lower().isin(k["Work Email"].str.lower())]
print(d)
