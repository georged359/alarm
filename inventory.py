from flask import Flask, request, render_template, jsonify
from predict import predictor
import time

"""Appends all the details for each tank to a list which can easilly be
accessed. including info about the current tasks that it is doing"""

"""in use(boolean),time started,volume,capabilities,name,time done"""
tanks = []
tanks.append([False,None,1000,['F','C'],'Albert',None])
tanks.append([False,None,800,['F','C'],'Brigadier',None])
tanks.append([False,None,1000,['F','C'],'Camilla',None])
tanks.append([False,None,800,['F','C'],'Dylon',None])
tanks.append([False,None,1000,['F','C'],'Emily',None])
tanks.append([False,None,800,['F','C'],'Florence',None])
tanks.append([False,None,680,['C'],'Gertrude',None])
tanks.append([False,None,680,['C'],'Harry',None])
tanks.append([False,None,800,['F'],'R2D2',None])

"""Makes lists to store the processes currently in each stage of brewing"""
stage1 = []
stage2 = []
stage3 = []
stage4 = []

"""global variables to keep the amount of stock for each beer"""
global Pstock
global Dstock
global Hstock
Pstock = 0
Dstock = 0
Hstock = 0

app = Flask(__name__)

"""The home page holds all the relevant info about the current processes and
which tanks are currently being used. Also enables the user to interact,
modify,start and end processes. it will display all the info. Using the
module flask to make a gui in the form of a webpage. The html document home.html
will use get requests to send data back to python where it is used"""
@app.route('/')
def home():
    global Pstock
    global Dstock
    global Hstock

    equipment = request.args.get('equip')
    process = request.args.get('proc')
    volume = request.args.get('volume')
    beer = request.args.get('beer')

    process2 = request.args.get('proc2')
    volume2 = request.args.get('volume2')
    beer2 = request.args.get('beer2')

    number = request.args.get('numb')
    proc_canc = request.args.get('proc_canc')

    beer3 = request.args.get('beer3')
    quantity = request.args.get('quantity')

    beer4 = request.args.get('beer4')
    quantity2 = request.args.get('quantity2')

    """Starts processes by validating that the data entered is acceptable and also
    checks that the chosen tank is not currently in use. It updates the info for
    the table which the user sees to show the process info such as start time, end
    time, volume and beer type. It will also return relevant errors depending on
    the input"""
    if equipment:
        if tanks[int(equipment)][0] is False:
            if int(tanks[int(equipment)][2]) >= int(volume):
                if str(process) in (tanks[int(equipment)][3]):
                    tanks[int(equipment)][0] = True
                    tank_name = tanks[int(equipment)][4]
                    start_time = time.time()
                    if process == 'F':
                        end_time = start_time + int(2419200)
                        proc = 'Fermentation'
                        stage2.append([tank_name,volume,beer,time.ctime(start_time),\
                        time.ctime(end_time)])
                    elif process == 'C':
                        end_time = start_time + int(1209600)
                        proc = 'Conditioning'
                        stage3.append([tank_name,volume,beer,time.ctime(start_time),\
                        time.ctime(end_time)])

                    tanks[int(equipment)][1] = time.ctime(start_time)
                    tanks[int(equipment)][5] = time.ctime(end_time)

                else:
                    return '<form action="/" method="get" >\
                            <button type="submit"> Home</button>\
                            </form>\
                            <h1>Error: Tank does not have chosen capabilities</h1>'
            else:
                return '<form action="/" method="get" >\
                        <button type="submit"> Home</button>\
                        </form>\
                        <h1>Error: Volume exceeds tank capacity</h1>'
        else:
            return '<form action="/" method="get" >\
                    <button type="submit"> Home</button>\
                    </form>\
                    <h1>Error: Equipment in use</h1>'


    """This starts processes that do not require equipment. It gets the data from
    the html document and calcultes the process times and stats, it then appends
    the data to the relevant stage"""
    if process2:
        volume2 = volume2
        start_time = time.time()
        if process2 == 'HB':
            end_time = start_time + int(7200)
            stage1.append(['N/A',volume2,beer2,time.ctime(start_time),time.ctime(end_time)])
        elif process2 == 'B':
            duration = (int(volume2))*3600
            end_time = start_time + int(duration)
            stage4.append(['N/A',volume2,beer2,time.ctime(start_time),time.ctime(end_time)])

    """This code allows the user to end events, when the process finishes, the user
    can make the equipment avaliable again by confirming that the process has
    finished. It performs validation to make sure the tasks exist and return errors.
    It also updates the table to show the user the status of the tanks"""
    if proc_canc:
        if proc_canc == 's1':
            if len(stage1) >= int(number):
                del stage1[int(number)-1]
            else:
                return '<form action="/" method="get" >\
                        <button type="submit"> Home</button>\
                        </form>\
                        <h1>Error: Process does not exist</h1>'
        elif proc_canc == 's2':
            if len(stage2) >= int(number):
                tank_nam = stage2[int(number)-1][0]
                for items in tanks:
                    if items[4] == str(tank_nam):
                        items[0] = False
                        items[1] = None
                        items[5] = None
                del stage2[int(number)-1]


        elif proc_canc == 's3':
            if len(stage3) >= int(number):
                tank_nam = stage3[int(number)-1][0]
                for items in tanks:
                    if items[4] == str(tank_nam):
                        items[0] = False
                        items[1] = None
                        items[5] = None
                del stage3[int(number)-1]

            """For the last stage of brewing, when this one is ended, the beer
            produced is automatically added to the stock. The code determines then
            bottles that are produced and the beer type, it then removes the process"""

        elif proc_canc == 's4':
            if len(stage4) >= int(number):
                beer_name = stage4[int(number)-1][2]
                vol = stage4[int(number)-1][1]
                if beer_name == 'Pilsner':
                    Pstock += int(vol)*2
                if beer_name == 'Dunkel':
                    Dstock += int(vol)*2
                if beer_name == 'Red Helles':
                    Hstock += int(vol)*2

                del stage4[int(number)-1]


            else:
                return '<form action="/" method="get" >\
                        <button type="submit"> Home</button>\
                        </form>\
                        <h1>Error: Process does not exist</h1>'


    """This code allows the user to add and remove stock. It gets the values
    sent from the html page and adjusts the stock"""
    if quantity:
        beer_type = str(beer3)
        if beer_type == 'P':
            Pstock += int(quantity)
        if beer_type == 'D':
            Dstock += int(quantity)
        if beer_type == 'H':
            Hstock += int(quantity)

    if quantity2:
        beer_type = str(beer4)
        if beer_type == 'P':
            Pstock -= int(quantity2)
        if beer_type == 'D':
            Dstock -= int(quantity2)
        if beer_type == 'H':
            Hstock -= int(quantity2)

    return render_template('home.html',A=tanks[0][0],B=tanks[1][0],C=tanks[2][0],\
        D=tanks[3][0],E=tanks[4][0],F=tanks[5][0],G=tanks[6][0],H=tanks[7][0],\
        R=tanks[8][0],\
        Atime=tanks[0][1],Btime=tanks[1][1],Ctime=tanks[2][1],Dtime=tanks[3][1],\
        Etime=tanks[4][1],Ftime=tanks[5][1],Gtime=tanks[6][1],Htime=tanks[7][1],\
        Rtime=tanks[8][1],\
        Aendtime=tanks[0][5],Bendtime=tanks[1][5],Cendtime=tanks[2][5],\
        Dendtime=tanks[3][5],Eendtime=tanks[4][5],Fendtime=tanks[5][5],\
        Gendtime=tanks[6][5],Hendtime=tanks[7][5],Rendtime=tanks[8][5],\
        stage1=stage1,stage2=stage2,stage3=stage3,stage4=stage4,Pstock=Pstock,\
        Dstock=Dstock,Hstock=Hstock)

"""The predictions page shows the predictions for each month for 2 years in the
future. It takes the data from the predict.py page and uses flask to show then
info"""

@app.route('/predictions')
def predict():
    historic,pred_y1,pred_y2 = predictor()


    return render_template('predictions.html',historic=historic,pred_y1=pred_y1\
    ,pred_y2=pred_y2)

if __name__ == '__main__':
    app.run(debug=True)
