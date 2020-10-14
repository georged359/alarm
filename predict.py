import csv
from datetime import datetime
import time
import copy

"""This module predicts the future sales for the beers. It uses the import csv
module to read the csv file. It iterates through every line in the csv file and
adds the data to the relevant places depending on months due"""
def predictor():
    customer_id = []
    customer = []
    date_due = []
    beer_type = []
    gyle_num = []
    quantity = []

    total_beer_pmonth = []
    monthly_totals = [0,0,0,0,0,0,0,0,0,0,0,0] # nov to oct

    monthly_ratios = []
    for x in range(0,12):
        monthly_ratios.append([0,0,0]) # nov to oct (Pilsner, Dunkel, Helles)

    with open('Barnabys_sales_fabriacted_data.csv') as csv_doc:
        csv_file = csv.reader(csv_doc, delimiter=',')
        line_count = 0

        for rows in csv_file:
            if line_count == 0:
                line_count += 1
            else:
                customer_id.append(rows[0])
                customer.append(rows[1])
                date = datetime.strptime(rows[2], '%d-%b-%y')
                date_due.append([date.strftime('%d-%m-%Y')])
                beer_type.append(rows[3])
                gyle_num.append(rows[4])
                quantity.append(rows[5])

                month_due = int(date.strftime('%m'))
                monthly_totals[int((month_due+1)%12)] = (int(monthly_totals[(month_due+1)%12]) + int(quantity[line_count-1]))

                month_num = int((month_due+1)%12)

                """It sums up all the monthly sales for each beer"""
                if rows[3] == 'Organic Pilsner':
                    monthly_ratios[int(month_num)][0] += int(rows[5])
                elif rows[3] == 'Organic Dunkel':
                    monthly_ratios[int(month_num)][1] += int(rows[5])
                elif rows[3] == 'Organic Red Helles':
                    monthly_ratios[int(month_num)][2] += int(rows[5])
                #print(month_due , "is ",(month_due+1)%12)

                #monthly_totals[]
                line_count += 1
        """The prediction first sums all all the monthly sales for each beer
        and then calculates a growth rate for all of the beers combined by
        comparing months"""
        avrgrowth_rate = 0
        for x in range(0, len(monthly_totals)-1):
            month_to_month = (monthly_totals[x+1])/(monthly_totals[x])*100
            avrgrowth_rate += month_to_month

        avrgrowth_rate /= 11

        """The prediction next finds the average growth rate for each beer
        individually for additional accuracy"""

        avrgrowth_rate_pilsner = 0
        for x in range(0, 10):
            month_to_month = (monthly_ratios[x+1][0])/(monthly_ratios[x][0])*100
            avrgrowth_rate_pilsner += month_to_month
        avrgrowth_rate_pilsner /= 11


        avrgrowth_rate_dunkel = 0
        for x in range(0, 10):
            month_to_month = (monthly_ratios[x+1][1])/(monthly_ratios[x][1])*100
            avrgrowth_rate_dunkel += month_to_month
        avrgrowth_rate_dunkel /= 11


        avrgrowth_rate_helles = 0
        for x in range(0, 10):
            month_to_month = (monthly_ratios[x+1][1])/(monthly_ratios[x][1])*100
            avrgrowth_rate_helles += month_to_month
        avrgrowth_rate_helles /= 11

        """It then calculates the yearly percentage increase in order to calculates
        month x in the next year from month x in the previous year. It sums up
        both the individual growth rate and the total growth rate for increased
        accuracy and calcualtes the average which can then be used to predict
        the following year from the previous year"""
        avryearly_precentage_pilsner = (avrgrowth_rate_pilsner+avrgrowth_rate)/2
        avryearly_precentage_dunkel = (avrgrowth_rate_dunkel+avrgrowth_rate)/2
        avryearly_precentage_helles = (avrgrowth_rate_helles+avrgrowth_rate)/2

        """It then does the calcualtions for two years in the future Using
        the values figured above. These are appended to a list and returned."""
        next_year = copy.deepcopy(monthly_ratios)
        second_year = copy.deepcopy(monthly_ratios)
        for x in range(0,12):
            next_year[x][0] *= (avryearly_precentage_pilsner/100)
            next_year[x][0] = int(next_year[x][0])
            next_year[x][1] *= (avryearly_precentage_dunkel/100)
            next_year[x][1] = int(next_year[x][1])
            next_year[x][2] *= (avryearly_precentage_helles/100)
            next_year[x][2] = int(next_year[x][2])

        for x in range(0,12):
            second_year[x][0] *= ((avryearly_precentage_pilsner)/100)**2
            second_year[x][0] = int(second_year[x][0])
            second_year[x][1] *= ((avryearly_precentage_dunkel)/100)**2
            second_year[x][1] = int(second_year[x][1])
            second_year[x][2] *= ((avryearly_precentage_helles)/100)**2
            second_year[x][2] = int(second_year[x][2])

        return(monthly_ratios,next_year,second_year)
predictor()
