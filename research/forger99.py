"""SpaceSleepTwin 2.0: mechanistic Forger99 circadian light model.
Exploratory scenarios, not validated astronaut predictions.
Reference: Forger, Jewett & Kronauer (1999), DOI 10.1177/074873099129000867.
Parameters and equations: https://arcascope.github.io/circadian/api/models.html
Light inputs here are photopic lux, not melanopic EDI.
"""
import argparse, json
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

PROFILES = {
 "static": lambda h: 210.0 if h < 16 else 0.0,
 "dynamic": lambda h: 420.0 if h < 10 else 210.0 if h < 13 else 90.0 if h < 16 else 0.0,
 "late_bright": lambda h: 210.0 if h < 10 else 420.0 if h < 16 else 0.0,
}
def rhs(t, y, tau, profile):
    x, xc, n = y
    I = PROFILES[profile](t % 24)
    alpha = 0.05 * (I / 9500.0) ** 0.5 if I > 0 else 0.0
    B = 33.75 * (1-n) * alpha * (1-0.4*x) * (1-0.4*xc)
    return [
        np.pi/12 * (xc+B),
        np.pi/12 * (0.23*(xc-4*xc**3/3)-x*((24/(0.99669*tau))**2+0.55*B)),
        60*(alpha*(1-n)-0.0075*n),
    ]
def simulate(days=45, tau=24.2, profile="dynamic", step_hours=0.25):
    if profile not in PROFILES: raise ValueError("Unknown lighting profile")
    if not 1 <= days <= 180: raise ValueError("days must be 1..180")
    if not 23 <= tau <= 26: raise ValueError("tau must be 23..26")
    times = np.arange(0, days*24 + step_hours/2, step_hours)
    sol = solve_ivp(lambda t,y: rhs(t,y,tau,profile), (0,days*24), [1.0,0.0,0.5],
                    t_eval=times, rtol=1e-7, atol=1e-9, max_step=0.25)
    if not sol.success: raise RuntimeError(sol.message)
    return pd.DataFrame({"time_hours":sol.t,"day":sol.t/24,
      "clock_x":sol.y[0],"clock_xc":sol.y[1],"photoreceptor_state_n":sol.y[2],
      "photopic_lux":[PROFILES[profile](t%24) for t in sol.t],
      "scenario":profile})
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--days",type=int,default=45)
    parser.add_argument("--tau",type=float,default=24.2)
    parser.add_argument("--out",default="forger99_scenarios.csv")
    a=parser.parse_args()
    results=pd.concat([simulate(a.days,a.tau,p) for p in PROFILES],ignore_index=True)
    results.to_csv(a.out,index=False)
    print(json.dumps({"output":a.out,"rows":len(results),"scenarios":list(PROFILES),
       "status":"Mechanistic Forger99 model; uncalibrated and unvalidated for spaceflight"}))
