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
hbar = 6.5821*10**(-24)

type = "Type0"

### Read limit file ########################################################################################
openFile = "sourceFiles/MapTable_" + str(type) + ".txt"
# read in the file as a list of lines
FILE = open(openFile)
lines = FILE.read().split("\n")
FILE.close()
# your data
data = []

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
        _data[columnnames[c]] = float(columns[c])
    
    # add it to the data array
    data.append(_data)

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
### Fill graphs ########################################################################################
for m in range(0,7):
    array = [] 
    for _data in data:
        if _data['MASS']== m*100 +100:  
            array.append(_data)

            
    x        = n.zeros(7, dtype=float)
    xUp     = n.zeros(7, dtype=float)
    xDown   = n.zeros(7, dtype=float)
    y        = n.zeros(7, dtype=float)
    yExp     = n.zeros(7, dtype=float)
    yExpUp   = n.zeros(7, dtype=float)
    yExpDown = n.zeros(7, dtype=float)
    xsec = n.zeros(7, dtype=float)
    xsecE = n.zeros(7, dtype=float)
    xsecWino     = n.zeros(7, dtype=float)
    xsecHiggsino = n.zeros(7, dtype=float)

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
    
    graph  = rt.TGraph(int(7),x,y)
    graphExp  = rt.TGraphAsymmErrors(int(7),x,yExp,xUp,xDown,yExpUp,yExpDown)
    graph2 = rt.TGraph(int(7),x,xsecWino)
    graph3 = rt.TGraph(int(7),x,xsecHiggsino)
    titleName = "m_{#Chi^{#pm}} = " + str(m*100 +100) +  " GeV"
    graph.SetTitle(titleName)
    graphExp.SetTitle(titleName)
    graph.SetMarkerStyle(20)
    graphExp.SetMarkerStyle(20)
    graph2.SetMarkerStyle(20)
    graph.GetXaxis().SetTitle("c#tau_{Chi^{#pm}} [m]")
    graph.GetYaxis().SetTitle("cross-section [pb]")
    graphExp.GetXaxis().SetTitle("c#tau_{Chi^{#pm}} [m]")
    graphExp.GetYaxis().SetTitle("cross-section [pb]")
    xmin = TMath.MinElement(graph.GetN(),graph.GetX())
    xmax = TMath.MaxElement(graph.GetN(),graph.GetX())
    #ymin = TMath.MinElement(graph.GetN(),graph.GetY())
    #ymax = TMath.MaxElement(graph.GetN(),graph.GetY())

    if TMath.MinElement(graph2.GetN(),graph.GetX())<xmin:
        xmin = TMath.MinElement(graph2.GetN(),graph.GetX())
    if TMath.MaxElement(graph2.GetN(),graph.GetX())>xmax:
        xmax = TMath.MaxElement(graph2.GetN(),graph.GetX())
    #if TMath.MinElement(graph2.GetN(),graph.GetX())<ymin:
    #    ymin = TMath.MinElement(graph2.GetN(),graph.GetY())
    #if TMath.MaxElement(graph2.GetN(),graph.GetX())>ymax:
    #    ymax = TMath.MaxElement(graph2.GetN(),graph.GetY())
    
    graph.SetMinimum(ymin/100)
    graph.SetMaximum(ymax*1000)
    graph.GetXaxis().SetLimits(xmin/10,xmax*10)
    graphExp.SetMinimum(ymin/100)
    graphExp.SetMaximum(ymax*1000)
    graphExp.GetXaxis().SetLimits(xmin/10,xmax*10)
    graphExp.Draw("AP")
    canvas.Update()
    
    graph2.SetMarkerColor(2)
    #graph2.SetMarkerSize()
    graph2.SetLineColor(2)
    graph2.SetLineWidth(2)
    graph2.Draw("sameL")

    graph3.SetLineColor(3)
    graph3.SetLineWidth(2)
    graph3.Draw("sameL")

    legend.AddEntry(graph, "exp. limit","p")
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


