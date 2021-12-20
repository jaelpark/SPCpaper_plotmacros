import numpy as np
import ROOT

import scipy
from scipy import interpolate

import sys
sys.path.append("JPyPlotRatio");


import JPyPlotRatio

f = ROOT.TFile("data/Output_ALICE.root","read");
fmodel = ROOT.TFile("data/Output_TrentoVISHNU.root","read");

obsPanel = [0,3,2,1];
obsTypeStr  = ["4Psi4_n4Psi2","6Psi3_n6Psi2","6Psi6_n6Psi2","6Psi6_n6Psi3"
		];
plabel     = ["$\\langle cos[4(\\Psi_{4}-\\Psi_{2})]\\rangle$",
	      "$\\langle cos[6(\\Psi_{2}-\\Psi_{3})]\\rangle$",
	      "$\\langle cos[6(\\Psi_{6}-\\Psi_{2})]\\rangle$",
	      "$\\langle cos[6(\\Psi_{6}-\\Psi_{3})]\\rangle$" # 2 har
	      ];
dataTypeStr = ["ALICE","{T\\raisebox{-.5ex}{R}ENTo} (cumulants)","{T\\raisebox{-.5ex}{R}ENTo} (eccentricities)","{T\\raisebox{-.5ex}{R}ENTo} + VISH2+1 + UrQMD"];
dataTypeInRoot = ["ALICE","_Trento_Cumulants","_Trento_Ecc","_TrentoVISHNU_FinalState"];
dataTypePlotParams = [
        {'plotType':'data','color':'black','fmt':'s','fillstyle':'none','markersize':5.5},
        {'plotType':'data','color':'#0051a2','fmt':'s','markersize':4.0},
        {'plotType':'data','color':'#ff0000','fmt':'o','fillstyle':'none','markersize':5.5},
        {'plotType':'data','color':'#ff9900','fmt':'o','markersize':4.0}
];
modelTypePlotParams = [
	{'plotType':'theory','color':'black','alpha':0.5,'linestyle':'solid'},
	{'plotType':'theory','color':'#0051a2','alpha':0.5,'linestyle':'dotted'},
	{'plotType':'theory','color':'#ff0000','alpha':0.5,'linestyle':'dashed'},
	{'plotType':'theory','color':'#ff9900','alpha':0.5,'linestyle':'dashdot'}
];
def RemovePoints(arrays, pointIndices):
	return tuple([np.delete(a,pointIndices) for a in arrays]);

# define panel/xaxis limits/titles
ny = 2;
nx = 2;
xlimits = [(0.,53.)];
ylimits = [(-0.5,0.55),(-0.5,0.55),(-0.5,0.55),(-0.5,0.55)];

xtitle = ["Centrality percentile"];
ytitle = ["Correlations","Correlations"];
ytitleRight = ["Correlations"];
# Following two must be added
toptitle = "PbPb $\\sqrt{s_{NN}}$ = 2.76 TeV"; # need to add on the top
dataDetail = "$0.2 < p_\\mathrm{T} < 5.0\\,\\mathrm{GeV}/c$\n$|\\eta| < 0.8$";

plot = JPyPlotRatio.JPyPlotRatio(panels=(ny,nx),panelsize=(5,5),disableRatio=[0,1],
#	rowBounds=ylimits, #only one row, add the shared ylims
	colBounds={0:xlimits[0],1:xlimits[0]}, #two columns, set xlimit for both of them
	ratioBounds={0:(-1,3),1:(-1,3)},
	panelPrivateScale=[1,3],
	#panelLabel={i:label for i,label in enumerate(plabel)},
	panelLabelLoc=(0.07,0.86),panelLabelSize=11,
	panelLabel=plabel,
	#panelScaling={3:5},
	panelLabelAlign="left",
legendPanel=0,legendLoc=(0.70,0.26),legendSize=9,ylabel={0:ytitle[0],1:ytitle[1]});
plot.GetPlot().text(0.5,0.05,xtitle[0],size=plot.axisLabelSize,horizontalalignment="center");
plot.GetAxes(1).yaxis.tick_right();
plot.GetAxes(3).yaxis.tick_right();

plot.EnableLatex(True);

#plot.EnableLatex(True);
obsN = len(obsTypeStr);

#scale1 = {4:10,5:10};

plot.GetAxes(0).plot([0,50],[0,0],linestyle=":",color="gray");
plot.GetAxes(1).plot([0,50],[0,0],linestyle=":",color="gray");
plot.GetAxes(2).plot([0,50],[0,0],linestyle=":",color="gray");
plot.GetAxes(3).plot([0,50],[0,0],linestyle=":",color="gray");


for i in range(0,obsN):
	gr = f.Get("{:s}{:s}".format(obsTypeStr[i],"_Stat"));
	plot1 = plot.AddTGraph(obsPanel[i],gr,**dataTypePlotParams[i]);
	if(i==0):
		plot1 = plot.AddTGraph(obsPanel[i],gr,**dataTypePlotParams[i],label=dataTypeStr[0]);
	# systematics
	grsyst = f.Get("{:s}{:s}".format(obsTypeStr[i],"_Syst"));
	_,_,_,yerrsyst = JPyPlotRatio.TGraphErrorsToNumpy(grsyst);
	plot.AddSyst(plot1,yerrsyst);
	# model
	for j in range(0,3):
		grmodel = fmodel.Get("{:s}{:s}".format(obsTypeStr[i],dataTypeInRoot[j+1]));
		#grmodel.Print();
		plotModel = plot.AddTGraph(obsPanel[i],grmodel,**modelTypePlotParams[j],label=dataTypeStr[j+1]);

f.Close();

#plot.GetPlot().text(0.16,0.31,"ALICE",fontsize=9);
plot.GetPlot().text(0.34,0.75,toptitle,fontsize=9);
plot.GetPlot().text(0.34,0.70,dataDetail,fontsize=9);
#plot.GetAxes(3).text(0.1,0.1,dataDetail,fontsize=9);

plot.Plot();

#plot.GetRatioAxes(3).remove();

plot.Save("figs/Fig2_TwoHar_models.pdf");
plot.Show();

