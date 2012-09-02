from bbfreeze import Freezer

f = Freezer(
	'dist',#'infobiotics-dasboard-1.1.0', 
	includes=(
#		'_strptime',
	)
)

f.addScript('infobiotics-dashboard.py')

# not library.zip
f.use_compression = False

# freeze
f()
