from builddata import *
from Analysis import *


print(production_analysis(get_data()))
print(seasonal_analysis(get_data()))
print(monthly_analysis(get_data()))

