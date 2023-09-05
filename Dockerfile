FROM python:3.10

ADD meal_planner/ .

CMD ["python3", "./main.py"]
