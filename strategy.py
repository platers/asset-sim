class Strategy:
  name = 'Strategy name'

  def __init__(self, assumptions):
    self.assumptions = assumptions

  def annual_returns(self, year, assets): # returns assets after this year
    pass

class All_in(Strategy):
  name = 'All in 1x'
  def annual_returns(self, year, assets):
    if assets < 0:
      return assets
    return assets * (1 + self.assumptions.annual_returns(year))

class Leveraged(Strategy):
  name = 'Leveraged'

  def __init__(self, assumptions, leverage):
    Strategy.__init__(self, assumptions)
    self.leverage = leverage
    self.name = 'Leveraged {:.2}x'.format(str(leverage))

  def borrowing_cost(self, assets):
    return max(0, self.assumptions.INTEREST_RATE * (self.leverage - 1) * assets)

  def annual_returns(self, year, assets):
    if assets < 0:
      return assets
    return assets * (1 + self.assumptions.annual_returns(year) * self.leverage) - self.borrowing_cost(assets)

class Half_in(Leveraged):
  def __init__(self, assumptions):
    Leveraged.__init__(self, assumptions, 1 / 2)
    self.name = 'Half in 0.5x'

class Kelly(Leveraged):
  def __init__(self, assumptions):
    leverage = (assumptions.EQUITY_RETURN_MEAN - assumptions.INTEREST_RATE) / (assumptions.EQUITY_RETURN_STD ** 2)
    Leveraged.__init__(self, assumptions, leverage)
    self.name = 'Kelly {:.2}x'.format(leverage)

class Half_Kelly(Leveraged):
  def __init__(self, assumptions):
    leverage = (assumptions.EQUITY_RETURN_MEAN - assumptions.INTEREST_RATE) / (assumptions.EQUITY_RETURN_STD ** 2) / 2
    Leveraged.__init__(self, assumptions, leverage)
    self.name = 'Half Kelly {:.2}x'.format(leverage)
    
class Lifecycle(Leveraged):
  def __init__(self, assumptions, years):
    Strategy.__init__(self, assumptions)
    self.name = 'Lifecycle max-lev {}, RRA {}'.format(assumptions.MAX_LEVERAGE, assumptions.RRA)
    self.years = years

    self.samuelson_share = (assumptions.EQUITY_RETURN_MEAN - assumptions.INTEREST_RATE) / (assumptions.EQUITY_RETURN_STD ** 2 * assumptions.RRA)

  def present_value(self, assets, start_year):
    present_value = assets
    for year in range(start_year, self.years):
      present_value += self.assumptions.annual_savings(year) / ((1 + self.assumptions.INTEREST_RATE) ** year)
    return present_value

  def annual_returns(self, year, assets):
    if assets < 0:
      return assets
    target_exposure = self.samuelson_share * self.present_value(assets, year)
    exposure = min(target_exposure, assets * self.assumptions.MAX_LEVERAGE)
    self.leverage = max(0, exposure / assets)
    return assets + exposure * self.assumptions.annual_returns(year) - self.borrowing_cost(assets)