import classes_only as co
import pickle as pkl
import os

cur_dir = os.getcwd()
pickle_name = cur_dir + '/' + 'fitsforgui.pkl'
f = open(pickle_name,'rb')
original_plate = pkl.load(f)
plate = original_plate
#gridplot=co.Grid_plot()
n = 0
while n < 96:
	def add(buttonpressevent):
		global n
		n+=1
	def substract(buttonpressevent):
		global n
		n-=1
	name_key = plate.well_names[n]
	print(name_key)
	obj = plate.plate_dict[name_key]
	plot = co.Simple_dog(obj)
	plot.bnext.on_clicked(add)
	plot.bprev.on_clicked(substract)
	plot.show()
	print('Name %s Well Center(x,y,r) %s,%s,%s \nDrop center %s,%s,%s \nTarget center %s,%s,%s' %(obj.name, obj.wcx, obj.wcy,obj.wr,obj.dcx,obj.dcy,obj.dr,obj.tx,obj.ty,obj.tr ))

'''
for well_string in plate.well_names:
	obj = plate.plate_dict[well_string]
	plot=co.Simple_dog(obj)
	plot.show()
'''
#griplot= co.Grid_plot()
