# Series Meta

**series-meta** is a command line program for downloading and applying metadata of tv series to local files. All the meta information are pulled from [TMDb](https://www.themoviedb.org/).

Currently, series-meta follows the episode naming convention _Series name - sXXeXX - Episode name_ which for example will look like _Community - s02e07 - Aerodynamics of Gender_. series-meta recommends using the following directory structure for storing tv series.

```
├── TV Shows
│   ├── Series name
│   │   ├── Season 01
│   │   │    ├── Series name - s01e01 - Episode name
│   │   │    ├── ...
│   │   ├── Season 02
│   │   │    ├── Series name - s02e01 - Episode name
│   │   │    ├── ...
```

## Usage

```
-n                       Episode number of series
-s                       Series name
```

## Examples

Navigate to the directory where you have your episodes.

```
series-meta -s 'Silicon Valley' -n 1
series-meta -s 'Community' -n 3
```

## Spread the word

If you like this script, please tell others about it. Contributions are always welcome.

- Visit my [**website**](http://www.anjithsasindran.in)
- Contact me on [**LinkedIn**](http://in.linkedin.com/in/anjithsasindran)

## MIT License

StarView is released under MIT license. See file LICENSE