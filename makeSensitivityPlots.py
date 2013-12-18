#!/usr/bin/env/python

import ROOT as rt

from ROOT import gStyle
from ROOT import gROOT
from ROOT import TMath
from ROOT import TGraphAsymmErrors

import glob,gzip
import numpy as n

import sys
##############################################################################################################
gROOT.SetStyle("Plain");
gStyle.SetLegendFillColor(0);
gStyle.SetTitleFont(42,"xyz");
gStyle.SetLabelFont(42,"xyz");
gStyle.SetCanvasDefH(600);
gStyle.SetCanvasDefW(600);
gStyle.SetPadBottomMargin(0.15);
gStyle.SetPadTopMargin(0.10);
gStyle.SetPadLeftMargin(0.15);
gStyle.SetTextSize(0.042);
gStyle.SetTitleSize(0.05,"X"); 
gStyle.SetTitleSize(0.05,"Y"); 
gStyle.SetLabelSize(0.04,"X");
gStyle.SetLabelSize(0.04,"Y");
gStyle.SetTitleOffset(1.3,"X");
gStyle.SetTitleOffset(1.3,"Y");
gStyle.SetHistLineWidth(1);
gStyle.SetMarkerStyle(20);
gStyle.SetOptStat("");
gStyle.SetTextFont(132);
gStyle.SetFillColor(0);
gStyle.SetTitleSize(0.06,""); 
gROOT.ForceStyle(); 
##############################################################################################################
# speed of light [m/s]
c0 = 2.9979*10**(8)
# hbar [GeV/s]
hbar = 6.5821*10**(-25)

type = "Type2"
##############################################################################################################
##############################################################################################################

### Read limit file ########################################################################################
openFile = "sourceFiles/MapTable_" + str(type) + "_SYS.txt"
# read in the file as a list of lines
FILE = open(openFile)
lines = FILE.read().split("\n")
FILE.close()
# your data
data = []
widths = list()

# read the header
columnnames = lines[0].split()
NumberOfLines = len(lines)-1
# loop over the lines
for l in range(1,len(lines)):
    line = lines[l]
    # split the line
    columns = line.split()
    # skip empty lines
    if len(columns) == 0:
        continue
    # check that you have as many columns as columnnames
    if not len(columns) == len(columnnames):
        print "ERROR: number of columns in line{0} != number of columns in header line"
        sys.exit()
 
    # fill a dictionary:
    _data = dict()
    for c in range(0,len(columns)):
        _data[columnnames[c]] = float(columns[c])
    
    # add it to the data array
    data.append(_data)


for _data in data[0:NumberOfLines/7]:
    widths.append(_data["WIDTH"])

print widths
print ""
### Read limit file ########################################################################################
openFile = "sourceFiles/Compare_CrossSections_with_diff_Mixing.txt"
# read in the file as a list of lines
FILE = open(openFile)
lines = FILE.read().split("\n")
FILE.close()
# your data
dataXsec = []

# read the header
columnnames = lines[0].split()
# loop over the lines
for l in range(1,len(lines)):
    line = lines[l]
    # split the line
    columns = line.split()
    # skip empty lines
    if len(columns) == 0:
        continue
    # check that you have as many columns as columnnames
    if not len(columns) == len(columnnames):
        print "ERROR: number of columns in line{0} != number of columns in header line"
        sys.exit()
 
    # fill a dictionary:
    _data = dict()
    for c in range(0,len(columns)):
        number = columns[c]
        if c == 0:
            shorten = columns[c].split("_width")[0]
            number  = shorten[(len(shorten)-3):]
                    
        _data[columnnames[c]] = float(number)
    
    # add it to the data array
    dataXsec.append(_data)

print dataXsec


### Read the HiggsinoWinoCrossSection.txt file ########################################################################################
openFile = "sourceFiles/HiggsinoWinoCrossSection.txt"

# read in the file as a list of lines
FILE = open(openFile)
lines = FILE.read().split("\n")
FILE.close()
# your data
Xsec = []

