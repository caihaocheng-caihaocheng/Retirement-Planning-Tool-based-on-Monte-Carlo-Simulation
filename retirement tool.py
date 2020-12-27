import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


def simulate_result(y, x2, x4, x6, x8, lenOfSimulation):
    #suppose 60-y-o reteire and to 100 y-o
    #first year is calculated in advance
    years = 39
    total_result = {}
    #total_result.append({"index": 0, "value": y})
    total_result[0] = y
    for i in range(years):
        count = i + 1
        x3 = np.random.normal(loc = 0, scale = 0.08, size = lenOfSimulation)
        x5 = np.random.normal(loc = 0, scale = 0.03, size = lenOfSimulation)
        x7 = np.random.normal(loc = 50000, scale = 10000*0.3, size = lenOfSimulation)
        y = (y * x2 * (1 + x3) + y * x4 * (1 + x5) + y * (1 - x2 - x4) * (1 + x6) - x7) * (1 + x8)
        #total_result.append({"index": count, "value": y})
        total_result[count] = y
    return total_result


# ascending sorting
def sort_result(input_result):
    sorted_result = []
    for i in range(len(input_result)):
        sorted_result.append(sorted(input_result[i]))
    return sorted_result


def extract_percentile(sorted_result, lenOfSimulation):
    #since we siumlate 1000 for each age, thus the corresponding perceltile is x*1000
    _10th_p = []
    _25th_p = []
    _50th_p = []
    _75th_p = []
    _95th_p = []
    
    _10th = int(0.1 * lenOfSimulation)
    _25th = int(0.25 * lenOfSimulation)
    _50th = int(0.50 * lenOfSimulation)
    _75th = int(0.75 * lenOfSimulation)
    _95th = int(0.95 * lenOfSimulation)
    
    for i in range(len(sorted_result)):
        _10th_p.append(sorted_result[i][_10th])
        _25th_p.append(sorted_result[i][_25th])
        _50th_p.append(sorted_result[i][_50th])
        _75th_p.append(sorted_result[i][_75th])
        _95th_p.append(sorted_result[i][_95th])
    return _10th_p, _25th_p, _50th_p, _75th_p, _95th_p


def count_success_p(sorted_result, lenOfSimulation):
    p_list = []
    for i in range(len(sorted_result)):
        temp_len = len([w for w in range(len(sorted_result[i])) if sorted_result[i][w] > 0])
        p_list.append(temp_len/lenOfSimulation)
    return p_list


def count_frequence(input_result, lenOfSimulation):
    inter_num = 300
    frequency_distributions = {}
    money = {}
    for year in input_result.keys():
        max_val = max(input_result[year])
        min_val = min(input_result[year])
        inter_len = (max_val - min_val)/inter_num
        frequency_distribution = np.zeros(inter_num)
        
        ith_year_money = []
        for i in range(inter_num):
            ith_year_money.append(min_val+i*inter_len)
        
        for value in input_result[year]:
            if value == max_val:
                position = divmod(value-min_val,inter_len)[0]-1
            else:
                position = divmod(value-min_val,inter_len)[0]
            frequency_distribution[int(position)] += 1
        money[year] = ith_year_money
        frequency_distribution /= lenOfSimulation
        frequency_distributions[year] = frequency_distribution
    return frequency_distributions, money


