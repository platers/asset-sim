import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

np.random.seed(41238)

st.title('My first app')

MAX_LEVERAGE = 3 # all in is 1
INTEREST_RATE = 0.015 # cost of borrowing money
STARTING_AMOUNT = 10_000 # avoids divide by 0 errors
EQUITY_RETURN_MEAN = 0.08
EQUITY_RETURN_STD = 0.12
RRA = 1.2 # relative risk aversion, 1 is log utility



def income(year): # somewhat ambitious SWE progression
  if year < 6:
    return 200_000
  if year < 10:
    return 350_000
  if year < 40:
    return 500_000
  return 0 # retirement

def tax_rate(income):
  return 0.4 # high estimate

def expenses(post_tax_income):
  spending_rate = 0.20
  return max(min(post_tax_income * spending_rate, 50_000), 20_000)

def savings(year):
  inc = income(year)
  post_tax = inc * (1 - tax_rate(inc))
  net = post_tax - expenses(post_tax)
  return net

def cagr(year):
  # https://towardsdatascience.com/are-stock-returns-normally-distributed-e0388d71267e
  # SPY annual returns, not actually cagr, bad naming
  return np.random.normal(EQUITY_RETURN_MEAN, EQUITY_RETURN_STD)
  # optimistic returns
  #return np.random.normal(0.15, 0.20)

class Strategy:
  name = 'Strategy name'

  def annual_returns(self, year, assets): # returns assets after this year
    pass

class All_in(Strategy):
  name = 'All in'
  def annual_returns(self, year, assets):
    return assets * (1 + cagr(year))

class Leveraged(Strategy):
  name = 'Leveraged'
  def __init__(self, leverage):
    self.leverage = leverage
    self.name = 'Leveraged ' + str(leverage)

  def borrowing_cost(self, assets):
    return max(0, INTEREST_RATE * (self.leverage - 1) * assets)

  def annual_returns(self, year, assets):
    return assets * (1 + cagr(year) * self.leverage) - self.borrowing_cost(assets)

class Kelly(Leveraged):
  name = 'Kelly'
  def __init__(self):
    self.leverage = (EQUITY_RETURN_MEAN - INTEREST_RATE) / (EQUITY_RETURN_STD ** 2)
    self.name = 'Kelly {:.2}'.format(self.leverage)

class Half_Kelly(Leveraged):
  name = 'Half Kelly'
  def __init__(self):
    self.leverage = (EQUITY_RETURN_MEAN - INTEREST_RATE) / (EQUITY_RETURN_STD ** 2) / 2
    self.name = 'Half Kelly {:.2}'.format(self.leverage)
    
class Lifecycle(Leveraged):
  name = 'Lifecycle'
  def __init__(self, savings, years, max_leverage=MAX_LEVERAGE, rra=RRA):
    self.name = 'Lifecycle max-lev {}, RRA {}'.format(max_leverage, rra)
    self.max_leverage = max_leverage
    self.years = years
    self.savings = savings

    self.samuelson_share = (EQUITY_RETURN_MEAN - INTEREST_RATE) / (EQUITY_RETURN_STD ** 2 * rra)
    print('samuelson share', self.samuelson_share)

  def present_value(self, assets, start_year):
    present_value = assets
    for year in range(start_year, years):
      present_value += self.savings(year) / ((1 + INTEREST_RATE) ** year)
    return present_value

  def annual_returns(self, year, assets):
    target_exposure = self.samuelson_share * self.present_value(assets, year)
    exposure = min(target_exposure, assets * self.max_leverage)
    self.leverage = max(0, exposure / assets)
    return assets + exposure * cagr(year) - self.borrowing_cost(assets)
    


def simulate(years, strategy):
  assets = STARTING_AMOUNT
  data = []
  for year in range(years):
    assets = strategy.annual_returns(year, assets)
    assets += savings(year)
    assets = max(assets, 1000) # bankruptcy
    data.append(assets)
  return data
  
def graph_lines(years, strategy, runs=1, reduction=None, color='blue'): # if reduction is None plot all lines
  data = []
  for run in range(runs):
    data.append(simulate(years, strategy))
  if reduction:
    plt.plot(reduction(data, 0), label=strategy.name, color=color)
  else:
    for d in data:
      plt.plot(d, label=strategy.name, color=color)

def graph(strategies, years=20, runs=5, reduction=None, title='Assets over time'):
  fig = plt.figure()
  plt.xlabel('Year')
  plt.ylabel('Assets')
  plt.title(title)
  #plt.yscale('log')
  cmap = plt.get_cmap('plasma')
  colors = cmap(np.linspace(0, 0.9, len(strategies)))
  for strategy, color in zip(strategies, colors):
    graph_lines(years, strategy, runs=runs, reduction=reduction, color=color)

  handles, labels = plt.gca().get_legend_handles_labels()
  labels, ids = np.unique(labels, return_index=True)
  handles = [handles[i] for i in ids]
  plt.legend(handles, labels, loc='best')
  return fig

years = 30
target_exposure = simulate(years, All_in())[-1] * 0.8 # target exposure should be picked more carefully
lifecyle = Lifecycle(savings, years)
st.pyplot(graph([All_in(), lifecyle], years=years, runs=20))
graph([All_in(), lifecyle, Leveraged(3), Kelly()], years=years, runs=5)