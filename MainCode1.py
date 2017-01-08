from datetime import datetime
dutyCycle=23400# basically it is In second
tolerance=20# Defining some tolreance
increasing_fac=.9#Increasing factor to increase flow rate
decreasing_fac=.5#Decreasing factor to decrease the flow reat

def NDFRST(FlowData,Time,dutyCycle,tolerance,incFac,deFac):#NDFR=Next day flow rate and Starting time
    onTime=[]
    offTime=[]
    ave_flowRate=sum(FlowData)/len(FlowData)#Caculating average flow rate
    error=tolerance+300# initially error is being defined greater than tolerance
    outPutTime=0#Initialyzing total calculated runnung time
    while error>=tolerance:# if error less than tolerance then exit the loop
        for i in range(1,len(FlowData)-1):# this loop for geting total running time of motor at perticular flow rate
            preDataCheck=(FlowData[i-1]<=ave_flowRate)#Taking boolean decision whether previous flow rate is less than given flow rate
            presDataCheck=(FlowData[i]<=ave_flowRate)#Taking boolean decision whether present flow rate is less than given flow rate
            if preDataCheck != presDataCheck:#If above both decisions are not equal then note down the corresponding time
                if preDataCheck==1:#While going uphill 
                    preTime=Time[i]
                    onTime=onTime+[preTime]
                else:
                    presTime=Time[i]#While going downhill 
                    outPutTime=outPutTime+presTime-preTime
                    offTime=offTime+[presTime]
        Error=outPutTime-dutyCycle#Error between actual dutycycle and calculated running time
        error=abs(Error)#
        if error>=tolerance:
            outPutTime=0#Setting back to zerro for next iteration
            onTime=[]
            offTime=[]
            if Error>0:
                ave_flowRate=ave_flowRate+incFac
            else:
                ave_flowRate=ave_flowRate-deFac
    return [ave_flowRate,outPutTime,onTime,offTime]
                


dataFile=open('C:\Users\ADITYA\Desktop\FlowD.txt','r')
Time=[]
FlowData=[]
for line in dataFile:
    #print line.find(":")
    pos_semi1=line.find(":")# Position of first semicolon
    pos_semi2=line.find(":",pos_semi1+1)# Position of 2nd semicolon
    pos_semi3=line.find(":",pos_semi2+1)# Position of 3rd semicolon
    Hour=int(float(line[0:pos_semi1]))# Extracting the hours value
    minute=int(float(line[pos_semi1+1:pos_semi2]))# Extracting the minutes value
    Second=int(float(line[pos_semi2+1:pos_semi3]))# Extracting the Second value
    FlowRate=float(line[pos_semi3+1:])# Extracting the FlowRate value
    Time=Time+[Hour*3600+minute*60+Second]# Array of Time
    FlowData=FlowData+[FlowRate]# Array of FlowRate Data
Start_t=datetime.now()
aa= NDFRST(FlowData,Time,dutyCycle,tolerance,increasing_fac,decreasing_fac)
Thresold=aa[0]
print "Thresold Flow Rate=",Thresold
for i in range(0,2):
    print "Motor is Switched on at time = ",int((aa[2][i])/3600),":",int(((aa[2][i])%3600)/60)
    print "Motor is Switched off at time = ",int((aa[3][i])/3600),":",int(((aa[2][i])%3600)/60)
    

#print datetime.now()-Start_t
