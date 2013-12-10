#!/usr/bin/env/python

import ROOT as rt
import glob,gzip
import numpy as n


from ROOT import gStyle
from ROOT import gROOT
from ROOT import TMath 

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
openFile = "Compare_CrossSections_with_diff_Mixing.txt"
# read in the file as a list of lines
FILE = open(openFile)
lines = FILE.read().split("\n")
FILE.close()

# your data
data = []

# read the header
columnnames = lines[0].split()
#print columnnames
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
        print columns[c]
        number = columns[c]
        if c == 0:
            shorten = columns[c].split("_width")[0]
            print shorten
            number  = shorten[(len(shorten)-3):]
            print number
                    
        _data[columnnames[c]] = float(number)
    
    # add it to the data array
    data.append(_data)

print data

array = []
x    = n.zeros(7, dtype=float)
yHiggsino    = n.zeros(7, dtype=float)
yWino        = n.zeros(7, dtype=float)
yOriginal    = n.zeros(7, dtype=float)
yRelDiff     = n.zeros(7, dtype=float)
for m in range(0,7):
   
    for _data in data:
        if _data['SAMPLE']== m*100 +100:  
            array.append(_data)
            break

print "\n\n"
print array
print ""

_part = dict()

i = 0
for _part in array:
    print _part
    x[i] = _part['SAMPLE']
    yHiggsino[i] = _part['HIGGSINOLIKE']
    yWino[i]     = _part['WINOLIKE']
    yOriginal[i] = _part['ORIGINAL']
    yRelDiff[i]  = _part['WINOLIKE']/ _part['HIGGSINOLIKE']-1.
    i = i+1
    
#    xsec = n.zeros(7, dtype=float)
#    obslimit = []
#    mass = []
#    width = []
#    i=0
#    _part = dict()
#    ymin = 1000000
#    ymax = -1000000
#    for _part in array:
#        obslimit.append(float(_part['OBSLIMIT']))
#        mass.append(_part['MASS'])
#        xsec[i] = _part['XSECTION']
#        if ymin>xsec[i]:
#                ymin = xsec[i]
#        if ymax<xsec[i]:
#            ymax = xsec[i]
#        x[i] = c0*hbar/float(_part['WIDTH'])
#        if float(_part['OBSLIMIT']) == -1:
#            y[i]=1000
#        else:
#            y[i] = float(_part['OBSLIMIT'])
#        if ymin>y[i]:
#                ymin = y[i]
#        if ymax<y[i]:
#                ymax = y[i]
#        print "Width = " + str(x[i])
#        i = i+1
    
canvas = rt.TCanvas("canvas","canvas",500,500)
canvas.cd()
#canvas.SetLogx()
canvas.SetLogy()

legend = rt.TLegend(0.5,0.7,0.9,0.9)

graph  = rt.TGraph(int(7),x,yHiggsino)
graph2 = rt.TGraph(int(7),x,yWino)
graph3 = rt.TGraph(int(7),x,yOriginal)
titleName = ""
graph.SetTitle(titleName)
graph.SetMarkerStyle(20)
graph2.SetMarkerStyle(20)
graph3.SetMarkerStyle(20)
graph.GetXaxis().SetTitle("m_{#Chi^{#pm}} [GeV]")
graph.GetYaxis().SetTitle("cross-section [pb]")
xmin = TMath.MinElement(graph.GetN(),graph.GetX())
xmax = TMath.MaxElement(graph.GetN(),graph.GetX())
ymin = TMath.MinElement(graph.GetN(),graph.GetY())
ymax = TMath.MaxElement(graph.GetN(),graph.GetY())

if TMath.MinElement(graph2.GetN(),graph.GetX())<xmin:
    xmin = TMath.MinElement(graph2.GetN(),graph.GetX())
if TMath.MaxElement(graph2.GetN(),graph.GetX())>xmax:
    xmax = TMath.MaxElement(graph2.GetN(),graph.GetX())
if TMath.MinElement(graph2.GetN(),graph.GetX())<ymin:
    ymin = TMath.MinElement(graph2.GetN(),graph.GetY())
if TMath.MaxElement(graph2.GetN(),graph.GetX())>ymax:
    ymax = TMath.MaxElement(graph2.GetN(),graph.GetY())

graph.SetMinimum(ymin/10)
graph.SetMaximum(ymax*10)
graph.GetXaxis().SetLimits(xmin-100,xmax+100)
graph.Draw("AP")
canvas.Update()

graph2.SetMarkerColor(2)
graph3.SetMarkerColor(3)
#graph2.SetMarkerSize()
graph2.SetLineColor(2)
graph2.SetLineWidth(2)
graph2.Draw("sameP")
graph3.Draw("sameP")

legend.AddEntry(graph, "Higgsino-like #Chi^{#pm}","p")
legend.AddEntry(graph2,"Wino-like #Chi^{#pm}","p")
legend.AddEntry(graph3,"Produced Samples","p")

legend.SetTextFont(132)
legend.SetTextSize(0.042)
legend.Draw("same")

info = rt.TLatex();
info.SetNDC();
info.SetTextSize(0.05);
#info.DrawLatex(0.60, 0.60,type);

pdfName = "CrossSection.pdf"
canvas.SaveAs(pdfName)
print ""

# Next Plot

canvas1 = rt.TCanvas("canvas","canvas",500,500)
canvas1.cd()
graphRelDiff  = rt.TGraph(int(7),x,yRelDiff)
graphRelDiff.SetMarkerStyle(20)
graphRelDiff.SetTitle("Wino-Like/Higgsino-Like")
graphRelDiff.Draw("AP")
pdfName = "CrossSection_RelDiff.pdf"
canvas1.SaveAs(pdfName)


