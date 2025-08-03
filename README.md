# PYTEST
To practice Selenium Python with the webpage: https://automationexercise.com/

AI spends only 1 minute convert manual test cases to automatic scripts. 
However, the results with some errors:
1. Total 26 test cases, AI only generates 15 test cases.
2. Some scripts execute with errors, caused by incorrect webElement locator.

I have fixed above problems, but the code still needs to be improved for code reable and reusable.

# To do:
Refactor current scripts to Page Object Model pattern.




# Build the Docker image
docker build -t pytest-automation .

# Run tests in Docker
docker run --rm \
  -e SENDER_EMAIL="your_email@gmail.com" \
  -e EMAIL_PASSWORD="your_app_password" \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  pytest-automation \
  pytest uiTests/automation_exercise_test.py -v --reruns=3 --reruns-delay=2 --html=reports/report.html --self-contained-html

# Or use docker-compose
export SENDER_EMAIL="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
docker-compose up --build
