import pypsa
import pandas as pd

## to get a time series of 24 hours 
time_index = pd.date_range("2026-06-01", periods=24, freq="h")

## wind profile of 24 hrs
wind_profile = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.7, 0.5,
                0.3, 0.2, 0.2, 0.3, 0.4, 0.3, 0.2, 0.3,
                0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5, 0.4]


##this is a container of rules and inputs basically
network = pypsa.Network()

##View Points into each hour
network.set_snapshots(time_index)


##Now we add our connection points which is our Buses,these points baiscally help
##us connect the generator to the load
network.add("Bus", "main_electrical_node")


##we now add the consumer or the costs of the node i.e. a load
##this will be connected via our bus
##here the cost we are bearing is a 100 MegaWatts(p_set)
network.add("Load", "City_load", bus="main_electrical_node", p_set=100)  


##our wind generator 
network.add("Generator","Wind_Turbine",bus="main_electrical_node",
            p_nom = 100,marginal_cost = 5)

##mapping our wind generators capabilites to the wind proflie
network.generators_t.p_max_pu['Wind_Turbine'] = wind_profile

##backup gas trubine if the wind generator doesnt produce power
network.add("Generator","Gas_Turbine",bus="main_electrical_node",
            p_nom = 100,marginal_cost = 30)

##batter for discharging or charging 
network.add("StorageUnit","battery",bus="main_electrical_node",p_nom = 50,max_hours = 4,marginal_cost = 0 )

##validation 
network.sanitize()


##optiminizes for the minimum cosw
network.optimize(solver_name="highs")


##To show time series output for generators for each hour
print(network.generators_t.p)


##to show time series discharg (+) and charge (-)for the battery 
print(network.storage_units_t.p)