# read the header
columnnames = lines[0].split()
# loop over the lines
for l in range(1,len(lines)):
    line = lines[l]
    # split the line
    columns = line.split()
    # skip empty lines
    if len(columns) == 0:
        continue
    # check that you have as many columns as columnnames
    if not len(columns) == len(columnnames):
        print "ERROR: number of columns in line{0} != number of columns in header line"
        sys.exit()
 
    # fill a dictionary:
    _data = dict()
    for c in range(0,len(columns)):
        number = columns[c]
        #if c == 0:
        #    shorten = columns[c].split("_width")[0]
        #    number  = shorten[(len(shorten)-3):]
                    
        _data[columnnames[c]] = float(number)
    
    # add it to the data array
    Xsec.append(_data)

print Xsec

### Fill graphs ########################################################################################
for m in range(0,7):
    array = [] 
    for _data in data:
        if _data['MASS']== m*100 +100:  
            array.append(_data)

            
    print "Number of Lines:" + str(NumberOfLines)
            
    x            = n.zeros(NumberOfLines/7, dtype=float)
    xUp          = n.zeros(NumberOfLines/7, dtype=float)
    xDown        = n.zeros(NumberOfLines/7, dtype=float)
    y            = n.zeros(NumberOfLines/7, dtype=float)
    yExp         = n.zeros(NumberOfLines/7, dtype=float)
    yExpUp       = n.zeros(NumberOfLines/7, dtype=float)
    yExpDown     = n.zeros(NumberOfLines/7, dtype=float)
    xsec         = n.zeros(NumberOfLines/7, dtype=float)
    xsecE        = n.zeros(NumberOfLines/7, dtype=float)
    xsecWino     = n.zeros(NumberOfLines/7, dtype=float)
    xsecHiggsino = n.zeros(NumberOfLines/7, dtype=float)

    higgsinoMean = 0
    winoMean     = 0
    i=0
    for _dataXsec in dataXsec:
        if _dataXsec['SAMPLE'] == m*100 +100:
            higgsinoMean = higgsinoMean + _dataXsec["HIGGSINOLIKE"]
            winoMean = winoMean + _dataXsec["WINOLIKE"]
            i= i+1

    higgsinoMean = (higgsinoMean/i)*10**9
    winoMean     = (winoMean/i)*10**9

    print "xsec Higgsino = " + str(higgsinoMean)
    
    obslimit     = []
    explimit     = []
    explimitUp   = []
    explimitDown = []
    mass         = []
    width        = []
    i=0
    _part = dict()
    ymin = 1000000
    ymax = -1000000
    for _part in array:
        obslimit.append(float(_part['OBSLIMIT']))
        explimit.append(float(_part['EXPLIMIT']))
        explimitUp.append(float(_part['EXPLIMITUP']))
        explimitDown.append(float(_part['EXPLIMITDOWN']))
        mass.append(_part['MASS'])
        xsec[i] = _part['XSECTION']
        xsecWino[i] = winoMean
        xsecHiggsino[i] = higgsinoMean
        if ymin>xsec[i]:
                ymin = xsec[i]
        if ymax<xsec[i]:
            ymax = xsec[i]
        x[i] = c0*hbar/float(_part['WIDTH'])
        xUp[i] = 0.0
        xDown[i] = 0.0
        if float(_part['OBSLIMIT']) == -1:
            y[i]=1000
        else:
            y[i] = float(_part['OBSLIMIT'])
        if float(_part['EXPLIMIT']) == -1:
            yExp[i]=1000
        else:
            yExp[i] = float(_part['EXPLIMIT'])
        if float(_part['EXPLIMITUP']) == -1:
            yExpUp[i]=0
        else:
            yExpUp[i] = float(_part['EXPLIMITUP']) - float(_part['EXPLIMIT'])
        if float(_part['EXPLIMITDOWN']) == -1:
            yExpDown[i]=0
        else:
            yExpDown[i] = float(_part['EXPLIMIT']) - float(_part['EXPLIMITDOWN'])
        if ymin>y[i]:
                ymin = y[i]
        if ymax<y[i]:
                ymax = y[i]
        print "Width = " + str(x[i])
        print "obs. limit = " + str(y[i])
        print "exp. limit = " + str(yExp[i])
        i = i+1
        
    
    canvas = rt.TCanvas("canvas","canvas",500,500)
    canvas.cd()
    canvas.SetLogx()
    canvas.SetLogy()

    legend = rt.TLegend(0.3,0.7,0.9,0.9)
    
    graphObs  = rt.TGraph(int(NumberOfLines/7),x,y)
    graphExp  = rt.TGraphAsymmErrors(int(NumberOfLines/7),x,yExp,xUp,xDown,yExpUp,yExpDown)
    graph2 = rt.TGraph(int(NumberOfLines/7),x,xsecWino)
    graph3 = rt.TGraph(int(NumberOfLines/7),x,xsecHiggsino)
    titleName = "m_{#Chi^{#pm}} = " + str(m*100 +100) +  " GeV"
    graphObs.SetTitle(titleName)
    graphExp.SetTitle(titleName)
    graphObs.SetMarkerStyle(20)
    graphExp.SetMarkerStyle(20)
    graph2.SetMarkerStyle(20)
    graphObs.GetXaxis().SetTitle("c#tau_{Chi^{#pm}} [m]")
    graphObs.GetYaxis().SetTitle("cross-section [pb]")
    graphExp.GetXaxis().SetTitle("c#tau_{Chi^{#pm}} [m]")
    graphExp.GetYaxis().SetTitle("cross-section [pb]")
    xmin = TMath.MinElement(graphObs.GetN(),graphObs.GetX())
    xmax = TMath.MaxElement(graphObs.GetN(),graphObs.GetX())
    #ymin = TMath.MinElement(graphObs.GetN(),graphObs.GetY())
    #ymax = TMath.MaxElement(graphObs.GetN(),graphObs.GetY())

    if TMath.MinElement(graph2.GetN(),graphObs.GetX())<xmin:
        xmin = TMath.MinElement(graph2.GetN(),graphObs.GetX())
    if TMath.MaxElement(graph2.GetN(),graphObs.GetX())>xmax:
        xmax = TMath.MaxElement(graph2.GetN(),graphObs.GetX())
    #if TMath.MinElement(graph2.GetN(),graphObs.GetX())<ymin:
    #    ymin = TMath.MinElement(graph2.GetN(),graphObs.GetY())
    #if TMath.MaxElement(graph2.GetN(),graphObs.GetX())>ymax:
    #    ymax = TMath.MaxElement(graph2.GetN(),graphObs.GetY())
    
    graphObs.SetMinimum(ymin/100)
    graphObs.SetMaximum(ymax*1000)
    graphObs.GetXaxis().SetLimits(xmin/10,xmax*10)
    graphExp.SetMinimum(ymin/100)
    graphExp.SetMaximum(ymax*1000)
    graphExp.GetXaxis().SetLimits(xmin/10,xmax*10)
    graphObs.Draw("AP")
    canvas.Update()
    
    graph2.SetMarkerColor(2)
    #graph2.SetMarkerSize()
    graph2.SetLineColor(2)
    graph2.SetLineWidth(2)
    graph2.Draw("sameL")

    graph3.SetLineColor(3)
    graph3.SetLineWidth(2)
    graph3.Draw("sameL")

    legend.AddEntry(graphObs, "exp. limit","p")
    legend.AddEntry(graph2, "#sigma^{theo} with wino-like #Chi^{#pm}_{1}","l")
    legend.AddEntry(graph3, "#sigma^{theo} with higgsino-like #Chi^{#pm}_{1}","l")

    legend.SetTextFont(132)
    legend.SetTextSize(0.042)
    legend.Draw("same")

    info = rt.TLatex();
    info.SetNDC();
    info.SetTextSize(0.05);
    info.DrawLatex(0.60, 0.60,type);
    
    pdfName = "plots/HSCPSensitivity_m" + str(m*100 +100) + "_" + str(type) + ".pdf"
    canvas.SaveAs(pdfName)
    print ""


