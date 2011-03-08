workon ets-trunk--no-site-packages
cd dashboard
export PYTHON=`pwd`
python -c "from infobiotics.mcss.api import McssParams; params = McssParams(); print params.directory"

