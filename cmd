python3 snake.py --mode play --ui on --rate step --modelname finaltests.npy --sessions 10
python3 snake.py --mode play --ui off --rate step --modelname finaltests.npy --sessions 10
python3 snake.py --mode train --ui on --rate step --modelname finaltests.npy --sessions 10
python3 snake.py --mode train --ui off --rate step --modelname finaltests.npy --sessions 10

python3 snake.py --mode play --ui on --rate human --modelname finaltests.npy --sessions 10
python3 snake.py --mode play --ui off --rate human --modelname finaltests.npy --sessions 10
python3 snake.py --mode train --ui on --rate human --modelname finaltests.npy --sessions 10
python3 snake.py --mode train --ui off --rate human --modelname finaltests.npy --sessions 10

python3 snake.py --mode play --ui on --rate cpu --modelname finaltests.npy --sessions 10
python3 snake.py --mode play --ui off --rate cpu --modelname finaltests.npy --sessions 10
python3 snake.py --mode train --ui on --rate cpu --modelname finaltests.npy --sessions 10
python3 snake.py --mode train --ui off --rate cpu --modelname finaltests.npy --sessions 10