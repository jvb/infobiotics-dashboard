from bbfreeze import Freezer
f = Freezer(
	'infobiotics-dasboard-1.1.0', 
	includes=(
		'_strptime',
	)
)
f.addScript('infobiotics-dashboard.py')
f() # starts the freezing process