def main():
    
    while True:
        mode = input("Please choose Mode (Mode 1 is the probability you will still have money,Mode 2 is the probability how many money do you still have in ith year): ")
        if mode == "1" or mode == "2":
            mode = eval(mode)
            break
        else:
            print("You should input a number\n")

    while True:
        #remaining money at 60 years old
        #x1 = 1100000
        x1 = input("Please input the remaining money at 60 years old: ")
        if is_number(x1) == True:
            break
        else:
            print("You should input a number\n")
    x1 = eval(x1)
        
    while True:
        #stock percentage
        #x2 = 0.2
        x2 = input("Please input a percentage on investing Stock: ")
        if is_number(x2) == True: 
            x2 = eval(x2)
            if x2 > 1:
                print("Please input a value smaller than or equal than 1: ")
            else:
                break
        else:
            print("You should input a number\n")
    
    while True:
        #bond percentage
        #x4 = 0.3
        x4 = input("Please input a percentage on investing Bond: ")
        if is_number(x4) == True: 
            x4 = eval(x4)
            if x4 + x2 > 1:
                print("Please input a value to make the addition of bond percentage and stock percentage to smaller than or equal than 1\n")
            else:
                break
        else:
            print("You should input a number\n")
            
    while True:
        #annual interest
        #x6 = 0.03
        x6 = input("Please input a percentage on Annual Interest from the bank: ")
        if is_number(x6) == True:
            x6 = eval(x6)
            break
        else:
            print("You should input a number\n")
            
    while True:
        #annual cost
        x7_cost = input("Please input an Annual Cost every year: ")
        if is_number(x7_cost) == True:
            x7_cost = eval(x7_cost)
            break
        else:
            print("You should input a number\n")
            
    
    while True:
        #inflation
        #x8 = 0.017
        x8 = input("Please input a Inflation rate: ")
        if is_number(x8) == True:
            x8 = eval(x8)
            break
        else:
            print("You should input a number\n")
            
    
    
    if mode == 2:
        while True:
            #which year do you want to know how many money remains
            #ith_year = 10
            ith_year = input("Input an age that you may have different deposits with different probabilities: ")
            if is_number(ith_year) == True:
                ith_year = eval(ith_year)
                if ith_year > 60 and ith_year < 100:
                    ith_year = ith_year - 60
                    break
                else:
                    print("You should input a number which is bigger than 60 and smaller than 100\n")
            else:
                print("You should input a number\n")
                
                
    
    #number of simulation 
    lenOfSimulation = 10000

    
    #stock return rate   -10%---+10%
    x3 = np.random.normal(loc = 0, scale = 0.08, size = lenOfSimulation)
    df_x3 = pd.DataFrame(x3)
    
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(2,1,1)
    ax1.scatter(df_x3.index, df_x3.values)
    plt.grid()
    
    ax2 = fig.add_subplot(2,1,2)
    df_x3.hist(bins = 50, alpha = 0.5, ax = ax2)
    df_x3.plot(kind = 'kde', secondary_y = True, ax = ax2)
    plt.grid()
    
    #bond return rate -5%---+5%
    x5 = np.random.normal(loc = 0, scale = 0.03, size = lenOfSimulation)
    df_x5 = pd.DataFrame(x5)
    
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(2,1,1)
    ax1.scatter(df_x5.index, df_x5.values)
    plt.grid()
    
    ax2 = fig.add_subplot(2,1,2)
    df_x5.hist(bins = 50, alpha = 0.5, ax = ax2)
    df_x5.plot(kind = 'kde', secondary_y = True, ax = ax2)
    plt.grid()
    
    
    #annual cost 
    x7 = np.random.normal(loc = x7_cost, scale = 10000*0.3, size = lenOfSimulation)
    #print(max(x7))
    #print(min(x7))
    
    df_x7 = pd.DataFrame(x7)
    
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(2,1,1)
    ax1.scatter(df_x7.index, df_x7.values)
    plt.grid()
    
    ax2 = fig.add_subplot(2,1,2)
    df_x7.hist(bins = 50, alpha = 0.5, ax = ax2)
    df_x7.plot(kind = 'kde', secondary_y = True, ax = ax2)
    plt.grid()
    plt.show()
    
    y1 = (x1*x2*(1+x3) + x1*x4*(1+x5) + x1*(1-x2-x4)*(1+x6) - x7)*(1+x8)
    total_result = simulate_result(y1,x2,x4,x6,x8,lenOfSimulation)
    sorted_result = sort_result(total_result)
    _10th_p, _25th_p, _50th_p, _75th_p, _95th_p = extract_percentile(sorted_result, lenOfSimulation)
    result_success_p = count_success_p(sorted_result, lenOfSimulation)
    x_data = [i for i in range(40)]
    

        
    plt.plot(x_data, _10th_p, "-o", color = "r", label = "10th percentile")
    plt.plot(x_data, _25th_p, "-o", color = "b", label = "25th percentile")
    plt.plot(x_data, _50th_p, "-o", color = "y", label = "50th percentile")
    plt.plot(x_data, _75th_p, "-o", color = "grey", label = "75th percentile")
    plt.plot(x_data, _95th_p, "-o", color = "purple", label = "95th percentile")
    plt.legend()
    plt.show()
    
    plt.plot(x_data, result_success_p, "-o", color = 'b', label = "Probability")
    plt.legend()
    plt.show()
    
    if mode == 2:
        
        result, money = count_frequence(total_result, lenOfSimulation)
        accumulated_probability = result[ith_year].copy()
        for i in range(1,len(accumulated_probability)):
            accumulated_probability[i] = accumulated_probability[i-1] + accumulated_probability[i]
        
        plt.plot(money[ith_year], result[ith_year], label = "Probability")
        plt.legend()
        plt.show()
        
        plt.plot(money[ith_year],1-accumulated_probability, label = "Accumulated Probability")
        plt.legend()
        plt.show()
    
       
main()