class Strategy:
  name = 'Strategy name'

  def __init__(self, assumptions):
    self.assumptions = assumptions

  def annual_returns(self, year, assets): # returns assets after this year
    pass

class All_in(Strategy):
  name = 'All in'
  def annual_returns(self, year, assets):
    return assets * (1 + self.assumptions.annual_returns(year))

class Leveraged(Strategy):
  name = 'Leveraged'

  def __init__(self, assumptions, leverage):
    Strategy.__init__(self, assumptions)
    self.leverage = leverage
    self.name = 'Leveraged ' + str(leverage)

  def borrowing_cost(self, assets):
    return max(0, self.assumptions.INTEREST_RATE * (self.leverage - 1) * assets)

  def annual_returns(self, year, assets):
    return assets * (1 + self.assumptions.annual_returns(year) * self.leverage) - self.borrowing_cost(assets)

# class Kelly(Leveraged):
#   name = 'Kelly'
#   def __init__(self):
#     self.leverage = (EQUITY_RETURN_MEAN - INTEREST_RATE) / (EQUITY_RETURN_STD ** 2)
#     self.name = 'Kelly {:.2}'.format(self.leverage)

# class Half_Kelly(Leveraged):
#   name = 'Half Kelly'
#   def __init__(self):
#     self.leverage = (EQUITY_RETURN_MEAN - INTEREST_RATE) / (EQUITY_RETURN_STD ** 2) / 2
#     self.name = 'Half Kelly {:.2}'.format(self.leverage)
    
# class Lifecycle(Leveraged):
#   name = 'Lifecycle'
#   def __init__(self, savings, years, max_leverage=MAX_LEVERAGE, rra=RRA):
#     self.name = 'Lifecycle max-lev {}, RRA {}'.format(max_leverage, rra)
#     self.max_leverage = max_leverage
#     self.years = years
#     self.savings = savings

#     self.samuelson_share = (EQUITY_RETURN_MEAN - INTEREST_RATE) / (EQUITY_RETURN_STD ** 2 * rra)
#     print('samuelson share', self.samuelson_share)

#   def present_value(self, assets, start_year):
#     present_value = assets
#     for year in range(start_year, years):
#       present_value += self.savings(year) / ((1 + INTEREST_RATE) ** year)
#     return present_value

#   def annual_returns(self, year, assets):
#     target_exposure = self.samuelson_share * self.present_value(assets, year)
#     exposure = min(target_exposure, assets * self.max_leverage)
#     self.leverage = max(0, exposure / assets)
#     return assets + exposure * cagr(year) - self.borrowing_cost(assets)