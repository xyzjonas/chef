
runserver:
    poetry run chef serve

dev:
  poetry run chef serve

[working-directory: 'src/js/chef']
ui:
    npm run dev

docker-build-prod:
  docker build -t scotch3840/chef .

docker-push:
  docker push scotch3840/chef

docker: docker-build-prod
  docker push scotch3840/chef

build:
    cd src/js/chef && npm run build
    poetry build

build-and-publish:
    cd src/js/chef && npm run build
    poetry build
    poetry publish

migrate:
  poetry run chef migrate-db