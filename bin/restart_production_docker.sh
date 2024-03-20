docker-compose -p prod_{{ your_project_name }} -f production.yml down

if [ "$1" == "build" ]; then
    docker-compose -p prod_{{ your_project_name }} -f production.yml up --build -d

    docker exec -it prod_{{ your_project_name }}_django-1 python /app/manage.py migrate
    docker exec -it prod_{{ your_project_name }}_django-1 python /app/manage.py loaddata initial_data.json
else
    docker-compose -p prod_{{ your_project_name }} -f production.yml up -d
fi
