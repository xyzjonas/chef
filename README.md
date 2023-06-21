# 👨‍🍳 Chef

A simple, customizable recipe management app.

<picture>
 <img alt="screenshot1" src="https://github.com/jonasbrauer/chef/assets/10963153/98b9ca93-1fe0-44c5-afff-403423f5be09" height=360>
</picture>

<picture>
 <img alt="screenshot2" src="https://github.com/jonasbrauer/chef/assets/10963153/17ee4e24-62be-4b3d-89ed-ed1644c3df2c" height=360>
</picture>

<picture>
 <img alt="screenshot3" src="https://github.com/jonasbrauer/chef/assets/10963153/2c6aea89-2220-40ed-a1d1-4b13c558314a" height=360>
</picture>

<picture>
 <img alt="screenshot4" src="https://github.com/jonasbrauer/chef/assets/10963153/fe1cf765-6475-47bc-b69c-06b21eb08d2a" height=360>
</picture>

## Installation

```shell
$ curl https://raw.githubusercontent.com/jonasbrauer/chef/master/install.sh | bash
```

or install the package yourself

```shell
$ pip install chef-recipes
```

...or run with docker:

```shell
$ docker build . -t chef
$ docker run -p 8000:8000 -v ~/.chef:/chef/data chef
```