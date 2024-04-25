# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:14:16 2024

@author: JMessner
"""

from blackscholes import Option
import numpy as np


DAYS_IN_YEAR = 365

class Position:
    #contains option objects and number of contracts
    def __init__(self, name, contracts, option=None, option_data=None, multiplier=100):
        self.name = name
        self.contracts = contracts
        self.multiplier = multiplier
        
        if option is not None:
            if option_data is not None:
                raise ValueError("enter either an option object, or a dictionary with the info needed to create an option object, not both")
            self.option = option
        elif option_data is not None:
            if option is not None:
                raise ValueError("enter either an option object, or a dictionary with the info needed to create an option object, not both")
            
            opt_type = option_data[0]
            div_yield = option_data[1]
            rf_rate = option_data[2]
            volatility = option_data[3]
            spot = option_data[4]
            time = option_data[5]
            strike = option_data[6]
            
            self.option = Option(opt_type=opt_type, div_yield=div_yield, rf_rate=rf_rate, 
                                 volatility=volatility, spot=spot, time=time, strike=strike)
            
        else:
            raise ValueError("an option should be provided")
        
    def value(self):
        return self.contracts * self.option.value() * self.multiplier
    
    def dollar_delta(self):
        position_delta = self.contracts * self.option.delta * self.multiplier
        return position_delta * self.option.spot
    
    def dollar_gamma(self):
        position_gamma = self.contracts * self.option.gamma * self.multiplier
        return position_gamma * (self.option.spot ** 2 / 100)
    
    def dollar_vega(self):
        return self.contracts * self.option.vega * self.multiplier
    
    def dollar_theta(self, days=1, days_in_year=365):
        return self.contracts * self.option._theta(days=days, days_in_year=days_in_year) * self.multiplier
    
    def value_by_spot(self, spot_range, days_fwd=None, days_in_year=DAYS_IN_YEAR, at_expiration=True):
        if days_fwd is not None:
            new_time = self.option.time - (days_fwd / days_in_year)
            if new_time < 0:
                raise ValueError('days_fwd is greater than remaining time, use at_expiration=True')
        else:
            new_time = 0
        
        opt = self.option.update_time(new_time)
        
        opt_values = {}
        
        for spot in spot_range:
            opt_inner = opt.update_spot(spot)
            opt_values[spot] = opt_inner.value()
        
        return opt_values
    
    def value_by_vol(self, vol_range, days_fwd=0, days_in_year=DAYS_IN_YEAR):
        new_time = self.option.time - (days_fwd / days_in_year)
        opt = self.option.update_time(new_time)    
        opt_values = {}
        
        for vol in vol_range:
            opt_values[vol] = opt.update_volatility(vol).value()
        
        return opt_values
    
    def value_by_time(self, time_range):
        opt_values = {}
        opt = self.option
        
        for time in time_range:
            opt_values[time] = opt.update_time(time).value()
        
        return opt_values
    
    def value_grid_spot_vol(self, spot_range, vol_range, days_fwd, days_in_year=DAYS_IN_YEAR):
        pass
        
        new_time = self.option.time - (days_fwd / days_in_year)
        opt = self.option.update_time(new_time)          
        
        grid = np.zeros((len(spot_range), len(vol_range)))
        
        for i in range(len(spot_range)):
            opt = opt.update_spot(spot_range[i])
            for j in range(len(vol_range)):
                opt = opt.update_volatility(vol_range[j])
                grid[i,j] = opt.value()
        
        return grid
         
        
    def delta_by_time(self, time_range):
        deltas = {}
        opt = self.option
        
        for time in time_range:
            deltas[time] = opt.update_time(time).delta
        
        return deltas
    
    def delta_by_spot(self, spot_range, days_fwd=0, days_in_year=DAYS_IN_YEAR):
        new_time = self.option.time - (days_fwd / days_in_year)
        opt = self.option.update_time(new_time)    
        deltas = {}
        
        for spot in spot_range:
            deltas[spot] = opt.update_spot(spot).delta
        
        return deltas
    
    def delta_by_vol(self, vol_range, days_fwd=0, days_in_year=DAYS_IN_YEAR):
        new_time = self.option.time - (days_fwd / days_in_year)
        opt = self.option.update_time(new_time)
        deltas = {}
        
        for vol in vol_range:
            deltas[vol] = opt.update_volatility(vol).delta
        
        return deltas
    

    
class MultiLeg:
    #contains position objects
    #initiate with a list of positions {name: position object}
    
    def __init__(self, positions, spot=100):
        self.positions = positions
        self.spot = spot
        
    def value(self):
        position_values = [p.value() for p in self.positions]
        return np.sum(position_values)
    
    def pos_values(self):
        d = {}
        for p in self.positions:
            d[p.name] = p.value()
        return d
    
    def pos_prices(self):
        d = {}
        for p in self.positions:
            d[p.name] = p.option.value()
        return d
    
    def pos_dte(self):
        d = {}
        for p in self.positions:
            d[p.name] = p.option.time * DAYS_IN_YEAR
        return d
    
    def dollar_delta(self):
        position_deltas = [p.dollar_delta() for p in self.positions]
        return np.sum(position_deltas)
    
    def pos_dollar_delta(self):
        d = {}
        for p in self.positions:
            d[p.name] = p.dollar_delta()
        return d
    
    def dollar_vega(self):
        position_vegas = [p.dollar_vega() for p in self.positions]
        return np.sum(position_vegas)
    
    def pos_dollar_vega(self):
        d = {}
        for p in self.positions:
            d[p.name] = p.dollar_vega()
        return d
    
    def dollar_gamma(self):
        position_gammas = [p.dollar_gamma() for p in self.positions]
        return np.sum(position_gammas)
    
    def pos_dollar_gamma(self):
        d = {}
        for p in self.positions:
            d[p.name] = p.dollar_gamma()
        return d
    
    def dollar_theta(self):
        position_thetas = [p.dollar_theta() for p in self.positions]
        return np.sum(position_thetas)

    def pos_dollar_theta(self):
        d = {}
        for p in self.positions:
            d[p.name] = p.dollar_theta()
        return d
    
    def value_by_spot(self, spot_levels, days_fwd=None, at_expiration=True, days_in_year=DAYS_IN_YEAR):
        
        updated_positions = []
        for p in self.positions:
            name = p.name
            contracts = p.contracts
            option = p.option
            updated_positions.append(Position(name, contracts, option))
        
        min_time = min([p.option.time for p in updated_positions])
        
        if days_fwd is not None:
            time_step = days_fwd / days_in_year
            if time_step > min_time:
                raise ValueError('days_fwd is greater than one position\'s remaining time')    
        elif at_expiration == True:
            time_step = min_time
        
        elif at_expiration == False:
            time_step = 0
            
        for p in updated_positions:
            new_time = p.option.time - time_step
            p.option = p.option.update_time(new_time, inplace=False)
            
        updated_position_values = []
        for i in range(len(spot_levels)):
            inner_position_values = []
            for p in updated_positions:
                inner_position_values.append(Position(p.name, p.contracts, p.option.update_spot(spot_levels[i])).value())
            updated_position_values.append(sum(inner_position_values))
        
        return updated_position_values
        
    def value_grid_spot_vol(self, spot_levels, vol_levels, days_fwd=None, at_expiration=True, days_in_year=DAYS_IN_YEAR):
        
        updated_positions = []
        for p in self.positions:
            name = p.name
            contracts = p.contracts
            option = p.option
            updated_positions.append(Position(name, contracts, option))
            
        min_time = min([p.option.time for p in updated_positions])
        
        if days_fwd is not None:
            time_step = days_fwd / days_in_year
            if time_step > min_time:
                raise ValueError('days_fwd is greater than one position\'s remaining time')
        elif at_expiration == True:
            time_step = min_time
        elif at_expiration == False:
            time_step=0
        
        for p in updated_positions:
            new_time = p.option.time - time_step
            p.option = p.option.update_time(new_time, inplace=False)
    
        updated_position_values = np.zeros((len(vol_levels), len(spot_levels)))
        
        for i in range(len(vol_levels)):
            for j in range(len(spot_levels)):
                for p in updated_positions:
                    p.option.update_spot(spot_levels[j], inplace=True)
                    p.option.update_volatility(vol_levels[i], inplace=True)
                    updated_position_values[i,j] = updated_position_values[i,j] + p.value()
        
        return updated_position_values
    
    def value_grid_spot_vol_shocks(self, spot_shocks, vol_shocks, days_fwd=None, at_expiration=True, days_in_year=DAYS_IN_YEAR):
        
        updated_positions = []
        for p in self.positions:
            name = p.name
            contracts = p.contracts
            option = p.option
            updated_positions.append(Position(name, contracts, option))
            
        min_time = min([p.option.time for p in updated_positions])
        
        if days_fwd is not None:
            time_step = days_fwd / days_in_year
            if time_step > min_time:
                raise ValueError('days_fwd is greater than one position\'s remaining time')
        elif at_expiration == True:
            time_step = min_time
        elif at_expiration == False:
            time_step=0
        
        for p in updated_positions:
            new_time = p.option.time - time_step
            p.option = p.option.update_time(new_time, inplace=False)
    
        updated_position_values = np.zeros((len(vol_shocks), len(spot_shocks)))
        
        original_position_dict = {}
        for pos in self.positions:
            original_position_dict[pos.name] = pos
        
        for i in range(len(vol_shocks)):
            for j in range(len(spot_shocks)):
                for p in updated_positions:
                    new_spot = original_position_dict[p.name].option.spot + spot_shocks[j]
                    if new_spot <= 0:
                        new_spot = 0.0001    
                    
                    new_vol = original_position_dict[p.name].option.volatility + vol_shocks[i]
                    if new_vol <= 0:
                        new_vol = 0.0001
             
                    p.option.update_spot(new_spot, inplace=True)
                    p.option.update_volatility(new_vol, inplace=True)
                    updated_position_values[i,j] = updated_position_values[i,j] + p.value()
        
        return updated_position_values
    
        
    '''
        updated_position_values = np.zeros((len(spot_shocks),len(vol_shocks)))
        
        for i in range(len(updated_positions)):
            p = updated_positions[i]
            values_inner = np.zeros_like(updated_position_values)
            for j in range(len(spot_shocks)):
                new_spot = p.option.spot + spot_shocks[j]
                p.option = p.option.update_spot(new_spot)
                for k in range(len(vol_shocks)):
                    new_vol = p.option.volatility + vol_shocks[k]
                    p.option = p.option.update_volatility(new_vol)
                    values_inner[j,k] = p.option.value()
            updated_position_values = updated_position_values + values_inner
        
        return updated_position_values
    '''