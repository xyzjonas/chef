
runserver:
    poetry run chef serve

[working-directory: 'src/js/chef']
dev:
    npm run dev

docker-build-prod:
  docker build -t scotch3840/chef .

docker-push:
  docker push scotch3840/chef

docker: docker-build-prod
  docker push scotch3840/chef