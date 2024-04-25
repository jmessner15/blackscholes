# -*- coding: utf-8 -*- 
"""
Created on Thu Jul 16 21:42:05 2020

@author: James

blackscholes oo library

class blackscholes

attributes
type; div_yield; rf_rate; volatility; spot; time; strike

methods


"""
import math
from scipy.stats import norm

class Option:
    def __init__(self, opt_type, div_yield, rf_rate, volatility, spot, time, strike):
        self.opt_type = opt_type
        self.div_yield = div_yield
        self.rf_rate = rf_rate
        self.volatility = volatility
        self.spot = spot
        self.time = time
        self.strike = strike
        if self.time == 0: self.time = 0.000001
        
        #computed attributes
        self.carry = self.rf_rate - self.div_yield
        self.d_1 = self._d_1()
        self.d_2 = self._d_2()
        self.delta = self._delta() 
        self.gamma = self._gamma()
        self.theta = self._theta(days=1, days_in_year=365)
        self.theta_7 = self._theta(days=7, days_in_year=365)
        self.vega = self._vega()
        self.rho = self._rho()
        self.rho_carry = self._rho_carry()
        self.vanna = self._vanna()
        self.volga = self._volga() 
        self.charm = self._charm()
        
        
    
    def update_opt_type(self, value, inplace=False):
        if inplace is False:
            return Option(opt_type=value, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=self.volatility, spot=self.spot, time=self.time, strike=self.strike)
        else:
            self.__init__(opt_type=value, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=self.volatility, spot=self.spot, time=self.time, strike=self.strike)
        
        
    def update_div_yield(self, value, inplace=False):
        if inplace is False:
            return Option(opt_type=self.opt_type, div_yield=value, rf_rate=self.rf_rate, volatility=self.volatility, spot=self.spot, time=self.time, strike=self.strike)
        else:
            self.__init__(opt_type=self.opt_type, div_yield=value, rf_rate=self.rf_rate, volatility=self.volatility, spot=self.spot, time=self.time, strike=self.strike)
    
    def update_rf_rate(self, value, inplace=False):
        if inplace is False:
            return Option(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=value, volatility=self.volatility, spot=self.spot, time=self.time, strike=self.strike)
        else:
            self.__init__(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=value, volatility=self.volatility, spot=self.spot, time=self.time, strike=self.strike)
        
    def update_volatility(self, value, inplace=False):
        if inplace is False:
            return Option(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=value, spot=self.spot, time=self.time, strike=self.strike)
        else:
            self.__init__(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=value, spot=self.spot, time=self.time, strike=self.strike)
    
    def update_spot(self, value, inplace=False):
        if inplace is False:
            return Option(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=self.volatility, spot=value, time=self.time, strike=self.strike)
        else:
            self.__init__(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=self.volatility, spot=value, time=self.time, strike=self.strike)
        
    def update_time(self, value, inplace=False):
        if inplace is False:
            return Option(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=self.volatility, spot=self.spot, time=value, strike=self.strike)
        else:
            self.__init__(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=self.volatility, spot=self.spot, time=value, strike=self.strike)
    
    def update_strike(self, value, inplace=False):
        if inplace is False:
            return Option(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=self.volatility, spot=self.spot, time=self.time, strike=value)
        else:
            self.__init__(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, volatility=self.volatility, spot=self.spot, time=self.time, strike=value)
    
    def _d_1(self):
        b = self.rf_rate - self.div_yield
        first_term_d1 = math.log(self.spot / self.strike)
        second_term_d1 = (b + self.volatility**2 / 2) * self.time
        numerator_d1 = first_term_d1 + second_term_d1
        denominator_d1 = self.volatility * math.sqrt(self.time)
        return numerator_d1 / denominator_d1
    
    def _d_2(self):
        return self.d_1 - (self.volatility * math.sqrt(self.time))
       
    def call_prob_exercise(self):
        return norm.cdf(self.d_2)
   
    def put_prob_exercise(self):
        return norm.cdf(-self.d_2)
    
    def prob_exercise(self):
        if self.opt_type == 'call':
            return self.call_prob_exercise()
        elif self.opt_type == 'put':
            return self.put_prob_exercise()
    
    def value(self):
        b = self.rf_rate - self.div_yield
        if self.opt_type == "call":
            first_term_value = self.spot * math.exp((b - self.rf_rate) * self.time) * norm.cdf(self.d_1)
            second_term_value = self.strike * math.exp(-self.rf_rate * self.time) * norm.cdf(self.d_2)
            return first_term_value - second_term_value
        elif self.opt_type == "put":
            first_term_value = self.strike * math.exp(-self.rf_rate * self.time) * norm.cdf(-self.d_2)
            second_term_value = self.spot * math.exp((b - self.rf_rate) * self.time) * norm.cdf(-self.d_1)
            return first_term_value - second_term_value

    def atm_iv_approx(self, mkt_price):
        return mkt_price / (0.4 * self.spot * math.exp((self.rf_rate - self.div_yield) * self.time) * math.sqrt(self.time))
   
    def implied_vol(self, mkt_price, tolerance=0.0001, search_increment=0.05):
        model_implied_vol = self.atm_iv_approx(mkt_price=mkt_price)
        dummy_option = Option(opt_type=self.opt_type, div_yield=self.div_yield, rf_rate=self.rf_rate, 
                              volatility=model_implied_vol, spot=self.spot, time=self.time, strike=self.strike)
        model_price = dummy_option.value()
        if model_price > mkt_price:
            while model_price > mkt_price: #if vol is too high, move lower until it becomes too low, then hone in on true value
                dummy_option.update_volatility(dummy_option.volatility - search_increment)
                model_price = dummy_option.value()
            lower_bound = dummy_option.volatility
            upper_bound = dummy_option.volatility + search_increment
            while abs(model_price - mkt_price) > tolerance:
                new_volatility = (upper_bound + lower_bound) / 2
                dummy_option.update_volatility(new_volatility)
                model_price = dummy_option.value()
                if model_price > mkt_price:
                    upper_bound = dummy_option.volatility
                else:
                    lower_bound = dummy_option.volatility             
            return new_volatility
        
        if model_price < mkt_price:
            while model_price < mkt_price: #if vol is too low, move higher until it becomes too high, then hone in on true value
                dummy_option.update_volatility(dummy_option.volatility + search_increment)
                model_price = dummy_option.value()
            upper_bound = dummy_option.volatility
            lower_bound = dummy_option.volatility - search_increment
            while abs(model_price - mkt_price) > tolerance:
                new_volatility = (upper_bound + lower_bound) / 2
                dummy_option.update_volatility(new_volatility)
                model_price = dummy_option.value()
                if model_price > mkt_price:
                    upper_bound = dummy_option.volatility
                else:
                    lower_bound = dummy_option.volatility
            return new_volatility
                
    def _delta(self):
        b = self.rf_rate - self.div_yield
        if self.opt_type == 'call':
            return math.exp((b - self.rf_rate) * self.time) * norm.cdf(self.d_1) 
        elif self.opt_type == 'put':
            return -math.exp((b - self.rf_rate) * self.time) * norm.cdf(-1*self.d_1)
        
    def _theta(self, days=1, days_in_year=365):
        b = self.rf_rate - self.div_yield
        if self.opt_type == 'call':
            first_term_theta = (self.spot * self.volatility * math.exp((b - self.rf_rate) * self.time) * norm.pdf(self.d_1)) / (2 * math.sqrt(self.time))
            second_term_theta = self.spot * (b - self.rf_rate) * math.exp((b - self.rf_rate) * self.time) * norm.cdf(self.d_1)
            third_term_theta = self.rf_rate * self.strike * math.exp(-self.rf_rate * self.time) * norm.cdf(self.d_2)   
            return (-first_term_theta - second_term_theta - third_term_theta) * (days / days_in_year)
        
        elif self.opt_type == 'put':
            first_term_theta = (self.spot * self.volatility * math.exp((b - self.rf_rate) * self.time) * norm.pdf(self.d_1)) / (2 * math.sqrt(self.time))
            second_term_theta = self.spot * (b - self.rf_rate) * math.exp((b - self.rf_rate) * self.time) * norm.cdf(-self.d_1)
            third_term_theta = self.rf_rate * self.strike * math.exp(-self.rf_rate * self.time) * norm.cdf(-self.d_2)      
            return (-first_term_theta + second_term_theta + third_term_theta) * (days / days_in_year)
        
    def _gamma(self):
        b = self.rf_rate - self.div_yield
        numerator_gamma = math.exp((b - self.rf_rate) * self.time) * norm.pdf(self.d_1)
        denominator_gamma = self.spot * self.volatility * math.sqrt(self.time)
        return numerator_gamma / denominator_gamma
        
    def _vega(self):
        b = self.rf_rate- self.div_yield
        return (self.spot * math.exp((b - self.rf_rate) * self.time) * norm.pdf(self.d_1) * math.sqrt(self.time)) / 100
   
    def _rho(self):
        if self.opt_type == 'call':
            return (self.time * self.strike * math.exp(-self.rf_rate * self.time) * norm.cdf(self.d_2)) / 100
        elif self.opt_type == 'put':
            return (-self.time * self.strike * math.exp(-self.rf_rate * self.time) * norm.cdf(-self.d_2)) / 100
   
    def _rho_carry(self):
        b = self.rf_rate- self.div_yield
        if self.opt_type == 'call':
            return (self.time * self.spot * math.exp((b - self.rf_rate) * self.time) * norm.cdf(self.d_1)) / 100
        elif self.opt_type == 'put':
            return (-self.time * self.spot * math.exp((b - self.rf_rate) * self.time) * norm.cdf(-self.d_1)) / 100
        
    def _vanna(self):
        b = self.rf_rate - self.div_yield
        first_term_vanna = self.vega / self.spot
        second_term_vanna = 1 - (self.d_1 / (self.volatility * math.sqrt(self.time)))
        return first_term_vanna * second_term_vanna

    def _volga(self):
        b = self.rf_rate - self.div_yield
        first_term_volga = self.vega
        second_term_volga = (self.d_1 * self.d_2) / self.volatility
        return (first_term_volga * second_term_volga) / 100
    
    def _charm(self):
        b = self.rf_rate - self.div_yield
        if self.opt_type =='call':
            first_term_charm = norm.pdf(self.d_1) * (b / (self.volatility * math.sqrt(self.time)) - self.d_2 / (2 * self.time)) 
            second_term_charm = (b - self.rf_rate) * norm.cdf(self.d_1)
            return -math.exp((b - self.rf_rate) * self.time) * (first_term_charm + second_term_charm)
        elif self.opt_type == 'put':
            first_term_charm = norm.pdf(self.d_1) * (b / (self.volatility * math.sqrt(self.time)) - self.d_2 / (2 * self.time))
            second_term_charm = (b - self.rf_rate) * norm.cdf(-self.d_1)
            return math.exp((b - self.rf_rate) * self.time) * (first_term_charm - second_term_charm)
    

