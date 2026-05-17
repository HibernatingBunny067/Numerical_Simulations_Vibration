echo "Making python environment..."
python3 -m venv .venv
sleep(1)

echo "Starting the environment..."
source .venv/bin/activate 
sleep(1)

echo "Installing dependencies..."
pip install -r REQUIREMENTS.txt
sleep(1)

echo "Running simulation..."
python3 -m simulation.main
