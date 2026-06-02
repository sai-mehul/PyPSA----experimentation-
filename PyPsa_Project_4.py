import pypsa 
import numpy as np 


##this is a part of our montecarlo simulation framework wherein we're trying to 
##brute force all the possible results within the same random experiment 
n_simulations = 10 
costs = []

for i in range(n_simulations):

  ##for the range of 0 to 999 (basically a 1000 elements if we're concidering 0
  ##as the first elemen) we generate the random wind profiles for the said 24 
  ##hours  
  wind_profile = np.clip(np.random.normal(0,0.1,24),0,1)
  

  ##we now for each simulation generate its individual networks 
  network = pypsa.Network()

  network.set_snapshots(range(24))

  network.add("Bus", "main_electrical_node")


  network.add("Load", "City_load", bus="main_electrical_node", p_set=100)

  network.add("Generator","Wind_Turbine",bus="main_electrical_node",
            p_nom = 100,marginal_cost = 5)

  network.generators_t.p_max_pu['Wind_Turbine'] = wind_profile

  network.add("Generator","Gas_Turbine",bus="main_electrical_node",
            p_nom = 100,marginal_cost = 30)
  
  network.sanitize()

  network.optimize(solver_name="highs")
  
  status, condition = network.optimize(solver_name="highs")



  ##This is done to add only the feasable costs within the cost array of the
  ##whole simulations basically showing all the possible fesable costs 
  if status == 'ok':
    costs.append(network.objective)
  else:
    costs.append(np.nan)
  


##this is done to see the worst possible cases using the Value @ Risk concept
##from finance 
costs = np.array(costs)
var_95 = np.percentile(costs, 95)
cvar_95 = costs[costs >= var_95].mean()

print(f"Expected Cost: {costs.mean():.2f}")
print(f"VaR (95%): {var_95:.2f}")
print(f"CVaR (95%): {cvar_95:.2f}")


  


