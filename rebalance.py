# Import the libraries we will use here
import datetime
import pandas as pd


# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
def initialize(context):
    pass

# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    # Implement your algorithm logic here.

    # data[sid(X)] holds the trade event data for that security.
    # context.portfolio holds the current portfolio state.
    # In our example, we're looking at 9 sector ETFs.  
    context.secs = symbols('XLY',  # XLY Consumer Discrectionary SPDR Fund   
                           'XLF',  # XLF Financial SPDR Fund  
                           'XLK',  # XLK Technology SPDR Fund  
                           'XLE',  # XLE Energy SPDR Fund  
                           'XLV',  # XLV Health Care SPRD Fund  
                           'XLI',  # XLI Industrial SPDR Fund  
                           'XLP',  # XLP Consumer Staples SPDR Fund   
                           'XLB',  # XLB Materials SPDR Fund  
                           'XLU')  # XLU Utilities SPRD Fund

    # This variable is used to manage leverage
    context.weights = 0.99/len(context.secs)
    rebalance(context, data)

def rebalance(context, data):

    # Do nothing if there are open orders:
    if has_orders(context):
        print('has open orders - doing nothing!')
        return

    # Do the rebalance. Loop through each of the stocks and order to the target percentage.  If already at the target, this command doesn't do anything.
    ###### A future improvement could be to set rebalance thresholds.
    for sec in context.secs:
        order_target_percent(sec, context.weights, limit_price=None, stop_price=None)
        log.info("Rebalanced %s to %f" % (str(sec), context.weights))
    
    
def has_orders(context):
    # Return true if there are pending orders.
    has_orders = False
    for sec in context.secs:
        orders = get_open_orders(sec)
        if orders:
            for oo in orders:                  
                message = 'Open order for {amount} shares in {stock}'  
                message = message.format(amount=oo.amount, stock=sec)  
                log.info(message)

            has_orders = True
    return has_orders