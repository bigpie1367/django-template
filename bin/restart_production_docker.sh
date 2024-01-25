docker-compose -p prod_{{ your_project_name }} down
docker-compose -p prod_{{ your_project_name }} -f production.yml up --build -d