### Fill graphs for Mass plots ########################################################################################

for m in range(0,NumberOfLines/7):

    array = [] 
    for _data in data:
        if _data['INDEX']== m:  
            array.append(_data)
            print _data

    print ""
    print array        
    print ""

    xMass            = n.zeros(7, dtype=float)
    xUpMass          = n.zeros(7, dtype=float)
    xDownMass        = n.zeros(7, dtype=float)
    yMass            = n.zeros(7, dtype=float)
    yExpMass         = n.zeros(7, dtype=float)
    yExpUpMass       = n.zeros(7, dtype=float)
    yExpDownMass     = n.zeros(7, dtype=float)
    xsecMass         = n.zeros(7, dtype=float)
    xsecEMass        = n.zeros(7, dtype=float)
    xsecWinoMass     = n.zeros(7, dtype=float)
    xsecHiggsinoMass = n.zeros(7, dtype=float)

    obslimit     = []
    explimit     = []
    explimitUp   = []
    explimitDown = []
    mass         = []
    width        = []
    i=0
    _part = dict()
    ymin = 1000000
    ymax = -1000000
    

    for _part in array:

        width = c0*hbar/float(_part['WIDTH'])

        for _Xsec in Xsec:
            if _Xsec['MASS'] == _part['MASS']:
                xsecHiggsinoMass[i] = _Xsec["HIGGSINOLIKE"]
                xsecWinoMass[i]     = _Xsec["WINOLIKE"]
                print "xsecHiggsinoMass = " + str(xsecHiggsinoMass[i])
                print "xsecWinoMass = " + str(xsecWinoMass[i])

 
        obslimit.append(float(_part['OBSLIMIT']))
        explimit.append(float(_part['EXPLIMIT']))
        explimitUp.append(float(_part['EXPLIMITUP']))
        explimitDown.append(float(_part['EXPLIMITDOWN']))
        mass.append(_part['MASS'])
        
        xsecMass[i] = _part['XSECTION']
        if ymin>xsecMass[i]:
                ymin = xsecMass[i]
        if ymax<xsecMass[i]:
            ymax = xsecMass[i]
        xMass[i] = float(_part['MASS'])
        xUpMass[i] = 0.0
        xDownMass[i] = 0.0
        if float(_part['OBSLIMIT']) == -1:
            yMass[i]=1000
        else:
            yMass[i] = float(_part['OBSLIMIT'])
        if float(_part['EXPLIMIT']) == -1:
            yExpMass[i]=1000
        else:
            yExp[i] = float(_part['EXPLIMIT'])
        if float(_part['EXPLIMITUP']) == -1:
            yExpUpMass[i]=0
        else:
            yExpUpMass[i] = float(_part['EXPLIMITUP']) - float(_part['EXPLIMIT'])
        if float(_part['EXPLIMITDOWN']) == -1:
            yExpDownMass[i]=0
        else:
            yExpDownMass[i] = float(_part['EXPLIMIT']) - float(_part['EXPLIMITDOWN'])
        if ymin>yMass[i]:
                ymin = yMass[i]
        if ymax<yMass[i]:
                ymax = yMass[i]
        print "Width = " + str(xMass[i])
        print "obs. limit = " + str(yMass[i])
        print "exp. limit = " + str(yExpMass[i])
        i = i+1
        
    
    canvasMass = rt.TCanvas("canvas","canvas",500,500)
    canvasMass.cd()
    #canvasMass.SetLogx()
    canvasMass.SetLogy()

    legendMass = rt.TLegend(0.3,0.7,0.9,0.9)
    
    graphObsMass  = rt.TGraph(int(7),xMass,yMass)
    graphExpMass  = rt.TGraphAsymmErrors(int(7),xMass,yExpMass,xUpMass,xDownMass,yExpUpMass,yExpDownMass)
    graph2Mass = rt.TGraph(int(7),xMass,xsecWinoMass)
    graph3Mass = rt.TGraph(int(7),xMass,xsecHiggsinoMass)
    titleName = "c#tau_{Chi^{#pm}} = " + str('%0.1f' %width) +  " m"
    #titleName = str('%0.1E' %widths)
    graphObsMass.SetTitle(titleName)
    graphExpMass.SetTitle(titleName)
    graphObsMass.SetMarkerStyle(20)
    graphExpMass.SetMarkerStyle(20)
    graph2Mass.SetMarkerStyle(20)
    graphObsMass.GetXaxis().SetTitle("m_{Chi^{#pm}} [GeV]")
    graphObsMass.GetYaxis().SetTitle("cross-section [pb]")
    graphExpMass.GetXaxis().SetTitle("m_{Chi^{#pm}} [GeV]")
    graphExpMass.GetYaxis().SetTitle("cross-section [pb]")
    xmin = TMath.MinElement(graphObsMass.GetN(),graphObsMass.GetX())
    xmax = TMath.MaxElement(graphObsMass.GetN(),graphObsMass.GetX())
    #ymin = TMath.MinElement(graphObs.GetN(),graphObs.GetY())
    #ymax = TMath.MaxElement(graphObs.GetN(),graphObs.GetY())

    if TMath.MinElement(graph2Mass.GetN(),graphObsMass.GetX())<xmin:
        xmin = TMath.MinElement(graph2Mass.GetN(),graphObsMass.GetX())
    if TMath.MaxElement(graph2Mass.GetN(),graphObsMass.GetX())>xmax:
        xmax = TMath.MaxElement(graph2Mass.GetN(),graphObsMass.GetX())
    #if TMath.MinElement(graph2.GetN(),graphObs.GetX())<ymin:
    #    ymin = TMath.MinElement(graph2.GetN(),graphObs.GetY())
    #if TMath.MaxElement(graph2.GetN(),graphObs.GetX())>ymax:
    #    ymax = TMath.MaxElement(graph2.GetN(),graphObs.GetY())
    
    graphObsMass.SetMinimum(ymin/100)
    graphObsMass.SetMaximum(ymax*1000)
    graphObsMass.GetXaxis().SetLimits(0,800)
    graphExpMass.SetMinimum(ymin/100)
    graphExpMass.SetMaximum(ymax*1000)
    graphExpMass.GetXaxis().SetLimits(0,800)
    graphObsMass.Draw("AP")
    canvasMass.Update()
    
    graph2Mass.SetMarkerColor(2)
    #graph2.SetMarkerSize()
    graph2Mass.SetLineColor(2)
    graph2Mass.SetLineWidth(2)
    graph2Mass.Draw("sameL")

    graph3Mass.SetLineColor(3)
    graph3Mass.SetLineWidth(2)
    graph3Mass.Draw("sameL")

    legendMass.AddEntry(graphObs, "exp. limit","p")
    legendMass.AddEntry(graph2, "#sigma^{theo} with wino-like #Chi^{#pm}_{1}","l")
    legendMass.AddEntry(graph3, "#sigma^{theo} with higgsino-like #Chi^{#pm}_{1}","l")

    legendMass.SetTextFont(132)
    legendMass.SetTextSize(0.042)
    legendMass.Draw("same")

    infoMass = rt.TLatex();
    infoMass.SetNDC();
    infoMass.SetTextSize(0.05);
    infoMass.DrawLatex(0.60, 0.60,type);
    
    pdfName = "plots/HSCPSensitivity_width" + str(m) + "_" + str(type) + ".pdf"
    canvasMass.SaveAs(pdfName)
    print ""


