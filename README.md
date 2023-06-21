# 👨‍🍳 Chef

A simple, customizable recipe management app.

<picture>
 <img alt="screenshot1" src="https://github.com/jonasbrauer/chef/assets/10963153/7caf01e0-c1f6-487b-9b09-2483cf938161" height=360>
</picture>

<picture>
 <img alt="screenshot2" src="https://github.com/jonasbrauer/chef/assets/10963153/067c5953-79cf-4be5-a2ca-89a293d3db90" height=360>
</picture>

<picture>
 <img alt="screenshot3" src="https://github.com/jonasbrauer/chef/assets/10963153/2c6aea89-2220-40ed-a1d1-4b13c558314a" height=360>
</picture>

<picture>
 <img alt="screenshot4" src="https://github.com/jonasbrauer/chef/assets/10963153/002aad12-4e6c-4815-8793-e6125405d940" height=360>
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
